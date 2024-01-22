"""Class file for tool for creating email drafts"""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.google.gmail import create_draft
from maia.openai.tools.tool import Tool


class CreateEmailDraftTool(Tool):
    """Enables user to create a email draft message."""
    function_definition: Function = {
        "name": "create_draft_email",
        "description": "Create an email draft message.",
        "parameters": {
            "type": "object",
            "required": ["to", "subject", "content"],
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Email adress of recipient."
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
        """Create email draft message."""
        logging.info("Tool CreateEmailDraftTool called.")
        return json.dumps(create_draft(**kwargs))
        