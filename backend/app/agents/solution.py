from app.core.gemini import gemini_client
from app.schemas.agent import ProblemSolutionSchema

class SolutionAgent:
    async def generate_solutions(self, problem_data: dict, analysis_data: dict) -> ProblemSolutionSchema:
        prompt = f"""
You are an expert Competitive Programmer and Software Engineer.
Given the problem statement and the architectural analysis, generate Brute Force, Better (if applicable), and Optimal solutions in both Python and C++.
If Brute Force and Better are the same, or Better doesn't make sense, omit Better. Always provide Optimal.

Problem Title: {problem_data.get('title')}
Problem Statement:
{problem_data.get('statement')}

Analysis Context:
Topic: {analysis_data.get('topic')}
Algorithm: {analysis_data.get('recommended_algorithm')}

Task:
Return the exact JSON structure containing the C++ and Python code for Brute Force, Better, and Optimal solutions.
Also provide the time and space complexity for each. Do not include markdown formatting around the JSON.
"""
        return await gemini_client.generate_structured(prompt, ProblemSolutionSchema)

solution_agent = SolutionAgent()
