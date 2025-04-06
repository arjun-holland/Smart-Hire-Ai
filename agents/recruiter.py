from utils.gemini_api import score_resume

# recruiter.py
def score_resume(resume_text, jd_summary):
    # Example simple scoring logic
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_summary.lower().split())
    common = resume_words.intersection(jd_words)
    score = len(common) / len(jd_words) * 100  # percentage match
    return f"Match Score: {score:.2f}%"
