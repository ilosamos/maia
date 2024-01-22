"""Example how to use elevenlabs text to speech"""
from maia.openai.llm import chat
from maia.elevenlabs.tts import text_to_speech

prompt = "Hi what's the weather in Vienna?"
result = chat(prompt)
print(result)
text_to_speech(result)