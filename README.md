# maia
### Python toolkit for your personal AI work-assistant.

**What it is:** This repo should act as a swiss army knife for everyone who wants to build a customized python AI assistant powered by Openai GPT models.

**What it is not:** An out of the box home assistant. 

The project uses OpenAI chat API with functions to give the assistant some capabilites.<br> 
https://platform.openai.com/docs/api-reference/chat<br>

A few of those are:
- Google calendar (search, create or update events)
- Google mail (read/write emails)
- Weather (Get a weather report for a specific town)
- Confluence (search for pages and read content in pages)

> **_Note:_** The assistant as its currently designed takes an input a prompt and then decides which tools to use or tasks to do and then gives you a response. There is no mechanism to have or store a continuous conversation.

## Dependencies
The code was written using **python 3.9** within **venv**.
Since there are lots of different tools involved, there are certain dependencies needed in order to run everything (see requirements.txt).
However feel free to clone the repo and mix and match what you need and disregard what you don't need.
For example in order to run text to speech "ffmpeg" is needed. You can also take a look into the Dockerfile where you can find external dependencies you would need outside python dependencies.
For example when you use ubuntu you would need the following dependencies other than python:
- build-essential 
- ffmpeg 
- python3-dev 
- libasound2-dev 
- libportaudio2 
- libportaudiocpp0 
- portaudio19-dev
<br><br>
### Install python dependencies using venv: ###
```bash
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

## Examples
The repository provides some examples of how to interact with the assistant. Those are:
- Basic python script (main.py)
- Slack Bot (example-slack.py)
- Homekit (example-homekit.py)
- Speech recognition (example-sr.py)
- Text to speech (example-tts.py)
- Dockerfile (just to show you how you could run it in docker)


Run a simple promt:
```bash
python main.py
```

## Config
Since most of the tools use external APIs, some configuration is needed in order to run the code. All the configuration should be included in an .env file (not included in the repo). Alternatively you could use environment variables with the same name as the variables in .env. Environment variables will overwrite .env configs.

This config also includes the initial prompt or the "system" prompt which should act as the base instructions how
the assistant should behave and interact with the user.

### Google
Note in order to use the googlel tools, you need to create a project in google cloud console and add a file called 
`desktop-client-secret.json` to the root of the project.

Also when starting the assistant for the first time and with activated google capabilities, you will be prompted for a google login in order for the assistant to use things like calendar api. After that a file called `token.json` will be created which holds your google user's access token along with a refresh token.

### .env
Here is a full list of configurations that can be set using .env file:
```bash
# OpenAI
OPENAI_LLM_MODEL="gpt-4-1106-preview"
OPENAI_EMBEDDING_MODEL="text-embedding-ada-002"
OPENAI_API_KEY="<your-openai-api-key>"

# Elevenlabs
ELEVENLABS_API_KEY="<your-elevenlabs-api-key>"

# Google
GOOGLE_STT_API_KEY="<google-api-key-to-use-speech-recognition>"

# App Specific
INITIAL_SYSTEM_PROMPT="
You are a helpful AI assistant.
"

# SLACK
SLACK_APP_ID="<slack-app-id>"
SLACK_SIGNING_SECRET="<slack-signing-secret>"
SLACK_BOT_TOKEN="<slack-bot-token>"

# CONFLUENCE
CONFLUENCE_BASE_URL="https://<your-site>.atlassian.net"
CONFLUENCE_API_EMAIL="<your-confluence-email>"
CONFLUENCE_API_TOKEN="<your-confluence-api-token>"
```

## Adding tools
All tools are located inside maia/openai/functions. 
A tool class file should look like this:
```python
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
```
>**Note:** I recommend keeping the tool classes free of logic to rather use them as an interface for calling you actual functions. The LLM can decide the parameters to use by itself which are then handed to the function using `**kwargs`.

After you created a new tool. You just have to add it to the tools array inside maia/openai/llm.py, that's it. The
LLM will use the description of the tools to determine which tools to use and with which arguments to call it with.
```python
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
```

>**_Note:_** It is recommended to first start with a small subset of tools and then work your way up as you configure everything.

## Other stuff
This is a spare time project of mine. There is no active support or anything. However feel free to raise issues or create a pull request. I will look into it if i find the time.

