import smtplib, ssl


SMTP_SERVER = "smtp.gmail.com"
PORT = 587

SENDER_EMAIL = "iot.ca1.emailbot@gmail.com"
PASSWORD = "1234qwer$#@!"


def send_mail(message, receiver_email):
    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message)

    




