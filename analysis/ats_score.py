"""ATS scoring utilities for ResumeIQ AI."""

from __future__ import annotations


def calculate_ats_score(
    resume_info: dict[str, object],
    resume_text: str,
) -> dict[str, object]:
    """Calculate a simple ATS-style score from extracted resume information."""
    score = 0
    checks = []
    word_count = len(resume_text.split())
    skills = resume_info.get("skills") or []

    scoring_rules = [
        ("Name found", bool(resume_info.get("name")), 10),
        ("Email found", bool(resume_info.get("email")), 10),
        ("Phone number found", bool(resume_info.get("phone")), 10),
        ("At least 5 skills found", len(skills) >= 5, 20),
        ("Education section found", bool(resume_info.get("education")), 15),
        ("Experience section found", bool(resume_info.get("experience")), 15),
        ("Projects section found", bool(resume_info.get("projects")), 10),
        ("Resume has enough detail", word_count >= 250, 10),
    ]

    for label, passed, points in scoring_rules:
        earned = points if passed else 0
        score += earned
        checks.append(
            {
                "check": label,
                "points": points,
                "earned": earned,
                "passed": passed,
            }
        )

    return {
        "score": score,
        "checks": checks,
    }


def get_ats_score_label(score: int) -> str:
    """Return a human-friendly label for an ATS score."""
    if score >= 80:
        return "Strong"
    if score >= 60:
        return "Good"
    if score >= 40:
        return "Needs Work"
    return "Incomplete"
