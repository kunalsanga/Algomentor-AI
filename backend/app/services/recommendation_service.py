import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RecommendationService:
    async def get_recommendation(self) -> Dict[str, Any]:
        """Return a recommended problem."""
        # For now, return a placeholder or static recommendation
        # In a real app, we'd query LeetCode API or DB to find unsolved problems
        
        return {
            "title": "Two Sum",
            "url": "https://leetcode.com/problems/two-sum",
            "difficulty": "Easy",
            "reason": "Popular Interview Question"
        }

recommendation_service = RecommendationService()
