"""Class file for tool for search for users contacts."""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.people import search_contacts
from maia.openai.tools.tool import Tool


class SearchContactsTool(Tool):
    """Enables user to search for email adresses of people."""
    function_definition: Function = {
        "name": "search_contacts",
        "description": "Search for a contact in the users contact list to get their email adresses.",
        "parameters": {
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Search for contacts."""
        logging.info("Tool SearchContactsTool called.")
        return json.dumps(search_contacts(**kwargs))
        