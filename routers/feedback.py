"""
routers/feedback.py — FastAPI endpoints for session summaries and feedback.
"""

from fastapi import APIRouter, HTTPException
from models.session import SESSIONS
from services.evaluator_service import generate_summary

router = APIRouter(prefix="/session", tags=["feedback"])


@router.get("/{session_id}/summary")
def get_summary(session_id: str):
    """
    Get a summary of the completed interview session.
    
    Returns:
    {
      "candidate_name": "Mehak",
      "topic": "DSA",
      "difficulty": "Medium",
      "summary": {
        "overall_score": 8.2,
        "strongest_areas": ["Arrays", "Sorting"],
        "weakest_areas": ["Graphs"],
        "recommended_study_topics": ["Graph traversal"],
        "summary_note": "..."
      },
      "per_question": [
        {
          "question": "...",
          "score": 8.5,
          "what_was_good": "...",
          "what_was_missing": "..."
        }
      ]
    }
    """
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, f"Session {session_id} not found.")
    if not session.finished:
        raise HTTPException(400, "Session is not finished yet.")

    # Generate the summary using the LLM
    summary = generate_summary(session)

    # Also return per-question breakdown
    per_question = [
        {
            "question": q.question,
            "score": q.score,
            "what_was_good": q.what_was_good,
            "what_was_missing": q.what_was_missing,
        }
        for q in session.questions
    ]

    return {
        "candidate_name": session.candidate_name,
        "topic": session.topic,
        "difficulty": session.difficulty,
        "summary": summary,
        "per_question": per_question,
    }