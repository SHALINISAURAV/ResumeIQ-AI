"""Reusable Streamlit UI helpers for ResumeIQ AI."""

from __future__ import annotations

import streamlit as st


def apply_custom_styles() -> None:
    """Apply lightweight CSS for a cleaner Streamlit interface."""
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1180px;
        }

        h1 {
            color: #111827;
            font-weight: 800;
        }

        h2, h3 {
            color: #1f2937;
        }

        [data-testid="stMetric"] {
            background: #f8fafc;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
        }

        [data-testid="stSidebar"] {
            background: #f9fafb;
        }

        .resumeiq-section {
            border-top: 1px solid #e5e7eb;
            margin: 1.5rem 0 1rem 0;
            padding-top: 1.25rem;
        }

        .resumeiq-pill {
            display: inline-block;
            background: #eff6ff;
            color: #1d4ed8;
            border: 1px solid #bfdbfe;
            border-radius: 999px;
            padding: 0.2rem 0.65rem;
            margin: 0.15rem 0.2rem 0.15rem 0;
            font-size: 0.9rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section_divider() -> None:
    """Render a subtle divider between major app sections."""
    st.markdown('<div class="resumeiq-section"></div>', unsafe_allow_html=True)


def render_skill_pills(skills: list[str]) -> None:
    """Render a compact list of skills as visual pills."""
    if not skills:
        st.write("No skills to display.")
        return

    pills = "".join(f'<span class="resumeiq-pill">{skill}</span>' for skill in skills)
    st.markdown(pills, unsafe_allow_html=True)
