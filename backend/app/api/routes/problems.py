from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Problem])
async def read_problems(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve problems.
    """
    problems = await crud.problem.get_multi(db, skip=skip, limit=limit)
    return problems

@router.post("/", response_model=schemas.Problem)
async def create_problem(
    *,
    db: AsyncSession = Depends(deps.get_db),
    problem_in: schemas.ProblemCreate,
) -> Any:
    """
    Create new problem.
    """
    problem = await crud.problem.get_by_url(db, url=problem_in.url)
    if problem:
        raise HTTPException(
            status_code=400,
            detail="The problem with this URL already exists in the system.",
        )
    problem = await crud.problem.create(db, obj_in=problem_in)
    return problem

@router.get("/{id}", response_model=schemas.Problem)
async def read_problem(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get problem by ID.
    """
    problem = await crud.problem.get(db, id=id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.delete("/{id}", response_model=schemas.Problem)
async def delete_problem(
    *,
    db: AsyncSession = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Delete a problem.
    """
    problem = await crud.problem.get(db, id=id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    problem = await crud.problem.remove(db, id=id)
    return problem
