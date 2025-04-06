from flask import Flask, request, render_template
import os
import re
from werkzeug.utils import secure_filename
from agents import recruiter
import fitz  # PyMuPDF
from dotenv import load_dotenv
from agents.summarizer_jd import JobDescriptionSummarizer
from utils import gemini_api
from utils.email_utils import send_selection_email

# Load environment variables
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs('uploads', exist_ok=True)

def extract_text(file_path):
    """Extract text from PDF or TXT files."""
    if file_path.endswith('.pdf'):
        try:
            with fitz.open(file_path) as doc:
                return "\n".join([page.get_text() for page in doc])
        except Exception as e:
            return f"❌ Error reading PDF: {e}"
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"❌ Error reading TXT: {e}"
    else:
        return "❌ Unsupported file format."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_file = request.files.get('resume')
        jd_text = request.form.get('job_description_text')
        candidate_email = request.form.get('candidate_email')
        candidate_name = request.form.get('candidate_name')

        if resume_file and resume_file.filename.endswith('.pdf') and jd_text.strip():
            resume_path = os.path.join(UPLOAD_FOLDER, secure_filename(resume_file.filename))
            resume_file.save(resume_path)

            resume_text = extract_text(resume_path)

            summarizer = JobDescriptionSummarizer(gemini_api)
            jd_summary = summarizer.summarize(jd_text)

            score_output = recruiter.score_resume(resume_text, jd_summary)

            try:
                # Extract the numeric score using regex
                match = re.search(r"([\d.]+)", score_output)
                if match:
                    score_value = float(match.group(1))
                    if score_value >= 70:
                        send_selection_email(candidate_email, candidate_name, score_value)
                    else:
                        send_selection_email(candidate_email, candidate_name, score_value)
                else:
                    print("⚠️ Could not extract score value from:", score_output)
            except Exception as e:
                print("⚠️ Email sending failed or score not valid:", e)

            return render_template('index.html', score=score_output)

        return render_template('index.html', score="❌ Please upload a PDF resume and enter a job description.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
