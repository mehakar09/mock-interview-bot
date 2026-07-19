"""
models/session.py — Data structures for interview sessions.

This file defines:
- QuestionRecord: A single Q&A exchange
- InterviewSession: Full interview (multiple questions)
- SESSIONS: In-memory storage (no database needed to start)
"""

from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
import uuid
import time


class QuestionRecord(BaseModel):
    """A single question-answer exchange in an interview."""
    
    question: str
    answer: Optional[str] = None  # Empty until candidate answers
    score: Optional[float] = None
    correctness: Optional[float] = None
    completeness: Optional[float] = None
    clarity: Optional[float] = None
    what_was_good: Optional[str] = None
    what_was_missing: Optional[str] = None
    ideal_answer_points: List[str] = []
    hint_used: bool = False


class InterviewSession(BaseModel):
    """A complete interview session (multiple questions)."""
    
    session_id: str
    candidate_name: str
    topic: str  # "DSA", "System Design", "HR", "Core CS", etc.
    difficulty: str  # "Easy", "Medium", "Hard"
    company_name: Optional[str] = None  # Company name if HR questions
    role_name: Optional[str] = None  # Role name if HR questions
    total_questions: int = 5
    questions: List[QuestionRecord] = []
    created_at: float = 0.0
    finished: bool = False

    @classmethod
    def new(cls, candidate_name: str, topic: str, difficulty: str, total_questions: int = 5, company_name: Optional[str] = None, role_name: Optional[str] = None) -> "InterviewSession":
        """Create a new interview session with a unique ID and timestamp."""
        return cls(
            session_id=str(uuid.uuid4()),  # Unique ID like "a1b2c3d4-e5f6-..."
            candidate_name=candidate_name,
            topic=topic,
            difficulty=difficulty,
            company_name=company_name,
            role_name=role_name,
            total_questions=total_questions,
            created_at=time.time(),  # When the session started
        )


# Simple in-memory storage
# Key: session_id, Value: InterviewSession object
# (Later we'll swap this for a real database)
SESSIONS: dict[str, InterviewSession] = {}