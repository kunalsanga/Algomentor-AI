from app.core.gemini import gemini_client
from app.schemas.agent import ProblemReviewSchema

class ReviewerAgent:
    async def review_solutions(self, problem_data: dict, solution_data: dict) -> ProblemReviewSchema:
        prompt = f"""
You are an expert Senior Software Engineer conducting a Code Review.
Review the provided optimal solutions for a LeetCode problem. Check for bugs, edge cases, and verify the complexity.

Problem Title: {problem_data.get('title')}

Constraints:
{problem_data.get('constraints')}

Optimal Python Code:
{solution_data.get('optimal_python', {}).get('code', '')}

Optimal C++ Code:
{solution_data.get('optimal_cpp', {}).get('code', '')}

Task:
1. Ensure edge cases (like empty arrays, large limits, negative numbers) are handled.
2. Identify any potential bugs.
3. Verify if the time and space complexities stated are strictly accurate.
4. Suggest micro-optimizations if any exist.

Return the exact JSON structure.
"""
        return await gemini_client.generate_structured(prompt, ProblemReviewSchema)

reviewer_agent = ReviewerAgent()
