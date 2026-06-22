from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.problem import Problem
from app.schemas.problem import ProblemCreate, ProblemUpdate

class CRUDProblem(CRUDBase[Problem, ProblemCreate, ProblemUpdate]):
    async def get_by_url(self, db: AsyncSession, *, url: str) -> Optional[Problem]:
        result = await db.execute(select(Problem).filter(Problem.url == url))
        return result.scalars().first()

    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Optional[Problem]:
        result = await db.execute(select(Problem).filter(Problem.slug == slug))
        return result.scalars().first()

problem = CRUDProblem(Problem)
