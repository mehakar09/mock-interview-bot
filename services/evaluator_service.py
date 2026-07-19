"""
services/evaluator_service.py — Business logic for answer evaluation.
"""

from services.llm_service import generate_json
from prompts.eval_prompts import build_eval_prompt, build_summary_prompt
from models.session import InterviewSession


def evaluate_answer(question: str, answer: str, topic: str, difficulty: str) -> dict:
    """
    Evaluate a candidate's answer and return scores.
    
    Args:
        question: The question asked
        answer: The candidate's answer
        topic: Interview topic
        difficulty: Interview difficulty
    
    Returns:
        Dict with score, correctness, completeness, clarity, feedback
    """
    prompt = build_eval_prompt(question, answer, topic, difficulty)
    result = generate_json(prompt)
    
    # Ensure all expected keys exist (safety check)
    result.setdefault("score", 0)
    result.setdefault("correctness", 0)
    result.setdefault("completeness", 0)
    result.setdefault("clarity", 0)
    result.setdefault("what_was_good", "")
    result.setdefault("what_was_missing", "")
    result.setdefault("ideal_answer_points", [])
    
    return result


def cap_score_if_hint_used(result: dict, hint_used: bool) -> dict:
    """
    If a hint was used, cap the score at 7/10.
    
    Args:
        result: The evaluation result dict
        hint_used: Whether the candidate used a hint
    
    Returns:
        The modified result dict
    """
    if hint_used and result.get("score", 0) > 7:
        result["score"] = 7.0
    return result


def generate_summary(session: InterviewSession) -> dict:
    """
    Generate a summary of the entire interview session.
    
    Args:
        session: The completed interview session
    
    Returns:
        Dict with overall_score, strongest_areas, weakest_areas, etc.
    """
    # Build a transcript of all Q&As
    lines = []
    for i, q in enumerate(session.questions, start=1):
        lines.append(
            f"Q{i}: {q.question}\n"
            f"Answer: {q.answer}\n"
            f"Score: {q.score}\n"
        )
    transcript = "\n".join(lines)
    
    prompt = build_summary_prompt(session.topic, session.difficulty, transcript)
    return generate_json(prompt)