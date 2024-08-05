import os
import json
import base64
import google.auth
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set the scope for the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Path to the credentials file
CREDENTIALS_PATH = 'credentials.json'
TOKEN_PATH = 'token.json'


def get_service():
    creds = None
    # Load credentials from file
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'r') as token_file:
            creds = service_account.Credentials.from_authorized_user_file(
                TOKEN_PATH, SCOPES)
    # If no valid credentials are available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, message_text):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    msg = MIMEText(message_text)
    message.attach(msg)
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(
            userId=user_id, body=message).execute()
        print(f'Message Id: {sent_message["id"]}')
        return sent_message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None


def send_activation_email(to_email, activation_link):
    service = get_service()
    sender_email = 'your-email@gmail.com'
    subject = 'Activate Your Account'
    message_text = f'Please click the following link to activate your account: {
        activation_link}'
    message = create_message(sender_email, to_email, subject, message_text)
    send_message(service, 'me', message)


if __name__ == '__main__':
    to_email = 'recipient@example.com'
    activation_link = 'https://example.com/activate?token=your-token'
    send_activation_email(to_email, activation_link)
