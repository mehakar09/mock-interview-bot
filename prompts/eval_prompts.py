"""
prompts/eval_prompts.py — Prompt templates for answer evaluation.

These are the instructions we send to Gemini to score answers.
"""


def build_eval_prompt(question: str, answer: str, topic: str, difficulty: str) -> str:
    """
    Build a prompt for evaluating a candidate's answer.
    
    Args:
        question: The interview question asked
        answer: The candidate's answer
        topic: e.g., "DSA", "System Design"
        difficulty: e.g., "Easy", "Medium", "Hard"
    
    Returns:
        A prompt string to send to the LLM
    """
    return f"""You are a senior engineer evaluating an interview answer.

Question: {question}
Candidate's answer: {answer}
Topic: {topic}
Difficulty: {difficulty}

Evaluate on:
1. Correctness (0-10) — Is the answer factually correct?
2. Completeness (0-10) — Did they cover all important points?
3. Clarity (0-10) — Is the explanation clear and easy to follow?

Return ONLY valid JSON (no markdown fences, no commentary):
{{
  "score": <overall 0-10 float, average of the three>,
  "correctness": <0-10 float>,
  "completeness": <0-10 float>,
  "clarity": <0-10 float>,
  "what_was_good": "<1-2 sentences about what the candidate got right>",
  "what_was_missing": "<1-2 sentences about what could be improved>",
  "ideal_answer_points": ["point1", "point2", "point3"]
}}
"""


def build_summary_prompt(topic: str, difficulty: str, transcript: str) -> str:
    """
    Build a prompt for generating a session summary.
    
    Args:
        topic: Interview topic
        difficulty: Interview difficulty
        transcript: Full Q&A transcript
    
    Returns:
        A prompt string to send to the LLM
    """
    return f"""You are a senior engineer summarizing a mock interview.

Topic: {topic}
Difficulty: {difficulty}

Full transcript (question, answer, score for each round):
{transcript}

Return ONLY valid JSON (no markdown fences, no commentary):
{{
  "overall_score": <0-10 float>,
  "strongest_areas": ["area1", "area2"],
  "weakest_areas": ["area1", "area2"],
  "recommended_study_topics": ["topic1", "topic2"],
  "summary_note": "<2-3 sentence overall impression>"
}}
"""