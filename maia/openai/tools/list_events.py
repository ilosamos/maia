"""This file contains the implementation of the list_events tool.""" 
import datetime
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gcalendar import get_events_llm
from maia.openai.tools.tool import Tool

today = datetime.datetime.now()
today = today.strftime("%d.%m.%Y %H:%M:%S")
timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo


class ListEventsTool(Tool):
    """List events from the google calendar."""
    function_definition: Function = {
        "name": "list_events",
        "description": f"List events from the google calendar. Today is {today} in the timezone {timezone}",
        "parameters": {
            "type": "object",
            "required": ["calendarIds", "timeMin", "timeMax"],
            "properties": {
                "calendarIds": {
                    "type": "array",
                    "description": "List of calendar IDs to query. Example: ['primary']",
                    "items": {
                        "type": "string",
                        "description": "calendar id"
                    }
                },
                "timeMin": {
                    "type": "string",
                    "description": "Lower bound for an event's start time to filter by. Example: '2023-07-10T00:00:00+02:00'"
                },
                "timeMax": {
                    "type": "string",
                    "description": "Upper bound for an event's end time to filter by. Example: '2023-07-10T00:00:00+02:00'"
                },
                "maxResults": {
                    "type": "integer",
                    "description": "The maximum number of results to return. Default is 10. Optional."
                },
                "q": {
                    "type": "string",
                    "description": "Free text search terms to find events that match these terms in any field, except for extended properties. Optional."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """List events from the google calendar."""
        logging.info("Calling list events tool with kwargs %s", kwargs)
        calendar_ids = kwargs.pop('calendarIds')
        events = get_events_llm(calendar_ids, **kwargs)
        return json.dumps(events)
