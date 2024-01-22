"""Get the content of a confluence page."""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.confluence.spaces import get_page_content
from maia.openai.tools.tool import Tool


class GetConfluencePage(Tool):
    """Get the content of a confluence page"""
    function_definition: Function = {
        "name": "get_confluence_page",
        "description": "Get a confluence page content by its id.",
        "parameters": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "string",
                    "description": "The confluence page id."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Get a specific confluence page."""
        logging.info("Tool GetConfluencePage called.")
        page = get_page_content(**kwargs)
        return json.dumps(page)
