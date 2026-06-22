from app.core.gemini import gemini_client
from app.schemas.agent import ProblemTeacherSchema

class TeacherAgent:
    async def teach(self, problem_data: dict, analysis_data: dict, solution_data: dict) -> ProblemTeacherSchema:
        prompt = f"""
You are an expert Computer Science Professor and algorithmic coach.
Explain the intuition and optimal solution to a student in a beginner-friendly way.

Problem Title: {problem_data.get('title')}
Topic: {analysis_data.get('topic')}
Algorithm: {analysis_data.get('recommended_algorithm')}
Optimal Python Solution:
{solution_data.get('optimal_python', {}).get('code', '')}

Task:
1. Explain the "Intuition" - how someone should naturally think about arriving at this solution.
2. Explain "Why it works" fundamentally.
3. List common mistakes or pitfalls students face.
4. List interview follow-up questions they might be asked.
5. Provide a tip on recognizing this pattern in future problems.

Return the exact JSON structure.
"""
        return await gemini_client.generate_structured(prompt, ProblemTeacherSchema)

teacher_agent = TeacherAgent()
