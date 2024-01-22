"""OpenAI Language Model (LLM) chat completion."""
import datetime
import json
import logging

import openai
from openai.types.chat.chat_completion import Choice
from openai.types.chat.chat_completion_message_tool_call import \
    ChatCompletionMessageToolCall
from openai.types.chat.chat_completion_tool_message_param import \
    ChatCompletionToolMessageParam

from maia.openai.tools.create_email_draft import CreateEmailDraftTool
from maia.openai.tools.create_event import CreateEventTool
from maia.openai.tools.get_conf_page import GetConfluencePage
from maia.openai.tools.get_weather import GetWeatherTool
from maia.openai.tools.list_calendars import ListCalendarsTool
from maia.openai.tools.list_conf_pages import ListConfluencePages
from maia.openai.tools.list_emails import ListEmailsTool
from maia.openai.tools.list_events import ListEventsTool
from maia.openai.tools.search_contacts import SearchContactsTool
from maia.openai.tools.search_event import SearchEventTool
from maia.openai.tools.send_email import SendEmailTool
from settings import INITIAL_SYSTEM_PROMPT, OPENAI_API_KEY, OPENAI_LLM_MODEL

openai.api_key = OPENAI_API_KEY

today = datetime.datetime.now()
today = today.strftime("%d.%m.%Y %H:%M:%S")
timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo

# Add or remove tools here
tools = [
    CreateEmailDraftTool,
    CreateEventTool,
    GetConfluencePage,
    GetWeatherTool,
    ListCalendarsTool,
    ListConfluencePages,
    ListEmailsTool,
    ListEventsTool,
    SearchContactsTool,
    SearchEventTool,
    SendEmailTool
]

# Tool switcher provides actual function call for given tool name
tool_switcher = {tool.function_definition["name"]: tool.call for tool in tools}

def chat(prompt: str) -> str:
    """Run openai chat completion."""
    messages = [{ "role": "user", "content": prompt }]
    return chat_completion(messages)

def chat_completion(conversation: list) -> str:
    """Run openai chat completion."""
    logging.info("Running openai completion...")
    messages = [{ "role": "system", "content": INITIAL_SYSTEM_PROMPT }]
    messages.append({ "role": "system", "content": f"The current date and time is {today} in the timezone {timezone}" })
    messages.extend(conversation)
    return _completion(messages)

def _get_model_params(messages: list) -> dict:
    return {
        "model": OPENAI_LLM_MODEL,
        "temperature": 1.2,
        "messages": messages,
        "tools": [{"type": "function", "function": tool.function_definition} for tool in tools]
    }

def _completion(messages: list) -> str:
    """Call openai api recursively depending on function choice"""
    model_params = _get_model_params(messages)
    response = _openai_chat(model_params)
    tool_messages = []

    if response.message.tool_calls:
        messages.append(response.message)
        for tool_call in response.message.tool_calls:
            tool_message = _call_tool(tool_call)
            tool_messages.append(tool_message)

    if len(tool_messages) > 0:
        messages.extend(tool_messages)
        return _completion(messages)

    assistant_reply = response.message.content
    return assistant_reply

def _openai_chat(model_params: dict) -> Choice:
    response = openai.chat.completions.create(**model_params)
    response = response.choices[0]
    return response

def _call_tool(tool_call: ChatCompletionMessageToolCall):
    kwargs = json.loads(tool_call.function.arguments)
    result = tool_switcher.get(tool_call.function.name)(kwargs)
    return _get_tool_message(result, tool_call.id)

def _get_tool_message(result: str, tool_call_id: str) -> ChatCompletionToolMessageParam:
    """Convert tool result into openai message"""
    return {
        "role": "tool",
        "content": result,
        "tool_call_id": tool_call_id
    }
