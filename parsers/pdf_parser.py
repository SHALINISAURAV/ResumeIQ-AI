"""PDF parsing utilities for ResumeIQ AI."""

from __future__ import annotations

import fitz


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract plain text from a PDF file represented as bytes.

    Streamlit uploaded files live in memory, so this function accepts bytes
    instead of a file path. That keeps it useful for local apps and deployment.
    """
    if not pdf_bytes:
        raise ValueError("The uploaded PDF file is empty.")

    text_parts: list[str] = []

    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
            for page in document:
                page_text = page.get_text("text")
                if page_text:
                    text_parts.append(page_text)
    except Exception as exc:
        raise ValueError("Could not read text from the uploaded PDF.") from exc

    extracted_text = "\n".join(text_parts).strip()

    if not extracted_text:
        raise ValueError(
            "No readable text was found. This may be a scanned resume image."
        )

    return extracted_text


def get_text_stats(text: str) -> dict[str, int]:
    """Return simple statistics for extracted resume text."""
    words = text.split()
    lines = [line for line in text.splitlines() if line.strip()]

    return {
        "characters": len(text),
        "words": len(words),
        "lines": len(lines),
    }
