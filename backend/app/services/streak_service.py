import logging
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from datetime import datetime, timezone

from app.models.problem import Problem

logger = logging.getLogger(__name__)

class StreakService:
    async def get_streak_status(self, db: AsyncSession) -> Dict[str, Any]:
        """Check if today's daily challenge is solved based on local DB."""
        today = datetime.now(timezone.utc).date()
        
        # Check if any problem was solved today
        stmt = select(Problem).filter(cast(Problem.created_at, Date) == today)
        result = await db.execute(stmt)
        problems_today = result.scalars().all()
        
        solved_today = len(problems_today) > 0
        
        daily_problem = None
        difficulty = None
        url = None
        
        for p in problems_today:
            if p.daily_challenge:
                daily_problem = p.title
                difficulty = p.difficulty
                url = p.url
                break
                
        return {
            "solved_today": solved_today,
            "daily_problem": daily_problem,
            "difficulty": difficulty,
            "url": url
        }

streak_service = StreakService()
