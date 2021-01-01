import smtplib, ssl
from time import sleep
import database_utils
import app


SMTP_SERVER = "smtp.gmail.com"
PORT = 587

SENDER_EMAIL = "iot.ca1.emailbot@gmail.com"
PASSWORD = "1234qwer$#@!"

mysql_connection, mysql_cursor = database_utils.get_mysql_connection(app.HOST, app.USER, app.PASSWORD, app.DATABASE)
receiver_email = database_utils.get_user_info(mysql_cursor)['email']
mysql_connection.close()
print(receiver_email)

def send_mail(message):
    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message)

    




