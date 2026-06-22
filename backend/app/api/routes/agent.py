import logging
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any

from app.api import deps
from app.agents.orchestrator import AgentOrchestrator
from app.crud import crud_problem
from app.models.ai_data import ProblemAnalysis, ProblemSolution, ProblemReview, ProblemNotes
from app.agents.analyzer import analyzer_agent
from app.agents.solution import solution_agent
from app.agents.reviewer import reviewer_agent
from app.agents.teacher import teacher_agent
from app.agents.similarity import similarity_agent
from app.services.notes_generator import notes_generator
from app.services.streak_service import streak_service
from app.services.recommendation_service import recommendation_service

router = APIRouter()
logger = logging.getLogger(__name__)

class ScrapeRequest(BaseModel):
    url: str

@router.post("/run", response_model=Dict[str, Any])
async def run_agent(
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Launch browser, check streak, find daily challenge, extract problem, and save to DB.
    """
    orchestrator = AgentOrchestrator(db)
    result = await orchestrator.run_daily_workflow()
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
        
    return result

@router.post("/scrape", response_model=Dict[str, Any])
async def scrape_problem(
    request: ScrapeRequest,
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Scrape a specific problem by URL.
    """
    orchestrator = AgentOrchestrator(db)
    result = await orchestrator.scrape_problem(request.url)
    
    if result.get("status") == "error":
        raise HTTPException(status_code=500, detail=result.get("message"))
        
    return result

@router.get("/streak-status", response_model=Dict[str, Any])
async def get_streak_status(
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Return streak status and recommended problem.
    """
    status = await streak_service.get_streak_status(db)
    recommendation = await recommendation_service.get_recommendation()
    
    return {
        "solved_today": status["solved_today"],
        "daily_problem": status.get("daily_problem"),
        "recommended_problem": recommendation
    }

@router.post("/analyze/{slug}")
async def analyze_problem(
    slug: str,
    db: AsyncSession = Depends(deps.get_db)
):
    """
    Run the full AI multi-agent pipeline for a given problem slug.
    Checks cache first.
    """
    # 1. Check if problem exists
    problem = await crud_problem.get_by_slug(db, slug=slug)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found. Please scrape it first.")

    # 2. Check Cache
    result = await db.execute(select(ProblemAnalysis).filter(ProblemAnalysis.problem_id == problem.id))
    existing_analysis = result.scalars().first()
    
    if existing_analysis:
        # Fetch remaining cached data
        sol_res = await db.execute(select(ProblemSolution).filter(ProblemSolution.problem_id == problem.id))
        rev_res = await db.execute(select(ProblemReview).filter(ProblemReview.problem_id == problem.id))
        not_res = await db.execute(select(ProblemNotes).filter(ProblemNotes.problem_id == problem.id))
        
        return {
            "status": "cached",
            "analysis": existing_analysis.data,
            "solution": sol_res.scalars().first().data if sol_res else None,
            "review": rev_res.scalars().first().data if rev_res else None,
            "notes": not_res.scalars().first().markdown_content if not_res else None
        }

    # 3. Format Problem Data for Agents
    problem_data = {
        "title": problem.title,
        "slug": problem.slug,
        "difficulty": problem.difficulty,
        "tags": problem.topic, # Stored as comma separated string
        "statement": problem.statement,
        "constraints": problem.constraints,
        "examples": problem.examples
    }

    try:
        # --- AGENT PIPELINE ---
        
        # Analyzer
        analysis = await analyzer_agent.analyze(problem_data)
        analysis_dict = analysis.model_dump()
        
        # Solution
        solution = await solution_agent.generate_solutions(problem_data, analysis_dict)
        solution_dict = solution.model_dump()
        
        # Reviewer
        review = await reviewer_agent.review_solutions(problem_data, solution_dict)
        review_dict = review.model_dump()
        
        # Teacher
        teacher = await teacher_agent.teach(problem_data, analysis_dict, solution_dict)
        teacher_dict = teacher.model_dump()
        
        # Similarity
        # Fetch previously solved problems (with analysis)
        from sqlalchemy.orm import selectinload
        hist_probs_res = await db.execute(
            select(crud_problem.Problem)
            .filter(crud_problem.Problem.id != problem.id)
            .options(selectinload(crud_problem.Problem.analysis))
        )
        hist_probs = hist_probs_res.scalars().all()
        
        history_data = []
        for p in hist_probs:
            if p.analysis:
                history_data.append({
                    "title": p.title,
                    "topic": p.analysis.data.get("topic"),
                    "patterns": p.analysis.data.get("patterns", [])
                })
                
        similarity = await similarity_agent.find_similarities(problem_data, analysis_dict, history_data)
        similarity_dict = similarity.model_dump()
        
        # Markdown Notes Generation
        markdown = notes_generator.generate_markdown(
            problem_data, analysis_dict, solution_dict, review_dict, teacher_dict, similarity_dict
        )
        
        # --- SAVE TO DB ---
        db_analysis = ProblemAnalysis(problem_id=problem.id, data=analysis_dict)
        db_solution = ProblemSolution(problem_id=problem.id, data=solution_dict)
        db_review = ProblemReview(problem_id=problem.id, data=review_dict)
        db_notes = ProblemNotes(
            problem_id=problem.id, 
            teacher_data=teacher_dict,
            similarity_data=similarity_dict,
            markdown_content=markdown
        )
        
        db.add(db_analysis)
        db.add(db_solution)
        db.add(db_review)
        db.add(db_notes)
        await db.commit()
        
        return {
            "status": "success",
            "analysis": analysis_dict,
            "solution": solution_dict,
            "review": review_dict,
            "teacher": teacher_dict,
            "similarity": similarity_dict,
            "markdown": markdown
        }
        
    except Exception as e:
        logger.error(f"Agent pipeline failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
