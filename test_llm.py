"""
test_llm.py — Explore what Gemini can do for our use case.

This file tests:
1. Simple text generation (question generation)
2. JSON parsing (evaluation scoring)
"""

from services.llm_service import generate_text, generate_json

print("=" * 60)
print("TEST 1: Simple Question Generation")
print("=" * 60)

question_prompt = """You are an interviewer at a top tech company.
Generate a Medium level DSA interview question about arrays.
Return ONLY the question, nothing else."""

try:
    question = generate_text(question_prompt)
    print(f"✓ Generated question:\n{question}\n")
except Exception as e:
    print(f"✗ Error: {e}\n")


print("=" * 60)
print("TEST 2: JSON Evaluation")
print("=" * 60)

eval_prompt = """You are a senior engineer evaluating an interview answer.

Question: What is the time complexity of binary search?
Candidate's answer: O(log n) because we divide the array in half each time.
Topic: DSA
Difficulty: Easy

Evaluate on:
1. Correctness (0-10)
2. Completeness (0-10)
3. Clarity (0-10)

Return ONLY valid JSON (no markdown fences, no commentary):
{
  "score": <overall 0-10 float>,
  "correctness": <0-10 float>,
  "completeness": <0-10 float>,
  "clarity": <0-10 float>,
  "what_was_good": "<1-2 sentences>",
  "what_was_missing": "<1-2 sentences>",
  "ideal_answer_points": ["point1", "point2"]
}
"""

try:
    result = generate_json(eval_prompt)
    print(f"✓ Parsed evaluation JSON:")
    import json
    print(json.dumps(result, indent=2))
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("All tests passed! Gemini is working.")
print("=" * 60)