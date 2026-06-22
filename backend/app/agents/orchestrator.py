import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.playwright_agent.leetcode_agent import LeetCodeAgent
from app.services.streak_service import streak_service
from app.crud.crud_problem import problem as crud_problem
from app.schemas.problem import ProblemCreate

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db
        # Use headful mode initially for debugging as per requirements
        self.agent = LeetCodeAgent(headless=False)

    async def run_daily_workflow(self) -> Dict[str, Any]:
        """Run the full workflow: Check streak -> Extract Daily -> Save."""
        logger.info("Starting Agent Orchestrator Workflow")
        
        # 1. Check streak
        streak_status = await streak_service.get_streak_status(self.db)
        if streak_status["solved_today"] and streak_status["daily_problem"]:
            logger.info("Daily challenge already solved today.")
            return {
                "status": "success",
                "message": "Daily challenge already solved",
                "problem_title": streak_status["daily_problem"],
                "difficulty": streak_status["difficulty"],
                "daily_challenge": True
            }

        # 2. Extract Problem using Playwright
        try:
            await self.agent.initialize()
            
            # Navigate and extract daily
            data = await self.agent.extract_daily_challenge()
            
            # 3. Store Problem
            existing = await crud_problem.get_by_slug(self.db, slug=data["slug"])
            if not existing:
                logger.info(f"Saving problem to DB: {data['title']}")
                problem_in = ProblemCreate(**data)
                saved_problem = await crud_problem.create(self.db, obj_in=problem_in)
            else:
                logger.info(f"Problem already exists in DB: {data['title']}")
                saved_problem = existing

            return {
                "status": "success",
                "problem_title": saved_problem.title,
                "difficulty": saved_problem.difficulty,
                "daily_challenge": True
            }
        except Exception as e:
            logger.error(f"Error in orchestrator workflow: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            await self.agent.close()

    async def scrape_problem(self, url: str) -> Dict[str, Any]:
        """Extract specific problem metadata by URL."""
        logger.info(f"Starting Scrape for {url}")
        
        try:
            await self.agent.initialize()
            data = await self.agent.extract_problem(url)
            
            # Store Problem
            existing = await crud_problem.get_by_slug(self.db, slug=data["slug"])
            if not existing:
                logger.info(f"Saving problem to DB: {data['title']}")
                problem_in = ProblemCreate(**data)
                saved_problem = await crud_problem.create(self.db, obj_in=problem_in)
            else:
                logger.info(f"Problem already exists in DB: {data['title']}")
                saved_problem = existing

            return {
                "status": "success",
                "problem_title": saved_problem.title,
                "difficulty": saved_problem.difficulty,
                "daily_challenge": False
            }
        except Exception as e:
            logger.error(f"Error scraping problem: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
        finally:
            await self.agent.close()
