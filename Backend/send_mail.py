import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"  # Replace with your provider's SMTP server
SMTP_PORT = 587                 # Standard port for STARTTLS Secure connection
SENDER_EMAIL = os.getenv("SENDER_EMAIL") 
SENDER_PASSWORD = os.getenv("PASS")  # Use an App Password, NOT your regular password

user_mails = {"kiran":"ckkiran94@gmail.com",
              "pavan":"pavanbushetti@gmail.com",
              "shreekant" : "shreekanthallakar@gmail.com"}

def send_mail(username,msg):
    print(f"{username} {msg.name} {msg.email} {msg.message}")
    mail = EmailMessage()
    mail["From"] = SENDER_EMAIL
    mail["To"] = user_mails[username]
    mail["Subject"] = "portfolio connect"
    mail.set_content(f"connect request \n\n From : {msg.name}\n email : {msg.email} \n message : {msg.message} \n\n Thank you ")

    try:
        # Use context manager to automatically close the connection when done
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to secure encrypted TLS
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(mail)
            
        print("Email sent successfully!")

    except Exception as e:
        print(f" Failed to send email. Error: {e}")