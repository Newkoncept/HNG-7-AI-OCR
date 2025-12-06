# llm_client.py
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "gpt-4o-mini")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


async def analyze_document_text(text: str) -> dict:
    """
    Call OpenRouter and return a dict like:
    {
      "summary": "...",
      "doc_type": "...",
      "attributes": {...}
    }
    """
    # You can truncate if text is huge to avoid token limits
    truncated_text = text[:20_000]  # naive; improve later if needed

    prompt = f"""
You are a document analyzer for a web app.

Given the following document text, return:
1. A concise summary (2-4 sentences).
2. A high-level document type (e.g. "invoice", "resume", "contract", "report", "other").
3. A JSON object of useful attributes you can infer (e.g. parties, dates, amounts).

Return your answer as strict JSON with keys:
- summary: string
- doc_type: string
- attributes: object

Document text:
\"\"\"{truncated_text}\"\"\"
    """.strip()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://your-app-url.example",
        "X-Title": "HNG-7-Siftline Analyzer",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You respond ONLY with valid JSON."},
            {"role": "user", "content": prompt},
        ],
        "response_format": {"type": "json_object"},
    }

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(BASE_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]

    import json
    return json.loads(content)
