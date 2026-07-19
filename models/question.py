"""
models/question.py — Request and response data structures for FastAPI.

These are the JSON shapes that the frontend sends and receives.
"""

from pydantic import BaseModel
from typing import Optional


class StartSessionRequest(BaseModel):
    """Frontend sends this to start a new interview."""
    candidate_name: str
    topic: str          # "DSA", "System Design", "HR", "Core CS"
    difficulty: str     # "Easy", "Medium", "Hard"
    total_questions: int = 5
    company_name: Optional[str] = None  # Optional company name for HR questions
    role_name: Optional[str] = None  # Optional role name for HR questions


class SubmitAnswerRequest(BaseModel):
    """Frontend sends this when candidate submits their answer."""
    answer: str
    used_hint: bool = False


class EvaluationResult(BaseModel):
    """Response sent back with evaluation scores."""
    score: float
    correctness: float
    completeness: float
    clarity: float
    what_was_good: str
    what_was_missing: str
    ideal_answer_points: list[str]