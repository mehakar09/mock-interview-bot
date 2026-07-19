"""
prompts/question_prompts.py — Prompt templates for question generation.

These are the instructions we send to Gemini to generate questions.
"""


def build_question_prompt(topic: str, difficulty: str, previous_questions: list[str], company_name: str = None, role_name: str = None) -> str:
    """
    Build a prompt for generating a new question.
    
    Args:
        topic: e.g., "DSA", "System Design", "HR", "Core CS"
        difficulty: e.g., "Easy", "Medium", "Hard"
        previous_questions: List of questions already asked (to avoid repeats)
        company_name: Company name (for HR questions)
        role_name: Role/position name (for HR questions)
    
    Returns:
        A prompt string to send to the LLM
    """
    prev = "\n".join(f"- {q}" for q in previous_questions) if previous_questions else "None yet"
    
    # Special handling for HR questions
    if topic == "HR":
        company_context = ""
        if company_name and role_name:
            company_context = f"The candidate is interviewing for a {role_name} position at {company_name}."
        elif company_name:
            company_context = f"The candidate is interviewing for {company_name}."
        elif role_name:
            company_context = f"The candidate is interviewing for a {role_name} position."
        else:
            company_context = "The candidate is interviewing for a tech company."
        
        return f"""You are a recruiter conducting an interview.
{company_context}
Generate a {difficulty} level HR interview question.

Previous questions already asked in this session:
{prev}

Rules:
- Do not repeat or closely resemble any previous question above.
- The question must be answerable in a text response.
- Return ONLY the question text, nothing else — no numbering, no preamble.
"""
    
    # Generic questions for other topics
    return f"""You are an interviewer at a top tech company.
Generate a {difficulty} level {topic} interview question.

Previous questions already asked in this session:
{prev}

Rules:
- Do not repeat or closely resemble any previous question above.
- The question must be answerable in a text response (no diagrams required).
- Return ONLY the question text, nothing else — no numbering, no preamble.
"""