import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_selection_email(to_email, name, score):
    sender_email = "arjunholland116@gmail.com"  # replace with your email
    sender_password = "ylzz bqrc tsav fiez"  # use app password if Gmail

    subject = "Your Resume Evaluation Result"

    if score >= 70:
        message = f"Hi {name},\n\nCongratulations! You have been selected based on your resume score of {score}%.\n We will share the interview details with out delay.\nBest regards,\nSmartHire Team"
    else:
        message = f"Hi {name},\n\nThank you for applying. Unfortunately, your resume score of {score}% did not meet the selection criteria.\n\nBest wishes,\nSmartHire Team"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
