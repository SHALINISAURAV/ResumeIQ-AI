"""Rule-based resume improvement suggestions."""

from __future__ import annotations


def generate_resume_suggestions(
    resume_info: dict[str, object],
    resume_text: str,
    skill_gap: dict[str, object],
    ats_result: dict[str, object],
) -> list[str]:
    """Generate practical suggestions based on resume analysis results."""
    suggestions = []
    lower_text = resume_text.lower()
    skills = resume_info.get("skills") or []
    missing_skills = skill_gap.get("missing_skills") or []
    word_count = len(resume_text.split())
    ats_score = int(ats_result.get("score", 0))

    if "linkedin.com" not in lower_text:
        suggestions.append("Add a LinkedIn profile link near your contact details.")

    if "github.com" not in lower_text and "github" not in lower_text:
        suggestions.append("Add a GitHub link to showcase your code and projects.")

    if not resume_info.get("email"):
        suggestions.append("Add a professional email address.")

    if not resume_info.get("phone"):
        suggestions.append("Add a phone number so recruiters can contact you easily.")

    if len(skills) < 5:
        suggestions.append("Add more technical skills that match your target role.")

    if not resume_info.get("projects"):
        suggestions.append("Add a Projects section with 2-3 relevant portfolio projects.")

    if not resume_info.get("experience"):
        suggestions.append(
            "Add an Experience section with internships, freelance work, or practical training."
        )

    if "summary" not in lower_text and "objective" not in lower_text:
        suggestions.append("Add a short professional summary at the top of your resume.")

    if "certification" not in lower_text and "certifications" not in lower_text:
        suggestions.append("Add relevant certifications if you have completed any.")

    if missing_skills:
        top_missing = ", ".join(missing_skills[:3])
        suggestions.append(f"Learn or highlight these role-specific skills: {top_missing}.")

    if word_count < 250:
        suggestions.append("Add more detail to your resume. Aim for at least 250 words.")

    if ats_score < 70:
        suggestions.append("Improve missing ATS sections to raise your resume completeness score.")

    if not suggestions:
        suggestions.append(
            "Your resume covers the main basics. Focus next on stronger impact metrics."
        )

    return suggestions
