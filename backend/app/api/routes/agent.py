import logging
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.agents.orchestrator import AgentOrchestrator
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
