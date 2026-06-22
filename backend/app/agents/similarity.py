from app.core.gemini import gemini_client
from app.schemas.agent import ProblemSimilaritySchema
import json

class SimilarityAgent:
    async def find_similarities(self, current_problem: dict, analysis_data: dict, history_data: list) -> ProblemSimilaritySchema:
        if not history_data:
            # If no history, return empty structures
            return ProblemSimilaritySchema(
                similar_problems=[],
                shared_patterns=[],
                shared_topics=[]
            )
            
        history_json = json.dumps(history_data)
        
        prompt = f"""
You are an expert algorithmic learning coach.
We are building a personalized learning system. Compare the current problem the user just solved with their previously solved problems.

Current Problem:
Title: {current_problem.get('title')}
Topic: {analysis_data.get('topic')}
Subtopic: {analysis_data.get('subtopic')}
Patterns: {analysis_data.get('patterns', [])}

User's Previously Solved Problems (JSON):
{history_json}

Task:
Identify which of the previously solved problems are most similar to the current problem (up to 3).
Assign a similarity score between 0.0 and 1.0.
List the shared patterns and shared topics between them.
Return the exact JSON structure.
"""
        return await gemini_client.generate_structured(prompt, ProblemSimilaritySchema)

similarity_agent = SimilarityAgent()
