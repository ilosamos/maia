"""List all confluence pages"""
import json
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.confluence.spaces import list_all_pages
from maia.openai.tools.tool import Tool


class ListConfluencePages(Tool):
    """Get all confluence pages"""
    function_definition: Function = {
        "name": "list_confluence_pages",
        "description": "List all the confluence pages the user has access to.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }

    @classmethod
    def call(cls, kwargs):
        """List all confluence pages (without content)"""
        logging.info("Tool ListConfluencePages called.")
        pages = list_all_pages(**kwargs)
        return json.dumps(pages)
