"""Create event tool enables user to create a new event in the google calendar."""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gcalendar import create_or_update_event
from maia.openai.tools.tool import Tool


class CreateEventTool(Tool):
    """Tool enables user to create a new event in the google calendar."""
    function_definition: Function = {
        "name": "create_event",
        "description": "Create a new event in the calendar.",
        "parameters": {
            "type": "object",
            "required": ["calendarId", "summary", "start", "end", "location", "description"],
            "properties": {
                "calendarId": {
                    "type": "string",
                    "description": "Calendar ID to create or delte an event."
                },
                "summary": {
                    "type": "string",
                    "description": "Title of the event."
                },
                "start": {
                    "type": "object",
                    "description": "The (inclusive) start time of the event. For a recurring event, this is the start time of the first instance.",
                    "required": ["dateTime", "timeZone"],
                    "properties": {
                        "dateTime": {
                            "type": "string",
                            "description": "The time, as a combined date-time value (formatted according to RFC3339)."
                        },
                        "timeZone": {
                            "type": "string",
                            "description": "The time zone in which the time is specified. Example: \"Europe/Zurich\")."
                        }
                    }
                },
                "end": {
                    "type": "object",
                    "description": "The (exclusive) end time of the event. For a recurring event, this is the end time of the first instance.",
                    "required": ["dateTime", "timeZone"],
                    "properties": {
                        "dateTime": {
                            "type": "string",
                            "description": "The time, as a combined date-time value (formatted according to RFC3339)."
                        },
                        "timeZone": {
                            "type": "string",
                            "description": "The time zone in which the time is specified. Example: \"Europe/Zurich\")."
                        }
                    }
                },
                "location": {
                    "type": "string",
                    "description": "The location of the event, such as a location name, address or geographic coordinates."
                },
                "description": {
                    "type": "string",
                    "description": "Description of the event, such as additional infos and notes."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Create event in the google calendar."""
        logging.info("Create event tool called.")
        try:
            return json.dumps(create_or_update_event(kwargs))
        except: # pylint: disable=bare-except
            return json.dumps({ "error": "Could not create event." })