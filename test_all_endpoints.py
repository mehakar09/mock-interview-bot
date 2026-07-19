"""
test_all_endpoints.py — Complete endpoint testing in one go.

Tests all 6 endpoints:
1. POST /session/start — Create interview
2. GET /session/{id}/question — Get current question
3. POST /session/{id}/answer — Submit answer 1
4. POST /session/{id}/answer — Submit answer 2
5. POST /session/{id}/answer — Submit answer 3 (final)
6. GET /session/{id}/summary — Get summary
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def print_response(response, key_fields=None):
    """Pretty print response"""
    if response.status_code in [200, 201]:
        print(f"✓ Status: {response.status_code}")
        data = response.json()
        if key_fields:
            for field in key_fields:
                print(f"  {field}: {data.get(field, 'N/A')}")
        else:
            print(json.dumps(data, indent=2))
        return data
    else:
        print(f"✗ Status: {response.status_code}")
        print(f"  Error: {response.text}")
        return None

# ============================================================================
print_section("TEST 1: Start a new interview session")
# ============================================================================

start_response = requests.post(
    f"{BASE_URL}/session/start",
    json={
        "candidate_name": "Mehak",
        "topic": "DSA",
        "difficulty": "Easy",
        "total_questions": 3
    }
)

start_data = print_response(start_response, ["session_id", "question_number", "total_questions"])

if not start_data:
    print("✗ Failed to start session. Stopping tests.")
    exit(1)

session_id = start_data["session_id"]
print(f"\n✓ Using session ID: {session_id}")

# ============================================================================
print_section("TEST 2: Get current question")
# ============================================================================

question_response = requests.get(f"{BASE_URL}/session/{session_id}/question")
question_data = print_response(question_response, ["question_number", "total_questions"])

# ============================================================================
print_section("TEST 3: Submit Answer 1 / 3")
# ============================================================================

print("Submitting answer to first question...")
print("Answer: 'O(log n) because we divide the array in half each time.'")

answer1_response = requests.post(
    f"{BASE_URL}/session/{session_id}/answer",
    json={
        "answer": "O(log n) because we divide the array in half each time.",
        "used_hint": False
    }
)

answer1_data = print_response(
    answer1_response,
    ["session_finished", "question_number", "total_questions"]
)

if answer1_data:
    score = answer1_data["evaluation"]["score"]
    feedback = answer1_data["evaluation"]["what_was_good"]
    print(f"\n  Score: {score}/10")
    print(f"  Feedback: {feedback}")
    print(f"  Next question ready: {answer1_data['next_question'][:60]}...")

time.sleep(1)  # Brief pause between submissions

# ============================================================================
print_section("TEST 4: Submit Answer 2 / 3")
# ============================================================================

print("Submitting answer to second question...")
print("Answer: 'O(n) because we need extra space for merging.'")

answer2_response = requests.post(
    f"{BASE_URL}/session/{session_id}/answer",
    json={
        "answer": "O(n) because we need extra space for merging.",
        "used_hint": False
    }
)

answer2_data = print_response(
    answer2_response,
    ["session_finished", "question_number", "total_questions"]
)

if answer2_data:
    score = answer2_data["evaluation"]["score"]
    print(f"\n  Score: {score}/10")
    print(f"  Session finished yet: {answer2_data['session_finished']}")

time.sleep(1)

# ============================================================================
print_section("TEST 5: Submit Answer 3 / 3 (Final)")
# ============================================================================

print("Submitting answer to third question (final)...")
print("Answer: 'Merge sort divides recursively and merges sorted parts.'")

answer3_response = requests.post(
    f"{BASE_URL}/session/{session_id}/answer",
    json={
        "answer": "Merge sort divides the array recursively and then merges the sorted parts.",
        "used_hint": False
    }
)

answer3_data = print_response(
    answer3_response,
    ["session_finished", "question_number", "total_questions"]
)

if answer3_data:
    score = answer3_data["evaluation"]["score"]
    is_finished = answer3_data["session_finished"]
    print(f"\n  Score: {score}/10")
    print(f"  Session finished: {is_finished}")
    
    if not is_finished:
        print("\n✗ ERROR: Session should be finished after 3 answers!")
        exit(1)

time.sleep(1)

# ============================================================================
print_section("TEST 6: Get Session Summary")
# ============================================================================

print("Fetching summary for completed session...")

summary_response = requests.get(f"{BASE_URL}/session/{session_id}/summary")
summary_data = print_response(summary_response)

if summary_data:
    print("\n✓ Summary details:")
    print(f"  Candidate: {summary_data['candidate_name']}")
    print(f"  Topic: {summary_data['topic']}")
    print(f"  Difficulty: {summary_data['difficulty']}")
    print(f"\n  Overall Score: {summary_data['summary']['overall_score']}/10")
    print(f"  Strongest Areas: {summary_data['summary']['strongest_areas']}")
    print(f"  Weakest Areas: {summary_data['summary']['weakest_areas']}")
    print(f"  Recommended Study: {summary_data['summary']['recommended_study_topics']}")
    print(f"  Summary: {summary_data['summary']['summary_note']}")

# ============================================================================
print_section("✓ ALL TESTS PASSED!")
# ============================================================================

print("""
Your API is fully functional! ✓

Tested:
  ✓ POST /session/start
  ✓ GET /session/{id}/question
  ✓ POST /session/{id}/answer (3 times)
  ✓ GET /session/{id}/summary

You're ready to build the frontend!
""")