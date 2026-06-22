from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.base import CRUDBase
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

class CRUDNote(CRUDBase[Note, NoteCreate, NoteUpdate]):
    async def get_by_problem_id(
        self, db: AsyncSession, *, problem_id: int
    ) -> List[Note]:
        result = await db.execute(select(Note).filter(Note.problem_id == problem_id))
        return result.scalars().all()

note = CRUDNote(Note)
