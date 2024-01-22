"""Slack bot for Maia."""
import logging

from slack_bolt import App

from maia.openai.llm import chat_completion

app = App()

# Add functionality here
@app.command("/maia")
def command(ack, respond, cmd):
    """Handle slack command."""
    ack()
    respond(msg(f"User wrote: _{cmd['text']}_"))

    try:
        completion = chat_completion([{ "role": "user", "content": cmd["text"]}])
        respond(msg(completion))
    except Exception as e:
        logging.error(e)
        respond(msg("Sorry there was en error processing the request. Please try again later."))

def msg(text: str) -> str:
    """Create a slack message."""
    return { 
        "response_type": "in_channel",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": text
                }
            }
        ]
    }

if __name__ == "__main__":
    app.start(8080)  # POST http://localhost:8080/slack/events