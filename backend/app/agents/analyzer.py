from app.core.gemini import gemini_client
from app.schemas.agent import ProblemAnalysisSchema

class AnalyzerAgent:
    async def analyze(self, problem_data: dict) -> ProblemAnalysisSchema:
        prompt = f"""
You are an expert algorithmic problem analyzer.
Analyze the following LeetCode problem and output the exact JSON structure requested.

Title: {problem_data.get('title')}
Difficulty: {problem_data.get('difficulty')}
Tags: {problem_data.get('tags')}

Statement:
{problem_data.get('statement')}

Constraints:
{problem_data.get('constraints')}

Examples:
{problem_data.get('examples')}

Task:
Provide a detailed structural breakdown of this problem. Identify the primary topic, subtopics, the core algorithm or pattern required, and key observations necessary to reach the optimal solution. Explain why it holds its current difficulty rating.
"""
        return await gemini_client.generate_structured(prompt, ProblemAnalysisSchema)

analyzer_agent = AnalyzerAgent()
