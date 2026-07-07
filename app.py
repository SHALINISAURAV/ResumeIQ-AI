"""Main Streamlit application for ResumeIQ AI."""

import plotly.graph_objects as go
import streamlit as st

from analysis.ats_score import calculate_ats_score, get_ats_score_label
from analysis.information_extraction import extract_resume_information
from analysis.job_match import calculate_job_match
from analysis.skill_gap import analyze_skill_gap
from analysis.suggestions import generate_resume_suggestions
from components.ui import apply_custom_styles, render_section_divider, render_skill_pills
from parsers.pdf_parser import extract_text_from_pdf, get_text_stats


JOB_ROLES = [
    "AI Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Python Developer",
    "Data Analyst",
]


def configure_page() -> None:
    """Configure basic Streamlit page settings."""
    st.set_page_config(
        page_title="ResumeIQ AI",
        page_icon=":page_facing_up:",
        layout="wide",
    )


def render_sidebar() -> tuple[object, str, bool]:
    """Render sidebar controls and return user inputs."""
    st.sidebar.title("ResumeIQ AI")
    st.sidebar.caption("Free local resume analysis for portfolio projects.")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
        help="Only PDF files are supported in this project.",
    )

    selected_role = st.sidebar.selectbox(
        "Target Job Role",
        JOB_ROLES,
    )

    analyze_button = st.sidebar.button(
        "Analyze Resume",
        type="primary",
        use_container_width=True,
    )

    return uploaded_file, selected_role, analyze_button


def render_header() -> None:
    """Render the main app title and short description."""
    st.title("ResumeIQ AI")
    st.write(
        "An open-source AI resume analyzer that checks resume quality, "
        "skill gaps, and job match using local Python tools."
    )
    st.caption("No paid APIs. No API keys. Built with Python, Streamlit, and open-source NLP.")


def render_empty_state() -> None:
    """Render instructions shown before the user analyzes a resume."""
    st.info("Upload a PDF resume from the sidebar, choose a job role, and click Analyze Resume.")


def render_extracted_information(resume_info: dict[str, object]) -> None:
    """Render extracted resume information."""
    st.subheader("Extracted Information")

    contact_col_1, contact_col_2, contact_col_3 = st.columns(3)

    with contact_col_1:
        st.write("**Name**")
        st.write(resume_info["name"] or "Not found")

    with contact_col_2:
        st.write("**Email**")
        st.write(resume_info["email"] or "Not found")

    with contact_col_3:
        st.write("**Phone**")
        st.write(resume_info["phone"] or "Not found")

    skills = resume_info["skills"]
    st.write("**Skills**")
    if skills:
        render_skill_pills(skills)
    else:
        st.write("No known skills found yet.")

    info_tab_1, info_tab_2, info_tab_3 = st.tabs(
        ["Education", "Experience", "Projects"]
    )

    with info_tab_1:
        st.write(resume_info["education"] or "Education section not found.")

    with info_tab_2:
        st.write(resume_info["experience"] or "Experience section not found.")

    with info_tab_3:
        st.write(resume_info["projects"] or "Projects section not found.")


def render_ats_score(ats_result: dict[str, object]) -> None:
    """Render ATS score as a gauge chart and checklist."""
    score = int(ats_result["score"])
    score_label = get_ats_score_label(score)

    st.subheader("ATS Score")

    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%"},
            title={"text": score_label},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#dcfce7"},
                ],
            },
        )
    )
    figure.update_layout(height=260, margin={"t": 40, "b": 10, "l": 30, "r": 30})
    st.plotly_chart(figure, use_container_width=True)

    with st.expander("ATS Score Breakdown"):
        for item in ats_result["checks"]:
            status = "Passed" if item["passed"] else "Missing"
            st.write(
                f"**{status}:** {item['check']} "
                f"({item['earned']}/{item['points']} points)"
            )


