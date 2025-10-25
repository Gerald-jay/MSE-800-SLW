from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

DEFAULT_MODEL = "gemini-2.0-flash"

def get_client(api_key: Optional[str] = None) -> genai.Client:
    # 如果函数没有传入，就从环境变量里取 / if not provided, get from environment variable
    api_key = api_key or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("❌ Missing GOOGLE_API_KEY. Please set it in .env or environment variables.")

    return genai.Client(api_key=api_key)

def generate_text(contents: str, model: str = DEFAULT_MODEL, temperature: float = 0.2, max_tokens: int = 1800) -> str:
    client = get_client()
    resp = client.models.generate_content(
        model=model,
        contents=contents,
        config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    # SDK v1.46+ exposes .text
    return getattr(resp, "text", None) or ""
