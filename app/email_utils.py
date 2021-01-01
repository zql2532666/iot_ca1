import smtplib, ssl
from time import sleep
import database_utils

# variables for MYSQL Database connection 
HOST = "localhost"
USER = "root"
PASSWORD = "root"
DATABASE = "iot_ca1"

SMTP_SERVER = "smtp.gmail.com"
PORT = 587

SENDER_EMAIL = "iot.ca1.emailbot@gmail.com"
PASSWORD = "1234qwer$#@!"

mysql_connection, mysql_cursor = database_utils.get_mysql_connection(HOST, USER, PASSWORD, DATABASE)
receiver_email = database_utils.get_user_info(mysql_cursor)['email']
mysql_connection.close()
print(receiver_email)

def send_mail(message):
    context = ssl.create_default_context()

    with smtplib.SMTP(SMTP_SERVER, PORT) as server:
        server.starttls(context=context)
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message)

    




