import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def get_job_description_summary(text):
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not set in environment.")
    # Put your actual API logic here
    return f"[Mocked Summary] {text[:200]}..."
def score_resume(resume_text, jd_summary):
    if not GEMINI_API_KEY:
        raise ValueError("❌ GEMINI_API_KEY not set in environment.")
    
    # Example simple scoring logic
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_summary.lower().split())
    common = resume_words.intersection(jd_words)
    score = len(common) / len(jd_words) * 100  # percentage match
    return f"Match Score: {score:.2f}%"
