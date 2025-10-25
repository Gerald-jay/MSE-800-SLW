import argparse
from pathlib import Path
from typing import Optional
from pypdf import PdfReader
from docx import Document
from model_client import generate_text
import textwrap


PROMPTS_DIR = Path(__file__).parent / "prompts"

def read_pdf(path: Path) -> str:
    text_parts = []
    with open(path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts).strip()

def read_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)

def read_txt(path: Path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="ignore")

def load_prompt_template() -> str:
    return (PROMPTS_DIR / "analyst_prompt.md").read_text(encoding="utf-8")

def load_system_preamble() -> str:
    return (PROMPTS_DIR / "system_preamble.md").read_text(encoding="utf-8")

def build_prompt(cv_text: str, job_desc: Optional[str], target_role: Optional[str]) -> str:
    system = load_system_preamble()
    tmpl = load_prompt_template()
    return textwrap.dedent(f"""
{system}

{tmpl}
""").format(
        target_role=target_role or "(not specified)",
        job_desc=job_desc or "(not provided)",
        cv_text=cv_text
    )

def detect_reader(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".docx":
        return "docx"
    return "txt"

def read_cv(path: Path) -> str:
    kind = detect_reader(path)
    if kind == "pdf":
        return read_pdf(path)
    if kind == "docx":
        return read_docx(path)
    return read_txt(path)

def main():
    ap = argparse.ArgumentParser(description="Analyze your CV using Gemini.")
    ap.add_argument("--cv", required=True, type=Path, help="Path to CV file (.pdf/.docx/.txt)")
    ap.add_argument("--job", type=Path, default=None, help="Optional job description text file")
    ap.add_argument("--target", type=str, default=None, help="Optional target role (e.g., 'Backend Engineer | Python')")
    ap.add_argument("--model", type=str, default="gemini-2.0-flash", help="Gemini model name")
    ap.add_argument("--temp", type=float, default=0.2, help="Sampling temperature")
    ap.add_argument("--max_tokens", type=int, default=1800, help="Max output tokens")
    ap.add_argument("--out", type=Path, default=Path("cv_report.md"), help="Output Markdown report path")

    args = ap.parse_args()

    cv_text = read_cv(args.cv)
    jd_text = read_txt(args.job) if args.job else None

    prompt = build_prompt(cv_text=cv_text, job_desc=jd_text, target_role=args.target)

    print("Analyzing with Gemini...")
    result_md = generate_text(contents=prompt, model=args.model, temperature=args.temp, max_tokens=args.max_tokens)

    # Save report
    args.out.write_text(result_md, encoding="utf-8")
    print(f"\nSaved report to: {args.out.resolve()}")

    # Print a short teaser to console (first 40 lines)
    teaser = "\n".join(result_md.splitlines()[:40])
    print("\n----- Preview -----\n")
    print(teaser)
    print("\n(Full report saved above)")

if __name__ == "__main__":
    main()
