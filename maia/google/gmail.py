"""This module handles gmail api interactions."""

import base64
import logging
from email.message import EmailMessage

import googleapiclient.discovery
from googleapiclient.errors import HttpError

from settings import G_CREDENTIALS

def get_emails(unread_only: bool = False):
    """Get emails from gmail inbox, return list of emails."""
    service = googleapiclient.discovery.build('gmail', 'v1', credentials=G_CREDENTIALS)

    kwargs = {
        "maxResults": 5,
        "labelIds": ['INBOX', 'CATEGORY_PERSONAL'],
        "includeSpamTrash": False,
        "q": "is:unread" if unread_only else ""
    }

    results = service.users().messages().list(userId="me", **kwargs).execute()
    messages = results.get('messages', [])

    logging.info("Got %d messages, now retrieving content.", len(messages))

    emails = []

    # Stitch together object with only necessary fields
    for message in messages:
        result = service.users().messages().get(userId="me", id=message['id'], format="full").execute()

        payload = result['payload']
        payload = {key: value for key, value in payload.items() if key in ["headers"]}
        headers = payload['headers']

        filtered_headers = [header for header in headers if header['name'] in ['From', 'To', 'Subject']]
        payload['headers'] = filtered_headers

        fields_to_keep = ['id', 'snippet', 'internalDate', 'labelIds', 'payload']
        result = {key: value for key, value in result.items() if key in fields_to_keep}
        result['payload'] = payload

        emails.append(result)

    logging.info("Retrieved %d emails.", len(emails))
    return emails

def get_emails_llm(unread_only: bool = False):
    """Wrapper function for get_emails which is called by llm."""
    return get_emails(unread_only)

def create_draft(to: str, subject: str, content: str):
    """Create email draft message with given content, subject and recipient."""
    logging.info("Creating draft with subject %s for sending to %s.", subject, to)
    logging.debug("Content: %s", content)

    try:
        service = googleapiclient.discovery.build('gmail', 'v1', credentials=G_CREDENTIALS)
        message = {"message": {"raw": _create_message(to, subject, content)}}
        draft = (
            service.users().drafts().create(userId="me", body=message).execute()
        )

    except HttpError as error:
        logging.error(error)
        return "There as an error creating the email draft."

    return draft

def create_and_send(to: str, subject: str, content: str):
    """Create and directly send an email."""
    logging.info("Send email with subject %s for sending to %s.", subject, to)
    logging.debug("Content: %s", content)

    try:
        service = googleapiclient.discovery.build('gmail', 'v1', credentials=G_CREDENTIALS)
        message = {"raw": _create_message(to, subject, content)}
        send_message = (
            service.users().messages().send(userId="me", body=message).execute()
        )

    except HttpError as error:
        logging.error(error)
        return "There as an error sending the email."

    return send_message

def _create_message(to: str, subject: str, content: str) -> str:
    """Create email message with given content, subject and recipient."""
    logging.info("Creating message with subject %s for sending to %s.", subject, to)

    message = EmailMessage()
    message.set_content(content)
    message['Subject'] = subject
    message['From'] = 'me'
    message['To'] = to

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return encoded_message