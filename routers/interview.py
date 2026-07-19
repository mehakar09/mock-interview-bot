"""
routers/interview.py — FastAPI endpoints for interview sessions.

Endpoints:
- POST /session/start — Start a new interview
- GET /session/{id}/question — Get current question
- POST /session/{id}/answer — Submit answer, get evaluation
"""

from fastapi import APIRouter, HTTPException
from models.session import InterviewSession, SESSIONS, QuestionRecord
from models.question import StartSessionRequest, SubmitAnswerRequest
from services.question_service import generate_next_question
from services.evaluator_service import evaluate_answer, cap_score_if_hint_used

router = APIRouter(prefix="/session", tags=["interview"])


@router.post("/start")
def start_session(req: StartSessionRequest):
    """
    Start a new interview session.
    
    Request body:
    {
      "candidate_name": "Mehak",
      "topic": "DSA",
      "difficulty": "Medium",
      "total_questions": 5,
      "company_name": "Google",
      "role_name": "Software Engineer"
    }
    
    Response:
    {
      "session_id": "...",
      "question_number": 1,
      "total_questions": 5,
      "question": "What is..."
    }
    """
    # Create a new session
    session = InterviewSession.new(
        candidate_name=req.candidate_name,
        topic=req.topic,
        difficulty=req.difficulty,
        total_questions=req.total_questions,
        company_name=req.company_name,
        role_name=req.role_name,
    )
    
    # Store it
    SESSIONS[session.session_id] = session

    # Generate the first question
    first_question = generate_next_question(session.topic, session.difficulty, [], session.company_name, session.role_name)
    session.questions.append(QuestionRecord(question=first_question))

    return {
        "session_id": session.session_id,
        "question_number": 1,
        "total_questions": session.total_questions,
        "question": first_question,
    }


@router.get("/{session_id}/question")
def get_current_question(session_id: str):
    """
    Get the current question in a session.
    """
    session = _get_session(session_id)
    if not session.questions:
        raise HTTPException(400, "No question generated yet — call /session/start first.")
    
    idx = len(session.questions) - 1
    return {
        "question_number": idx + 1,
        "total_questions": session.total_questions,
        "question": session.questions[idx].question,
    }


@router.post("/{session_id}/answer")
def submit_answer(session_id: str, req: SubmitAnswerRequest):
    """
    Submit an answer and get evaluation.
    
    Request body:
    {
      "answer": "Binary search works by...",
      "used_hint": false
    }
    
    Response:
    {
      "evaluation": {
        "score": 8.5,
        "correctness": 9.0,
        "completeness": 8.0,
        "clarity": 8.5,
        "what_was_good": "...",
        "what_was_missing": "...",
        "ideal_answer_points": [...]
      },
      "session_finished": false,
      "next_question": "What is...",
      "question_number": 2,
      "total_questions": 5
    }
    """
    session = _get_session(session_id)
    if session.finished:
        raise HTTPException(400, "Session already finished.")

    # Get the current (unanswered) question
    current = session.questions[-1]
    current.answer = req.answer
    current.hint_used = req.used_hint

    # Evaluate the answer
    result = evaluate_answer(current.question, req.answer, session.topic, session.difficulty)
    result = cap_score_if_hint_used(result, req.used_hint)

    # Store evaluation results in the question record
    current.score = result["score"]
    current.correctness = result["correctness"]
    current.completeness = result["completeness"]
    current.clarity = result["clarity"]
    current.what_was_good = result["what_was_good"]
    current.what_was_missing = result["what_was_missing"]
    current.ideal_answer_points = result["ideal_answer_points"]

    # Decide what happens next
    is_last = len(session.questions) >= session.total_questions
    next_question = None

    if not is_last:
        # Generate the next question
        previous_qs = [q.question for q in session.questions]
        next_question = generate_next_question(session.topic, session.difficulty, previous_qs, session.company_name, session.role_name)
        session.questions.append(QuestionRecord(question=next_question))
    else:
        # This was the last question
        session.finished = True

    return {
        "evaluation": result,
        "session_finished": session.finished,
        "next_question": next_question,
        "question_number": len(session.questions) if not session.finished else session.total_questions,
        "total_questions": session.total_questions,
    }


def _get_session(session_id: str) -> InterviewSession:
    """Helper function to retrieve a session or raise 404 error."""
    session = SESSIONS.get(session_id)
    if not session:
        raise HTTPException(404, f"Session {session_id} not found.")
    return session