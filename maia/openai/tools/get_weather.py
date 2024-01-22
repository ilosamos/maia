"""Get the weather via python-weather"""
import logging

from openai.types.chat.chat_completion_message_tool_call import Function

from maia.openai.tools.tool import Tool
from maia.weather.weather import get_weather


class GetWeatherTool(Tool):
    """Get the weather via python-weather"""
    function_definition: Function = {
        "name": "get_weather",
        "description": "Get the weather in Vienna.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city of the weather report."
                }
            }
        }
    }

    @classmethod
    def call(cls, kwargs):
        """Get the weather via python-weather"""
        logging.info("GetWeatherTool called.")
        return get_weather(**kwargs)