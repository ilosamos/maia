"""Google People API functions."""
import logging

import googleapiclient
from googleapiclient.errors import HttpError

from settings import G_CREDENTIALS


def list_contacts():
    """List the users contacts."""
    logging.info("List users contacts")

    try:
        service = googleapiclient.discovery.build('people', 'v1', credentials=G_CREDENTIALS)
        contacts = (
            service.people().connections().list(resourceName="people/me", personFields="names,emailAddresses").execute()
        )

    except HttpError as error:
        logging.error(error)
        return "There as an error listing the users contacts."

    return contacts

def search_contacts(query: str):
    """Search the users contacts."""
    logging.info("Search users contacts")

    try:
        service = googleapiclient.discovery.build('people', 'v1', credentials=G_CREDENTIALS)
        contacts = (
            service.people().searchContacts(query=query, readMask="names,emailAddresses").execute()
        )

    except HttpError as error:
        logging.error(error)
        return "There as an error searching the users contacts."

    return contacts
