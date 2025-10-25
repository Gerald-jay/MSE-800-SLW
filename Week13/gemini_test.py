# gemini_itinerary_cli.py
from google import genai
import os
from typing import List, Optional, Any

# Set API key
os.environ["GOOGLE_API_KEY"] = ""

def _extract_text(resp: Any) -> Optional[str]:
    """
    Compatible method for extracting text from different versions of google-genai response structures.
    Try convenient attributes first, then fallback to candidates -> content.parts[].text.
    """
    # Some versions have convenient attributes
    for attr in ("output_text", "text"):
        if hasattr(resp, attr):
            val = getattr(resp, attr)
            if val:
                return val

    # General structure
    candidates: List = getattr(resp, "candidates", None) or []
    for c in candidates:
        content = getattr(c, "content", None)
        parts = getattr(content, "parts", None) if content else None
        if parts:
            for p in parts:
                t = getattr(p, "text", None)
                if t:
                    return t
    return None


def instructor_chatbot_gemini():
    print("Welcome to AI Itinerary recommender! Answer a few questions to get personalized itinerary advice.\n")

    days = input("How many (days): ")
    location = input("Where is the destination (city name): ")
    age = input("Enter your age: ")

    prompt = f"""
You are a professional tourist recommender. Provide an itinerary recommendation based on user data.

User Details:
- days: {days} days
- destination: {location} city
- Age: {age} years

Based on the personal information,
give a structured itinerary with a name of the place, address and a short description for each day separately,
in order, with maximum three activities in a day.
"""

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "temperature": 0.7,
            "max_output_tokens": 800,
        }
    )

    print("\nMy Name is Hadi as AI Itinerary expert:")
    print(response.text)


if __name__ == "__main__":
    instructor_chatbot_gemini()
