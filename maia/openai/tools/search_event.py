"""Tool enables user to search for a specific search term to find the best matching event in the google calendar using embedding and cosine similarity."""
import json
import logging

import numpy as np
import openai
from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gcalendar import get_events
from maia.openai.tools.tool import Tool
from maia.utils.ml import cosine_similarity
from maia.openai.embedding import embedding_search
from settings import OPENAI_EMBEDDING_MODEL


class SearchEventTool(Tool):
    """Tool enables user to search for a specific search term to find the best matching event in the google calendar using embedding and cosine similarity."""
    function_definition: Function = {
        "name": "search_event",
        "description": "Search for a specific event in the calendar according to a search term.",
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
                "search_term": {
                    "type": "string",
                    "description": "Search term to find events that match these terms in any field, except for extended properties."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Search for a specific event in the calendar according to a search term."""
        calendar_ids = kwargs.pop('calendarIds')
        search_term = kwargs.pop('search_term')
        logging.info("Calling search event tool with search_term %s", search_term)

        events = get_events(calendar_ids=calendar_ids)
        data_list = [event["summary"] for event in events]
        best_match = embedding_search(data_list, search_term)
        
        return json.dumps(events[best_match])