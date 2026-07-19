"""
main.py — FastAPI app entry point.

This file creates the FastAPI app and registers all routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import routers
from routers import interview, feedback

app = FastAPI(
    title="AI Mock Interview Bot",
    description="Practice interviews with AI feedback",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(interview.router)
app.include_router(feedback.router)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def serve_frontend():
    """Serve the main frontend page."""
    return FileResponse("static/index.html")


@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)