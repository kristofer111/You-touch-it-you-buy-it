# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

def send_email(message: Mail):

    try:
        load_dotenv()
        key = os.environ.get('SENDGRID_API_KEY')
        if not key:
            raise RuntimeError("SENDGRID_API_KEY not set")
        sg = SendGridAPIClient(key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)