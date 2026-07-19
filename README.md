# AI Mock Interview Bot

An AI-powered mock interview platform that provides instant, personalized feedback using Google's Gemini API. Practice DSA, System Design, HR, and Core CS interviews with company and role-specific questions.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

## Features

- **Multiple Interview Topics**: DSA, System Design, HR, Core CS
- **AI-Powered Questions**: Dynamic question generation via Google Gemini API (no static banks)
- **Instant Feedback**: Score (0-10) + correctness, completeness, clarity breakdown
- **Personalized Feedback**: What you got right, what you missed, ideal answer points
- **Company-Specific HR**: Questions tailored to company name (e.g., "Why Google?")
- **Role-Specific HR**: Questions tailored to position (e.g., "Software Engineer at Google")
- **Session Summaries**: Overall performance, strongest/weakest areas, recommended study topics
- **Hint System**: Get a hint but score caps at 7/10
- **Full Production Deployment**: Live on Railway with auto-scaling

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Backend | Python + FastAPI | Async, auto-generated docs, minimal boilerplate |
| LLM | Google Gemini API (free tier) | No cost, fast, production-quality responses |
| Frontend | HTML/CSS/JavaScript (vanilla) | No build step, zero dependencies |
| Data Storage | In-memory (Python dict) | Quick prototyping, easily swappable for DB |
| Deployment | Railway | Free tier, GitHub auto-deployment, simple scaling |

## Live Demo

**[Try it here](https://mock-interview-bot-production.up.railway.app)** (replace with your Railway URL)

## Local Development

### Prerequisites

- Python 3.8+
- Gemini API key (free at [Google AI Studio](https://aistudio.google.com/app/apikey))
- Git

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/mehakar09/mock-interview-bot.git
cd mock-interview-bot
```

2. **Create `.env` file:**
```bash
cp .env.example .env
```

3. **Add your Gemini API key to `.env`:**
GEMINI_API_KEY= your_key_here_replace_with_actual_key
GEMINI_MODEL=gemini-3.5-flash
4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the server:**
```bash
uvicorn main:app --reload
```

6. **Open in browser:**
http://localhost:8000/
##How to Use

1. **Setup**: Enter your name, pick a topic (DSA/System Design/HR/Core CS), difficulty (Easy/Medium/Hard)
2. **For HR questions**: Optionally add company name (e.g., "Google") and role (e.g., "Software Engineer")
3. **Interview**: Answer each question in the text area
4. **Feedback**: See your score and what you got right/wrong
5. **Summary**: After all questions, view overall performance and study recommendations

## API Endpoints
POST /session/start

Start a new interview session
Body: { candidate_name, topic, difficulty, total_questions, company_name?, role_name? }

GET /session/{session_id}/question

Get the current question

POST /session/{session_id}/answer

Submit an answer and get evaluation
Body: { answer, used_hint }

GET /session/{session_id}/summary

Get the full session summary (after completion)
## Project Structure
mock-interview-bot/
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── models/
│   ├── session.py                   # InterviewSession & QuestionRecord models
│   └── question.py                  # Request/response schemas
├── routers/
│   ├── interview.py                 # /session endpoints
│   └── feedback.py                  # /summary endpoint
├── services/
│   ├── llm_service.py               # Gemini API wrapper
│   ├── question_service.py          # Question generation logic
│   └── evaluator_service.py         # Answer evaluation logic
├── prompts/
│   ├── question_prompts.py          # Question generation prompts
│   └── eval_prompts.py              # Evaluation & summary prompts
└── static/
└── index.html                   # Frontend (all 4 pages in 1 file)
## Example Questions Generated

**DSA (Easy):**
> Given an array of integers, find the two numbers that add up to a target sum.

**System Design (Medium):**
> Design a URL shortener service like bit.ly. How would you handle 1M requests/day?

**HR @ Google (Software Engineer):**
> Why do you want to work at Google as a Software Engineer, and what excites you most about this role?

**Core CS (Hard):**
> Explain the difference between process and thread. When would you use each?

## Interview Feedback Example
Score: 8.5/10
✓ What you got right:
Correctly identified binary search time complexity and explained the reasoning.
✗ What you missed:
Could have mentioned prerequisite of sorted array and space complexity.
Ideal answer should cover:
• O(log n) time complexity
• Binary search requires sorted array
• Divide-and-conquer approach
• Space complexity O(1) for iterative

## 🔮 Future Enhancements

- [ ] **Conversational Mode**: Real back-and-forth interviews with follow-up questions
- [ ] **Panel Mode**: Mix topics in one session (e.g., 2 DSA + 2 HR + 1 System Design)
- [ ] **Project-Based Grilling**: Upload your resume/projects and get interviewed on them
- [ ] **Database Persistence**: Store sessions in PostgreSQL so they survive server restarts
- [ ] **User Authentication**: Track interview history and progress over time
- [ ] **Difficulty Auto-Escalation**: Questions get harder if you score well
- [ ] **Audio/Video Mode**: Record your answers and get feedback on delivery
- [ ] **Leaderboard**: Compare your scores with other users
- [ ] **Mobile App**: React Native version for iOS/Android

## 🐛 Known Limitations

- Sessions are stored in-memory (cleared on server restart) — use database for persistence
- Gemini API free tier has rate limits (~60 requests/minute)
- No user authentication yet (anyone can access any session if they have the ID)

## 📝 License

MIT License — see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs via GitHub Issues
- Suggest features
- Submit pull requests

## 📧 Questions?

Open an issue on GitHub or contact me directly.

---

**Built with ❤️ using FastAPI + Gemini API**