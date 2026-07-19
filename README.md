# AI Mock Interview Bot

An AI-powered mock interview platform that provides instant, personalized feedback using Google's Gemini API. Practice DSA, System Design, HR, and Core CS interviews with company and role-specific questions.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-green)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

## Features

- Multiple Interview Topics: DSA, System Design, HR, Core CS
- AI-Powered Questions: Dynamic question generation via Google Gemini API (no static banks)
- Instant Feedback: Score (0-10) with correctness, completeness, clarity breakdown
- Personalized Feedback: What you got right, what you missed, ideal answer points
- Company-Specific HR: Questions tailored to company name (e.g., "Why Google?")
- Role-Specific HR: Questions tailored to position (e.g., "Software Engineer at Google")
- Session Summaries: Overall performance, strongest/weakest areas, recommended study topics
- Full Production Deployment: Live on Streamlit Cloud with instant updates

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Frontend | Streamlit | Interactive UI, zero frontend code needed |
| LLM | Google Gemini API (free tier) | No cost, fast, production-quality responses |
| Backend Logic | Python | Clean, maintainable code structure |
| Data Storage | In-memory Session State | Quick prototyping, easily swappable for database |
| Deployment | Streamlit Cloud | Free tier, GitHub integration, auto-deploy on push |

## Live Demo

Try the app here: https://mock-interview-bot-vczz7m8vxekfbwrc9kg9ng.streamlit.app/

## Local Development

### Prerequisites

- Python 3.11+
- Gemini API key (free at Google AI Studio: https://aistudio.google.com/app/apikey)
- Git

### Setup

1. Clone the repository:
```bash
git clone https://github.com/mehakar09/mock-interview-bot.git
cd mock-interview-bot
```

2. Create .env file:
```bash
cp .env.example .env
```

3. Add your Gemini API key to .env:
```
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the app:
```bash
streamlit run streamlit_app.py
```

6. Open in browser:
```
http://localhost:8501
```

## How to Use

1. Setup: Enter your name, pick a topic (DSA/System Design/HR/Core CS), difficulty (Easy/Medium/Hard), number of questions
2. For HR questions: Optionally add company name (e.g., "Google") and role (e.g., "Software Engineer")
3. Interview: Answer each question in the text area
4. Feedback: See your score and what you got right/wrong with ideal answer points
5. Summary: After all questions, view overall performance metrics and study recommendations
6. Restart: Start a new interview session

## Interview Flow

Stage 1 - Setup
- Enter candidate name
- Select interview topic
- Choose difficulty level
- Pick number of questions
- Optionally add company and role for HR interviews

Stage 2 - Interview
- Read AI-generated question
- Type your answer
- Submit for evaluation

Stage 3 - Feedback
- See score (0-10)
- View what you got right (green)
- View what you missed (red)
- Read ideal answer points
- Move to next question

Stage 4 - Summary
- View overall score
- Review all answers
- See performance breakdown
- Start new session

## Example Questions Generated

DSA (Easy):
Given an array of integers, find the two numbers that add up to a target sum.

System Design (Medium):
Design a URL shortener service like bit.ly. How would you handle 1M requests/day?

HR at Google (Software Engineer):
Why do you want to work at Google as a Software Engineer, and what excites you most about this role?

Core CS (Hard):
Explain the difference between process and thread. When would you use each?

## Interview Feedback Example

Score: 8.5/10

What you got right:
Correctly identified binary search time complexity and explained the reasoning.

What you missed:
Could have mentioned prerequisite of sorted array and space complexity.

Ideal answer should cover:
- O(log n) time complexity
- Binary search requires sorted array
- Divide-and-conquer approach
- Space complexity O(1) for iterative

## Project Structure

```
mock-interview-bot/
├── streamlit_app.py                 # Streamlit app (main entry point)
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── models/
│   ├── session.py                   # Interview session models
│   └── question.py                  # Request/response schemas
├── services/
│   ├── llm_service.py               # Gemini API wrapper
│   ├── question_service.py          # Question generation logic
│   └── evaluator_service.py         # Answer evaluation logic
├── prompts/
│   ├── question_prompts.py          # Question generation prompts
│   └── eval_prompts.py              # Evaluation prompts
└── README.md                        # This file
```

## Resume Bullets

For your CV, use these bullet points:

- Developed AI-powered mock interview platform using Python and Streamlit with dynamic question generation via Google Gemini API
- Implemented multi-topic interview support (DSA, System Design, HR, Core CS) with company and role-specific prompt engineering
- Designed structured LLM prompting system with JSON response parsing for consistent scoring and feedback breakdown
- Deployed full-stack application on Streamlit Cloud with GitHub integration and auto-deployment on code push
- Created interactive multi-stage interview flow (setup, interview, feedback, summary) with real-time AI evaluation

## Deployment to Streamlit Cloud

1. Fork or push code to GitHub repository
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Connect GitHub account
5. Select repository: mock-interview-bot
6. Main file path: streamlit_app.py
7. Click "Deploy"
8. Add secrets in app settings:
   - GEMINI_API_KEY: your actual API key
   - GEMINI_MODEL: gemini-3.5-flash
9. App goes live in 2-3 minutes

## Future Enhancements

- Conversational Mode: Real back-and-forth interviews with follow-up questions
- Panel Mode: Mix topics in one session (e.g., 2 DSA + 2 HR + 1 System Design)
- Project-Based Grilling: Upload resume or projects and get interviewed on them
- Database Persistence: Store sessions in PostgreSQL for history tracking
- User Authentication: Track interview history and progress over time
- Difficulty Auto-Escalation: Questions get harder if you score well
- Audio/Video Mode: Record your answers for delivery feedback
- Leaderboard: Compare your scores with other users
- Mobile App: React Native version for iOS/Android

## Known Limitations

- Sessions are stored in Streamlit session state (cleared on app restart)
- Gemini API free tier has rate limits (approximately 60 requests per minute)
- No user authentication yet (sessions are temporary)

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Feel free to:
- Report bugs via GitHub Issues
- Suggest features
- Submit pull requests

## Questions

Open an issue on GitHub or contact the maintainer directly.

---

Built with Python, Streamlit, and Google Gemini API
