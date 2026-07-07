"""Job match scoring using resume and job description similarity."""

from __future__ import annotations

from data.job_descriptions import JOB_DESCRIPTIONS


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def calculate_job_match(resume_text: str, target_role: str) -> dict[str, object]:
    """Compare resume text with a predefined job description."""
    job_description = JOB_DESCRIPTIONS.get(target_role, "")

    if not job_description:
        return {
            "target_role": target_role,
            "score": 0,
            "method": "No job description found",
            "job_description": "",
        }

    try:
        score = _calculate_sentence_transformer_score(resume_text, job_description)
        method = "Sentence Transformers"
    except Exception:
        score = _calculate_tfidf_score(resume_text, job_description)
        method = "TF-IDF fallback"

    return {
        "target_role": target_role,
        "score": score,
        "method": method,
        "job_description": job_description.strip(),
    }


def _calculate_sentence_transformer_score(
    resume_text: str,
    job_description: str,
) -> int:
    """Calculate semantic similarity using a local Sentence Transformer model."""
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity

    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode([resume_text, job_description])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    return _similarity_to_percentage(similarity)


def _calculate_tfidf_score(resume_text: str, job_description: str) -> int:
    """Calculate text similarity using TF-IDF when the model is unavailable."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform([resume_text, job_description])
    similarity = cosine_similarity(matrix[0], matrix[1])[0][0]

    return _similarity_to_percentage(similarity)


def _similarity_to_percentage(similarity: float) -> int:
    """Convert a similarity value between 0 and 1 into a percentage."""
    bounded_similarity = max(0.0, min(float(similarity), 1.0))
    return round(bounded_similarity * 100)
