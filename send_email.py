"""

The entire purpose of this file is to format and send emails.

"""


from datetime import date
import smtplib
from email.message import EmailMessage
from credentials import *



def send_email(email_text):
    # construct email
    email = EmailMessage()
    email['Subject'] = f'Password Cracked -- {date.today().month}/{date.today().day}/{date.today().year}'

    email['From'] = gmail_api['email']
    email['To'] = receiving_email['email']
    email.set_content(email_text, subtype='html')

    # Send the message via local SMTP server.
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.ehlo()
        s.login(gmail_api['email'], gmail_api['password'])
        s.send_message(email)


def format_email(password_html):
    with open('utilities/email_message.html', 'r') as f:
        html_string = f.read()
        html_string = html_string.replace('<!-- THIS IS WHERE YOUR PASSWORDS GO -->', password_html)

        return html_string

