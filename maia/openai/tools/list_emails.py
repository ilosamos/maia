import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gmail import get_emails_llm
from maia.openai.tools.tool import Tool


class ListEmailsTool(Tool):
    """Get last x emails for user"""
    function_definition: Function = {
        "name": "get_emails",
        "description": f"Get the users last few emails. Make sure to optimize the output for speech.",
        "parameters": {
            "type": "object",
            "properties": {
                "unread_only": {
                    "type": "boolean",
                    "description": "Only return calendars with unread emails."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Get last x emails for user"""
        logging.info("List emails tool called.")
        emails = get_emails_llm(**kwargs)
        return json.dumps(emails)