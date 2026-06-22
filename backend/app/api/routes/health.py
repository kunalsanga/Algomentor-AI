from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "LeetCode Agentic Learning Assistant is running"}
