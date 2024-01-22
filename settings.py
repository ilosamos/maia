"""Prepares all config and app settings for the app to run."""
import logging
import os

from dotenv import load_dotenv

from maia.google.auth import get_creds_from_desktop_flow
from maia.utils.logging import CustomFormatter

load_dotenv()

# Convert env to constants
# OpenAI
OPENAI_LLM_MODEL=os.getenv("OPENAI_LLM_MODEL")
OPENAI_EMBEDDING_MODEL=os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# Elevenlabs
ELEVENLABS_API_KEY=os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID=os.getenv("ELEVENLABS_VOICE_ID")
ELEVENLABS_MODEL=os.getenv("ELEVENLABS_MODEL")

# Google
GOOGLE_STT_API_KEY=os.getenv("GOOGLE_STT_API_KEY")

# App Specific
INITIAL_SYSTEM_PROMPT=os.getenv("INITIAL_SYSTEM_PROMPT")

# Zoho
ZOHO_CLIENT_ID=os.getenv("ZOHO_CLIENT_ID")
ZOHO_CLIENT_SECRET=os.getenv("ZOHO_CLIENT_SECRET")
ZOHO_ACCESS_TOKEN=os.getenv("ZOHO_ACCESS_TOKEN")
ZOHO_REFRESH_TOKEN=os.getenv("ZOHO_REFRESH_TOKEN")
ZOHO_ACCOUNT_ID=os.getenv("ZOHO_ACCOUNT_ID")
ZOHO_INBOX_FOLDER_ID=os.getenv("ZOHO_INBOX_FOLDER_ID")

#SLACK
SLACK_APP_ID=os.getenv("SLACK_APP_ID")
SLACK_SIGNING_SECRET=os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN=os.getenv("SLACK_BOT_TOKEN")

# CONFLUENCE
CONFLUENCE_BASE_URL=os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_API_EMAIL=os.getenv("CONFLUENCE_API_EMAIL")
CONFLUENCE_API_TOKEN=os.getenv("CONFLUENCE_API_TOKEN")

# Google credentials need client-secret.json file from google cloud console
# Uncomment this if you don't use google stuff
G_CREDENTIALS = get_creds_from_desktop_flow()

# All logging stuff goes here
logging.basicConfig(level=logging.INFO)
root_logger = logging.getLogger()
for handler in root_logger.handlers:
    handler.setFormatter(CustomFormatter('%(asctime)s %(levelname)s %(message)s'))
