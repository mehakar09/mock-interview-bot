import streamlit as st
import json
from services.llm_service import generate_text
from prompts.question_prompts import build_question_prompt
from services.evaluator_service import evaluate_answer

st.set_page_config(page_title="AI Mock Interview Bot", layout="wide")

# Custom CSS
st.markdown("""
<style>
    body { background-color: #0f1115; color: #e8e9ed; }
    .stButton > button { background-color: #6c8cff; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 AI Mock Interview Bot")
st.markdown("Master interviews with AI-powered practice and personalized feedback")

# Initialize session state
if "session" not in st.session_state:
    st.session_state.session = {
        "stage": "setup",  # setup, interview, feedback, summary
        "name": "",
        "topic": "",
        "difficulty": "",
        "company": "",
        "role": "",
        "questions": [],
        "current_q": 0,
    }

# PAGE 1: SETUP
if st.session_state.session["stage"] == "setup":
    st.header("Setup Your Interview")
    
    name = st.text_input("Your name")
    topic = st.selectbox("Topic", ["DSA", "System Design", "HR", "Core CS"])
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    num_questions = st.selectbox("Number of questions", [3, 5, 10])
    
    company = ""
    role = ""
    if topic == "HR":
        company = st.text_input("Company (optional)", placeholder="e.g., Google")
        role = st.text_input("Role (optional)", placeholder="e.g., Software Engineer")
    
    if st.button("Start Interview", key="start"):
        if name and topic and difficulty:
            st.session_state.session["name"] = name
            st.session_state.session["topic"] = topic
            st.session_state.session["difficulty"] = difficulty
            st.session_state.session["company"] = company
            st.session_state.session["role"] = role
            st.session_state.session["num_questions"] = num_questions
            
            # Generate first question
            try:
                q = generate_text(build_question_prompt(topic, difficulty, [], company, role))
                st.session_state.session["questions"] = [{"q": q, "a": "", "score": None}]
                st.session_state.session["stage"] = "interview"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# PAGE 2: INTERVIEW
elif st.session_state.session["stage"] == "interview":
    progress = st.session_state.session["current_q"] + 1
    total = st.session_state.session["num_questions"]
    
    st.progress(progress / total)
    st.subheader(f"Question {progress} of {total}")
    
    current = st.session_state.session["questions"][st.session_state.session["current_q"]]
    st.write(current["q"])
    
    answer = st.text_area("Your answer", key="answer_input")
    
    if st.button("Submit Answer", key="submit"):
        if answer:
            try:
                # Evaluate
                result = evaluate_answer(
                    current["q"], 
                    answer, 
                    st.session_state.session["topic"],
                    st.session_state.session["difficulty"]
                )
                
                current["a"] = answer
                current["score"] = result["score"]
                current["feedback"] = result
                
                st.session_state.session["stage"] = "feedback"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# PAGE 3: FEEDBACK
elif st.session_state.session["stage"] == "feedback":
    current = st.session_state.session["questions"][st.session_state.session["current_q"]]
    
    st.subheader(f"Score: {current['score']}/10")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✓ {current['feedback']['what_was_good']}")
    with col2:
        st.error(f"✗ {current['feedback']['what_was_missing']}")
    
    st.info("**Ideal answer should cover:**")
    for point in current['feedback']['ideal_answer_points']:
        st.write(f"• {point}")
    
    progress = st.session_state.session["current_q"] + 1
    total = st.session_state.session["num_questions"]
    
    if progress < total:
        if st.button("Next Question", key="next"):
            st.session_state.session["current_q"] += 1
            try:
                prev_qs = [q["q"] for q in st.session_state.session["questions"]]
                next_q = generate_text(
                    build_question_prompt(
                        st.session_state.session["topic"],
                        st.session_state.session["difficulty"],
                        prev_qs,
                        st.session_state.session["company"],
                        st.session_state.session["role"]
                    )
                )
                st.session_state.session["questions"].append({"q": next_q, "a": "", "score": None})
                st.session_state.session["stage"] = "interview"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        if st.button("View Summary", key="summary"):
            st.session_state.session["stage"] = "summary"
            st.rerun()

# PAGE 4: SUMMARY
elif st.session_state.session["stage"] == "summary":
    scores = [q["score"] for q in st.session_state.session["questions"] if q["score"]]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    st.subheader(f"Overall Score: {avg_score:.1f}/10")
    
    st.write("**Your Answers:**")
    for i, q in enumerate(st.session_state.session["questions"], 1):
        with st.expander(f"Q{i}: {q['q'][:50]}..."):
            st.write(f"**Your answer:** {q['a']}")
            st.write(f"**Score:** {q['score']}/10")
    
    if st.button("Start New Session", key="restart"):
        st.session_state.session = {
            "stage": "setup",
            "name": "",
            "topic": "",
            "difficulty": "",
            "company": "",
            "role": "",
            "questions": [],
            "current_q": 0,
        }
        st.rerun()