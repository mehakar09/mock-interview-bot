"""
services/question_service.py — Business logic for question generation.
"""

from services.llm_service import generate_text
from prompts.question_prompts import build_question_prompt


def generate_next_question(topic: str, difficulty: str, previous_questions: list[str], company_name: str = None, role_name: str = None) -> str:
    """
    Generate the next interview question.
    
    Args:
        topic: "DSA", "System Design", etc.
        difficulty: "Easy", "Medium", "Hard"
        previous_questions: Questions already asked
        company_name: Company name (for HR questions)
        role_name: Role/position name (for HR questions)
    
    Returns:
        A new question string
    """
    prompt = build_question_prompt(topic, difficulty, previous_questions, company_name, role_name)
    return generate_text(prompt)