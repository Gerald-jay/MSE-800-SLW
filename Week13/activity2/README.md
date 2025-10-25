# LLM CV Analyzer (Gemini)

Analyze a CV/resumé with Google's Gemini and get structured, personalized recommendations to improve alignment with tech-industry roles.

## Features
- Works with **PDF**, **DOCX**, or **plain text** CVs.
- Optional **job description** matching and **skills gap** analysis.
- Outputs a **Markdown report** and prints a concise summary to the console.
- Uses the **latest `google-genai` SDK (v1.46+)** via `config={...}`.
- Deterministic profile via configurable temperature/max tokens.

## Quickstart

1) **Install deps**
```bash
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -U google-genai pypdf python-docx
```

2) **Set your API key**
```bash
export GOOGLE_API_KEY="YOUR_KEY"      # Windows PowerShell: $env:GOOGLE_API_KEY="YOUR_KEY"
```

3) **Run**
```bash
python cv_analyzer.py --cv path/to/YourCV.pdf --job job_desc.txt --out report.md
# Or only analyze the CV:
python cv_analyzer.py --cv path/to/YourCV.docx --out report.md
```

4) **Result**
- A Markdown report will be saved to `--out` (default: `cv_report.md`).

## Project Layout
```
llm-cv-analyzer/
├─ cv_analyzer.py          # CLI entry
├─ model_client.py         # Gemini client helper
├─ prompts/
│  ├─ system_preamble.md   # System instruction
│  └─ analyst_prompt.md    # User prompt template (with placeholders)
├─ examples/
│  ├─ job_desc_sample.txt
│  └─ sample_cv.txt
├─ README.md
├─ requirements.txt
└─ .env.example
```

## Notes
- This tool keeps everything local except the text you send to the Gemini API.
- Remove sensitive data before running if desired (e.g., phone, address).

## License
MIT
