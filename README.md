# maia
### Toolkit for your personal AI assistant.

This repo should help anyone who wants to build a customized AI assistant powered by Openai GPT models.
It uses OpenAI chat API with functions to give the assistant some capabilites. A few of those are:
- Google calendar (search, create or update events)
- Google mail (read/write emails)
- Weather (Get a weather report for a specific town)
- Confluence (search for pages and read content in pages)

> **_Note:_** The assistant as its currently designed takes an input a prompt and then decides which tools to use or tasks to do and then gives you a response. There is no mechanism to have or store a continuous conversation.

## Examples
The repository provides some examples of how to interact with the assistant. Those are:
- Basic python script
- Slack Bot
- Homekit
- Speech recognition
- Text to speech

## Dependencies
Since there are lots of different tools involved, there are certain dependencies needed in order to run everything (see requirements.txt).
However feel free to clone the repo and mix and match what you need and disregard what you don't need.
For example in order to run text to speech "ffmpeg" is needed.

## Get Started
Since most of the tools use external APIs, some configuration is needed in order to run the code. All the configuration should be included in an .env file (not included in the repo). Alternatively you could use environment variables with the same name as the variables in .env. Environment variables will overwrite .env configs.

## .env
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