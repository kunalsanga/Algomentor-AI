import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NotesGenerator:
    def __init__(self, notes_dir: str = "notes"):
        self.notes_dir = notes_dir
        os.makedirs(self.notes_dir, exist_ok=True)

    def generate_markdown(self, problem: dict, analysis: dict, solution: dict, review: dict, teacher: dict, similarity: dict) -> str:
        """Generates a structured markdown note based on AI outputs"""
        slug = problem.get("slug", "unknown-problem")
        
        md = f"# {problem.get('title', slug)}\n\n"
        
        md += f"**Difficulty:** {problem.get('difficulty')}\n"
        md += f"**Topic:** {analysis.get('topic')} > {analysis.get('subtopic')}\n"
        
        patterns = ", ".join(analysis.get("patterns", []))
        if patterns:
            md += f"**Patterns:** {patterns}\n\n"
            
        md += "---\n\n## 💡 Key Insight & Intuition\n"
        md += f"{teacher.get('intuition')}\n\n"
        
        md += "### Why it works\n"
        md += f"{teacher.get('why_it_works')}\n\n"
        
        # Observations
        if analysis.get("key_observations"):
            md += "### Key Observations\n"
            for obs in analysis.get("key_observations", []):
                md += f"- {obs}\n"
            md += "\n"
        
        md += "---\n\n## 🚀 Optimal Solution\n"
        optimal_py = solution.get("optimal_python", {})
        md += f"**Time Complexity:** {optimal_py.get('time_complexity')}\n"
        md += f"**Space Complexity:** {optimal_py.get('space_complexity')}\n\n"
        
        md += "```python\n"
        md += f"{optimal_py.get('code', '')}\n"
        md += "```\n\n"
        
        md += f"**Explanation:**\n{optimal_py.get('explanation')}\n\n"
        
        md += "---\n\n## ⚠️ Common Mistakes & Bugs\n"
        for mistake in teacher.get("common_mistakes", []):
            md += f"- {mistake}\n"
        for bug in review.get("potential_bugs", []):
            md += f"- [Reviewer] {bug}\n"
        md += "\n"
        
        if similarity.get("similar_problems"):
            md += "---\n\n## 🔄 Similar Problems\n"
            md += f"You've already solved similar problems sharing patterns like **{', '.join(similarity.get('shared_patterns', []))}**:\n"
            for sim in similarity.get("similar_problems", []):
                md += f"- **{sim.get('title')}** (Similarity: {sim.get('similarity_score')})\n"
            md += "\n"
        
        md += "---\n\n## 🗣️ Interview Follow-Ups\n"
        for q in teacher.get("interview_follow_up", []):
            md += f"- {q}\n"
            
        # Save to file
        file_path = os.path.join(self.notes_dir, f"{slug}.md")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(md)
            logger.info(f"Saved note to {file_path}")
        except Exception as e:
            logger.error(f"Failed to save markdown file: {e}")
            
        return md

notes_generator = NotesGenerator()
