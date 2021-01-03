import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
PORT = 587

SENDER_EMAIL = "iot.ca1.emailbot@gmail.com"
PASSWORD = "1234qwer$#@!"


def send_mail(message_text, receiver_email):
    message = MIMEMultipart()
    context = ssl.create_default_context()
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email
    message["Subject"] = "Indoor Climate Monitoring System Notification"
    message.attach(MIMEText(message_text, "plain"))

    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())

    




