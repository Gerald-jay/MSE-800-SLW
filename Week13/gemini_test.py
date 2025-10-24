# gemini_itinerary_cli.py
from google import genai
import os
from typing import List, Optional, Any

# 设置密钥
os.environ["GOOGLE_API_KEY"] = ""

# 创建客户端
client = genai.Client()

def _extract_text(resp: Any) -> Optional[str]:
    """
    兼容不同版本 google-genai 返回结构的安全取文方法。
    优先尝试便捷字段，然后回退到 candidates -> content.parts[].text。
    """
    # 一些版本有便捷属性 / Some versions have convenient attributes
    for attr in ("output_text", "text"):
        if hasattr(resp, attr):
            val = getattr(resp, attr)
            if val:
                return val

    # 通用结构 / General structure
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
