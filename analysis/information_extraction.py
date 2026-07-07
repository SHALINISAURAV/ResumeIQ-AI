"""Rule-based information extraction for resume text."""

from __future__ import annotations

import re


COMMON_SKILLS = [
    "python",
    "sql",
    "machine learning",
    "deep learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "nlp",
    "computer vision",
    "streamlit",
    "flask",
    "django",
    "fastapi",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "gcp",
    "excel",
    "power bi",
    "tableau",
    "statistics",
    "java",
    "javascript",
    "html",
    "css",
]

SECTION_HEADINGS = [
    "summary",
    "objective",
    "skills",
    "technical skills",
    "education",
    "experience",
    "work experience",
    "professional experience",
    "projects",
    "certifications",
    "achievements",
]


def extract_email(text: str) -> str | None:
    """Extract the first email address found in resume text."""
    match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> str | None:
    """Extract a likely phone number from resume text."""
    pattern = r"(\+?\d[\d\s().-]{8,}\d)"
    match = re.search(pattern, text)
    return match.group(0).strip() if match else None


def extract_name(text: str) -> str | None:
    """Estimate the candidate name from the first useful resume line."""
    for line in text.splitlines()[:8]:
        clean_line = line.strip()

        if not clean_line:
            continue

        lower_line = clean_line.lower()
        if "@" in clean_line or "resume" in lower_line or "curriculum" in lower_line:
            continue

        if any(char.isdigit() for char in clean_line):
            continue

        words = clean_line.split()
        if 2 <= len(words) <= 4:
            return clean_line

    return None


def extract_skills(text: str) -> list[str]:
    """Find known technical skills mentioned in resume text."""
    normalized_text = text.lower()
    found_skills = []

    for skill in COMMON_SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"
        if re.search(pattern, normalized_text):
            found_skills.append(skill.title())

    return found_skills


def extract_section(text: str, possible_headings: list[str]) -> str | None:
    """Extract a rough text block for one resume section."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    start_index = None
    for index, line in enumerate(lines):
        line_key = line.lower().rstrip(":")
        if line_key in possible_headings:
            start_index = index + 1
            break

    if start_index is None:
        return None

    section_lines = []
    for line in lines[start_index:]:
        line_key = line.lower().rstrip(":")
        if line_key in SECTION_HEADINGS:
            break
        section_lines.append(line)

    section_text = "\n".join(section_lines).strip()
    return section_text if section_text else None


def extract_resume_information(text: str) -> dict[str, object]:
    """Extract important resume information into a structured dictionary."""
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_section(text, ["education"]),
        "experience": extract_section(
            text,
            ["experience", "work experience", "professional experience"],
        ),
        "projects": extract_section(text, ["projects"]),
    }
