"""Skill gap analysis for target job roles."""

from __future__ import annotations


ROLE_SKILLS = {
    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Nlp",
        "Computer Vision",
        "Pytorch",
        "Tensorflow",
        "Fastapi",
        "Git",
        "Docker",
    ],
    "Data Scientist": [
        "Python",
        "Sql",
        "Machine Learning",
        "Data Analysis",
        "Pandas",
        "Numpy",
        "Scikit-Learn",
        "Statistics",
        "Tableau",
        "Power Bi",
    ],
    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Scikit-Learn",
        "Pytorch",
        "Tensorflow",
        "Fastapi",
        "Docker",
        "Aws",
        "Git",
    ],
    "Python Developer": [
        "Python",
        "Sql",
        "Flask",
        "Django",
        "Fastapi",
        "Git",
        "Github",
        "Docker",
        "Html",
        "Css",
    ],
    "Data Analyst": [
        "Sql",
        "Excel",
        "Python",
        "Data Analysis",
        "Pandas",
        "Numpy",
        "Statistics",
        "Tableau",
        "Power Bi",
        "Git",
    ],
}


def analyze_skill_gap(
    resume_skills: list[str],
    target_role: str,
) -> dict[str, object]:
    """Compare resume skills with skills required for a target role."""
    required_skills = ROLE_SKILLS.get(target_role, [])
    normalized_resume_skills = {skill.lower(): skill for skill in resume_skills}

    matching_skills = [
        skill for skill in required_skills if skill.lower() in normalized_resume_skills
    ]
    missing_skills = [
        skill for skill in required_skills if skill.lower() not in normalized_resume_skills
    ]

    match_percentage = 0
    if required_skills:
        match_percentage = round((len(matching_skills) / len(required_skills)) * 100)

    return {
        "target_role": target_role,
        "required_skills": required_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
    }
