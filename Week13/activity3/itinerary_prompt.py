# itinerary_prompt.py
from typing import Optional
from pathlib import Path
import argparse, os
from flask.cli import load_dotenv
from google import genai

load_dotenv()

# 读取 API Key：优先参数，其次环境变量
def get_client(api_key: Optional[str] = None) -> genai.Client:
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("Missing GOOGLE_API_KEY. Set env var or pass --api_key.")
    return genai.Client(api_key=key)

# 你的基础提示词（Activity 1 的业务流：基于天数/城市/年龄给每日≤3个活动，含名称/地址/描述）
BASE_PROMPT = """You are a professional itinerary recommender. Provide an itinerary recommendation based on user data.

User Details:
- days: {days} days
- destination: {city} city
- Age: {age} years

Output requirements:
- Give a structured itinerary day by day.
- Each day has maximum three activities.
- For each activity include: place name, address, and a short description.
"""

# 正向（positive）约束：明确“要做什么/更偏好什么”
POSITIVE_GUIDANCE = """Style & policy (positive):
- Prioritize free/low-cost highlights, local markets, and public viewpoints.
- Prefer walkable clusters; minimize backtracking.
- Include realistic opening-hour hints if typical (e.g., “arrive before 10:00 to avoid queues”).
- Balance culture, nature, and food; keep language concise and practical.
"""

# 反向（negative）约束：明确“不要什么/避免什么”
NEGATIVE_CONSTRAINTS = """Constraints (negative):
- Do NOT include more than three activities per day.
- Avoid unsafe or illegal activities.
- Avoid vague addresses like “near downtown”; give concrete street or landmark addresses when possible.
- Avoid generic filler like “explore the city” without specifics.
"""

def build_prompt(days: int, city: str, age: int, mode: str) -> str:
    base = BASE_PROMPT.format(days=days, city=city, age=age)
    if mode == "positive":
        return f"{base}\n{POSITIVE_GUIDANCE}\n{NEGATIVE_CONSTRAINTS}\nRespond in English."
    elif mode == "negative":
        # 反向示例：强调要避免的内容+给出最小化输出要求
        return f"""{base}
Only return an itinerary that strictly avoids:
- more than three activities/day
- unsafe/illegal content
- vague addresses
Keep each activity specific and useful. Respond in English."""
    else:
        raise ValueError("mode must be 'positive' or 'negative'.")

def run_once(client: genai.Client, model: str, prompt: str) -> str:
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"temperature": 0.5, "max_output_tokens": 1200}
    )
    return resp.text or ""

def main():
    ap = argparse.ArgumentParser(description="Run positive vs negative prompt itineraries with Gemini.")
    ap.add_argument("--days", type=int, required=True)
    ap.add_argument("--city", type=str, required=True)
    ap.add_argument("--age", type=int, required=True)
    ap.add_argument("--model", type=str, default="gemini-2.0-flash")
    ap.add_argument("--api_key", type=str, default=None)
    ap.add_argument("--outdir", type=Path, default=Path("outputs"))
    args = ap.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    client = get_client(api_key=args.api_key)

    # Positive prompt
    pos_prompt = build_prompt(args.days, args.city, args.age, mode="positive")
    pos_text = run_once(client, args.model, pos_prompt)
    (args.outdir / "itinerary_positive.md").write_text(pos_text, encoding="utf-8")
    print("\n=== Positive Prompt Result (saved to outputs/itinerary_positive.md) ===\n")
    print("\n".join(pos_text.splitlines()[:40]))

    # Negative prompt
    neg_prompt = build_prompt(args.days, args.city, args.age, mode="negative")
    neg_text = run_once(client, args.model, neg_prompt)
    (args.outdir / "itinerary_negative.md").write_text(neg_text, encoding="utf-8")
    print("\n=== Negative Prompt Result (saved to outputs/itinerary_negative.md) ===\n")
    print("\n".join(neg_text.splitlines()[:40]))

    # 同步把两个实际提示词也存档，便于作业提交展示
    (args.outdir / "prompt_positive.txt").write_text(pos_prompt, encoding="utf-8")
    (args.outdir / "prompt_negative.txt").write_text(neg_prompt, encoding="utf-8")

if __name__ == "__main__":
    main()