def render_skill_gap(skill_gap: dict[str, object]) -> None:
    """Render matching and missing skills for the selected target role."""
    st.subheader("Skill Gap Analysis")
    st.metric(
        label=f"Skill Match for {skill_gap['target_role']}",
        value=f"{skill_gap['match_percentage']}%",
    )

    match_col, missing_col = st.columns(2)

    with match_col:
        st.write("**Matching Skills**")
        matching_skills = skill_gap["matching_skills"]
        if matching_skills:
            render_skill_pills(matching_skills)
        else:
            st.warning("No matching target-role skills found yet.")

    with missing_col:
        st.write("**Missing Skills**")
        missing_skills = skill_gap["missing_skills"]
        if missing_skills:
            st.error(", ".join(missing_skills))
        else:
            st.success("No missing skills for this role.")

    with st.expander("Required Skills for This Role"):
        st.write(", ".join(skill_gap["required_skills"]))


def render_job_match(job_match: dict[str, object]) -> None:
    """Render job match score and the description used for comparison."""
    st.subheader("Job Match")
    st.metric(
        label=f"Match for {job_match['target_role']}",
        value=f"{job_match['score']}%",
    )
    st.caption(f"Similarity method: {job_match['method']}")

    with st.expander("Job Description Used for Matching"):
        st.write(job_match["job_description"])


def render_suggestions(suggestions: list[str]) -> None:
    """Render resume improvement suggestions."""
    st.subheader("Resume Improvement Suggestions")

    for index, suggestion in enumerate(suggestions, start=1):
        st.info(f"{index}. {suggestion}")


def render_analysis_placeholders(
    selected_role: str,
    resume_text: str,
    resume_info: dict[str, object],
    ats_result: dict[str, object],
    skill_gap: dict[str, object],
    job_match: dict[str, object],
    suggestions: list[str],
) -> None:
    """Render placeholder sections for future resume analysis results."""
    render_section_divider()
    st.subheader("Resume Summary")
    text_stats = get_text_stats(resume_text)
    stat_col_1, stat_col_2, stat_col_3 = st.columns(3)

    with stat_col_1:
        st.metric("Characters", text_stats["characters"])

    with stat_col_2:
        st.metric("Words", text_stats["words"])

    with stat_col_3:
        st.metric("Text Lines", text_stats["lines"])

    with st.expander("Extracted Resume Text Preview"):
        st.text_area(
            "Raw text extracted from PDF",
            value=resume_text[:3000],
            height=300,
            disabled=True,
        )

    score_col, match_col = st.columns(2)

    with score_col:
        render_ats_score(ats_result)

    with match_col:
        render_job_match(job_match)

    render_section_divider()
    render_extracted_information(resume_info)

    render_section_divider()
    render_skill_gap(skill_gap)

    render_section_divider()
    render_suggestions(suggestions)


def main() -> None:
    """Run the Streamlit application."""
    configure_page()
    apply_custom_styles()
    uploaded_file, selected_role, analyze_button = render_sidebar()

    render_header()

    if analyze_button:
        if uploaded_file is None:
            st.warning("Please upload a PDF resume before analyzing.")
            return

        try:
            resume_text = extract_text_from_pdf(uploaded_file.getvalue())
        except ValueError as exc:
            st.error(str(exc))
            return

        resume_info = extract_resume_information(resume_text)
        ats_result = calculate_ats_score(resume_info, resume_text)
        skill_gap = analyze_skill_gap(resume_info["skills"], selected_role)
        job_match = calculate_job_match(resume_text, selected_role)
        suggestions = generate_resume_suggestions(
            resume_info,
            resume_text,
            skill_gap,
            ats_result,
        )
        render_analysis_placeholders(
            selected_role,
            resume_text,
            resume_info,
            ats_result,
            skill_gap,
            job_match,
            suggestions,
        )
        return

    render_empty_state()


if __name__ == "__main__":
    main()
