# ResumeIQ AI

ResumeIQ AI is a beginner-friendly AI Resume Analyzer built with Python,
Streamlit, and open-source NLP libraries. Users can upload a PDF resume and get
resume insights, ATS scoring, skill gap analysis, job match scoring, and
rule-based improvement suggestions.

This project uses only free and open-source tools. It does not require API keys,
billing accounts, databases, Docker, or paid AI services.

## Features

- PDF resume upload
- Resume text extraction with PyMuPDF
- Information extraction for name, email, phone, skills, education, experience,
  and projects
- ATS score with a visual gauge chart
- Skill gap analysis for selected target roles
- Job match score using Sentence Transformers with a TF-IDF fallback
- Rule-based resume improvement suggestions
- Clean Streamlit interface

## Tech Stack

- Python
- Streamlit
- PyMuPDF
- spaCy
- Sentence Transformers
- scikit-learn
- Pandas
- NumPy
- Plotly

## Project Structure

```text
ResumeIQ AI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── assets/
│   └── screenshots/
├── components/
│   └── ui.py
├── data/
│   └── job_descriptions.py
├── parsers/
│   └── pdf_parser.py
├── analysis/
│   ├── ats_score.py
│   ├── information_extraction.py
│   ├── job_match.py
│   ├── skill_gap.py
│   └── suggestions.py
└── utils/
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## How It Works

1. The user uploads a PDF resume.
2. PyMuPDF extracts text from the PDF.
3. Rule-based logic extracts contact details, skills, and resume sections.
4. ATS scoring checks resume completeness.
5. Skill gap analysis compares resume skills with target-role skills.
6. Job match compares the resume with a predefined job description.
7. Rule-based suggestions recommend improvements.

## Target Roles

- AI Engineer
- Data Scientist
- Machine Learning Engineer
- Python Developer
- Data Analyst

## Screenshots

Add project screenshots here before publishing the portfolio project.

```text
assets/screenshots/home.png
assets/screenshots/analysis-results.png
assets/screenshots/skill-gap.png
```

## Deployment

This project is ready to deploy on platforms such as Streamlit Community Cloud,
Render, or Hugging Face Spaces.

For Streamlit Community Cloud:

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
app.py
```

5. Deploy the app.

The first run may take longer if Sentence Transformers downloads the local model.
If the model is unavailable, the app uses a TF-IDF fallback for job matching.

## Notes

- This project does not use OpenAI, Gemini, Claude, or any paid API.
- Scanned image PDFs are not supported because OCR is intentionally excluded to
  keep the app lightweight.
- The current extractor is rule-based, so it is explainable but not perfect.
- Skill and job description lists can be customized in the `analysis/` and
  `data/` folders.

## License

This project is intended for learning and portfolio use.
