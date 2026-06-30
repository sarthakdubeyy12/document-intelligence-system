"""Standalone end-to-end check for prompt construction and LLM inference.

Run from the backend/ directory:

    python scripts/verify_llm.py

Requires ANTHROPIC_API_KEY in backend/.env (never committed). This script is for
manual verification only and is intentionally separate from the application flow.
"""

import sys
from pathlib import Path

from dotenv import load_dotenv

# Allow running directly (`python scripts/verify_llm.py`) by putting backend/ on the path.
BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.services.llm_service import build_prompt, generate_answer  # noqa: E402
from app.services.retrieval_service import RetrievedChunk  # noqa: E402

SAMPLE_QUERY = "How many paid vacation days do full-time employees get?"
SAMPLE_CHUNKS = [
    RetrievedChunk(
        chunk_id="handbook.pdf-p2-0",
        filename="handbook.pdf",
        page_number=2,
        text="Full-time employees accrue 20 days of paid vacation per year.",
        score=0.83,
    ),
]


def main() -> None:
    load_dotenv(BACKEND_DIR / ".env")
    prompt = build_prompt(SAMPLE_QUERY, SAMPLE_CHUNKS)

    try:
        answer = generate_answer(prompt)
    except Exception as exc:  # noqa: BLE001 - surface any failure to the operator
        print("API call: FAILED")
        print(f"Error: {type(exc).__name__}: {exc}")
        sys.exit(1)

    print("API call: SUCCESS")
    print("\nGenerated answer:")
    print(answer)


if __name__ == "__main__":
    main()
