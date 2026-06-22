from pydantic import BaseModel, Field
from typing import List, Optional

# -----------------
# 1. Analyzer Schema
# -----------------
class ProblemAnalysisSchema(BaseModel):
    topic: str = Field(description="The primary data structure or topic (e.g., Array, Graph, Dynamic Programming)")
    subtopic: str = Field(description="A more specific subtopic (e.g., Breadth-First Search, Two Pointers)")
    patterns: List[str] = Field(description="List of common algorithmic patterns used to solve this")
    difficulty_assessment: str = Field(description="A brief explanation of why the problem has its given difficulty")
    key_observations: List[str] = Field(description="List of core insights required to solve the problem")
    recommended_algorithm: str = Field(description="The name of the optimal algorithm to use")

# -----------------
# 2. Solution Schema
# -----------------
class SolutionCodeSchema(BaseModel):
    code: str
    explanation: str
    time_complexity: str
    space_complexity: str

class ProblemSolutionSchema(BaseModel):
    brute_force_cpp: Optional[SolutionCodeSchema] = None
    brute_force_python: Optional[SolutionCodeSchema] = None
    better_cpp: Optional[SolutionCodeSchema] = None
    better_python: Optional[SolutionCodeSchema] = None
    optimal_cpp: SolutionCodeSchema
    optimal_python: SolutionCodeSchema

# -----------------
# 3. Reviewer Schema
# -----------------
class ProblemReviewSchema(BaseModel):
    edge_cases_handled: List[str] = Field(description="List of edge cases the solution handles properly")
    potential_bugs: List[str] = Field(description="Any identified bugs or edge cases missed")
    complexity_verification: str = Field(description="Verification if the stated time/space complexity is accurate")
    optimizations: List[str] = Field(description="Any further micro-optimizations that can be done")

# -----------------
# 4. Teacher Schema
# -----------------
class ProblemTeacherSchema(BaseModel):
    intuition: str = Field(description="A beginner-friendly explanation of the intuition behind the optimal approach")
    why_it_works: str = Field(description="Explanation of why this approach guarantees the correct answer")
    common_mistakes: List[str] = Field(description="Common pitfalls students fall into when solving this")
    interview_follow_up: List[str] = Field(description="Potential follow-up questions an interviewer might ask")
    pattern_recognition_tips: str = Field(description="Tips on how to recognize this pattern in future problems")

# -----------------
# 5. Similarity Schema
# -----------------
class SimilarProblemEntry(BaseModel):
    title: str
    similarity_score: float

class ProblemSimilaritySchema(BaseModel):
    similar_problems: List[SimilarProblemEntry] = Field(description="List of similar previously solved problems")
    shared_patterns: List[str] = Field(description="Patterns shared with similar problems")
    shared_topics: List[str] = Field(description="Topics shared with similar problems")
