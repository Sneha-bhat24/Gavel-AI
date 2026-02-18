import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_text(prompt: str) -> str:
    """
    Direct Gemini call (same API as preprocessing).
    Reliable and supports newest models.
    """

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2
        }
    )

    return response.text
