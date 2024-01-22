"""List calendars including calendarIds for available calendars."""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gcalendar import get_calendars_llm
from maia.openai.tools.tool import Tool


class ListCalendarsTool(Tool):
    """List calendars including calendarIds for available calendars."""
    function_definition: Function = {
        "name": "get_calendar_id",
        "description": "Get the calendar id for a specific calendar.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }

    @classmethod
    def call(cls, kwargs):
        """List calendars including calendarIds for available calendars."""
        logging.info("List calendars tool called.")
        calendars = get_calendars_llm()
        # Filter only important fields
        filtered_calendars = []
        for calendar in calendars:
            filtered_calendars.append({
                "id": calendar["id"], 
                "summary": calendar["summary"] if "summary" in calendar else "", 
                "description": calendar["description"] if "description" in calendar else ""
            })
        
        return json.dumps(filtered_calendars)
    
