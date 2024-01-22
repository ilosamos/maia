"""Google Calendar API helper functions."""
import logging
from datetime import datetime, timedelta

import googleapiclient.discovery
from werkzeug.exceptions import BadRequest

from settings import G_CREDENTIALS


def get_calendars_llm():
    """Returns a list of calendars."""
    return get_calendars()

def get_calendars():
    """Returns a list of calendars."""
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=G_CREDENTIALS)

    # Retrieve the calendars from the API
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])

    return calendars

def get_events_llm(calendar_ids: list = None, **kwargs):
    """Returns a list of events for the given calendar_ids and additionsl kwargs."""
    if calendar_ids is None:
        calendar_ids = ["primary"]
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=G_CREDENTIALS)

    events = []

    for calendar_id in calendar_ids:
        # Retrieve the events from the calendar
        events_result = service.events().list(calendarId=calendar_id, **kwargs).execute()
        events = filter_events(events_result)

    return events

def get_events(calendar_ids: list = None):
    """Returns a list of events for the given calendar_ids."""
    if calendar_ids is None:
        calendar_ids = ["primary"]
    # Rest of the code...
    logging.info("Getting events from calendar ids %s", calendar_ids)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=G_CREDENTIALS)

    current_date = datetime.now()
    current_date = current_date.replace(hour=0, minute=0, second=0, microsecond=0)
    one_year_from_now = current_date + timedelta(days=365)

    # Define the start and end date/time for the events you want to retrieve
    start_date = current_date.isoformat() + 'Z'  # 'Z' indicates UTC time
    end_date = one_year_from_now.isoformat() + 'Z'  # 'Z' indicates UTC time

    logging.info("Getting events from %s to %s", start_date, end_date)

    events = []

    # Retrieve the events from the calendar
    for calendar_id in calendar_ids:
        events_result = service.events().list(calendarId=calendar_id, timeMin=start_date, timeMax=end_date).execute()
        events.extend(filter_events(events_result))
    return events

def filter_events(events_result: any) -> list:
    """Filters the events_result to only keep the fields that are needed."""
    events = []
    filtered_events = events_result.get('items', [])
    fields_to_keep = ['id', 'status', 'htmlLink', 'summary', 'start', 'end', 'location']
    filtered_events = [{key: value for key, value in event.items() if key in fields_to_keep} for event in filtered_events]
    events.extend(filtered_events)
    return events

def create_or_update_event(event: dict):
    """Creates or updates an event."""
    logging.info("Creating or updating event %s", event)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=G_CREDENTIALS)
    calendar_id = "primary"

    if 'calendarId' in event:
        calendar_id = event['calendarId']
        event.pop('calendarId')

    # Retrieve the events from the calendar
    try:
        if "id" in event:
            event = service.events().update(calendarId=calendar_id, eventId=event["id"], body=event).execute()
        else:
            event = service.events().insert(calendarId=calendar_id, body=event).execute()
    except Exception as exc:
        raise BadRequest from exc
    return event

def delete_event(calendar_id: str, event_id: str):
    """Deletes an event."""
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=G_CREDENTIALS)
    # Retrieve the events from the calendar
    try:
        event = service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    except Exception as exc:
        raise BadRequest from exc
    return event
