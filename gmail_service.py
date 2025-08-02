import os
import base64
from email.mime.text import MIMEText
from typing import List, Dict, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

class GmailService:
    def __init__(self):
        self.service = None

    def authenticate(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('gmail', 'v1', credentials=creds)

    def get_unread_emails(self, max_results=5) -> List[Dict]:
        if not self.service:
            self.authenticate()
        results = self.service.users().messages().list(
            userId='me', labelIds=['UNREAD'], maxResults=max_results
        ).execute()
        messages = results.get('messages', [])
        emails = []
        for message in messages:
            msg = self.service.users().messages().get(
                userId='me', id=message['id'], format='full'
            ).execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            body = self._extract_body(msg['payload'])
            emails.append({
                'id': msg['id'],
                'thread_id': msg['threadId'],
                'subject': subject,
                'sender': sender,
                'body': body,
            })
        return emails

    def _extract_body(self, payload) -> str:
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
        return ""

    def send_email(self, to: str, subject: str, body: str, thread_id: Optional[str] = None) -> bool:
        if not self.service:
            self.authenticate()
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        request_body = {'raw': raw_message}
        if thread_id:
            request_body['threadId'] = thread_id
        sent_message = self.service.users().messages().send(
            userId='me', body=request_body
        ).execute()
        print(f"Email sent! Message ID: {sent_message['id']}")
        return True

    def mark_as_read(self, message_id: str) -> bool:
        if not self.service:
            self.authenticate()
        self.service.users().messages().modify(
            userId='me', id=message_id, body={'removeLabelIds': ['UNREAD']}
        ).execute()
        return True 