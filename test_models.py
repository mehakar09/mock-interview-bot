"""
Test that the Session model works correctly.
"""

from models.session import InterviewSession, QuestionRecord, SESSIONS

print("=" * 60)
print("TEST: Creating an Interview Session")
print("=" * 60)

# Create a new session
session = InterviewSession.new(
    candidate_name="Mehak",
    topic="DSA",
    difficulty="Medium",
    total_questions=5
)

print(f"✓ Session created!")
print(f"  - Session ID: {session.session_id}")
print(f"  - Candidate: {session.candidate_name}")
print(f"  - Topic: {session.topic}")
print(f"  - Difficulty: {session.difficulty}")
print(f"  - Total Questions: {session.total_questions}")
print(f"  - Created at: {session.created_at}")

# Add a question to the session
session.questions.append(
    QuestionRecord(
        question="What is the time complexity of binary search?"
    )
)

print(f"\n✓ Question added!")
print(f"  - Question: {session.questions[0].question}")
print(f"  - Answer: {session.questions[0].answer}")
print(f"  - Score: {session.questions[0].score}")

# Simulate storing the session
SESSIONS[session.session_id] = session

print(f"\n✓ Session stored in memory!")
print(f"  - Total sessions in memory: {len(SESSIONS)}")

# Retrieve the session
retrieved = SESSIONS[session.session_id]
print(f"\n✓ Session retrieved!")
print(f"  - Retrieved candidate: {retrieved.candidate_name}")
print(f"  - Retrieved topic: {retrieved.topic}")

print("\n" + "=" * 60)
print("All model tests passed!")
print("=" * 60)