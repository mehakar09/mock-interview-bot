"""
llm_service.py — Wrapper around Gemini API.

This file handles ALL communication with the LLM.
If you want to swap Gemini for OpenAI/Groq later, 
you only need to change this file.
"""

import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key and model name from .env
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Configure the Gemini SDK
if API_KEY:
    genai.configure(api_key=API_KEY)
    _model = genai.GenerativeModel(MODEL_NAME)
else:
    _model = None
    print("⚠️  WARNING: GEMINI_API_KEY not set in .env file")


def generate_text(prompt: str) -> str:
    """
    Call Gemini and return raw text response.
    
    Args:
        prompt (str): The prompt to send to the LLM
        
    Returns:
        str: The LLM's response as text
        
    Raises:
        RuntimeError: If API key is not set
    """
    if not _model:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. \n"
            "1. Go to https://aistudio.google.com/app/apikey\n"
            "2. Create an API key\n"
            "3. Add it to your .env file: GEMINI_API_KEY=your_key\n"
            "4. Try again"
        )
    
    response = _model.generate_content(prompt)
    return response.text.strip()


def generate_json(prompt: str) -> dict:
    """
    Call Gemini expecting JSON back.
    Safely parses JSON even if the model wraps it in ```json fences.
    
    Args:
        prompt (str): The prompt to send (should ask for JSON output)
        
    Returns:
        dict: Parsed JSON response
        
    Raises:
        ValueError: If the model didn't return valid JSON
    """
    raw = generate_text(prompt)
    
    # Sometimes the model returns ```json code fences even when told not to
    # Strip them out
    cleaned = re.sub(r"^```json\n|^```\n|```$", "", raw.strip(), flags=re.MULTILINE)
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Model did not return valid JSON. Raw output:\n{raw}"
        ) from e


# Test function (we'll run this in Step 2.5)
if __name__ == "__main__":
    # This only runs if you do: python services/llm_service.py
    print("Testing Gemini API connection...")
    try:
        response = generate_text("Say 'Hello from Gemini!' and nothing else.")
        print(f"✓ Success! Response: {response}")
    except Exception as e:
        print(f"✗ Error: {e}")