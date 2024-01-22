"""Class file for tool for sending emails"""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gmail import create_and_send
from maia.openai.tools.tool import Tool


class SendEmailTool(Tool):
    """Enables user to create and send an email message."""
    function_definition: Function = {
        "name": "send_email",
        "description": "Send an email.",
        "parameters": {
            "type": "object",
            "required": ["to", "subject", "content"],
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Email recipient."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject."
                },
                "content": {
                    "type": "string",
                    "description": "Email content."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Send email."""
        logging.info("Tool SendEmailTool called.")
        return json.dumps(create_and_send(**kwargs))
        