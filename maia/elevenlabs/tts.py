"""Text-to-speech using Elevenlabs API."""
import logging

from elevenlabs import generate, play, set_api_key

from settings import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, ELEVENLABS_MODEL

set_api_key(ELEVENLABS_API_KEY)

def text_to_speech(text: str, instant_play: bool = True):
    """Convert text to speech and play it."""
    logging.info("Converting text to speech...")

    audio = generate(
        text=text,
        voice=ELEVENLABS_VOICE_ID,
        model=ELEVENLABS_MODEL
    )

    if instant_play:
        play_audio(audio)

def play_audio(audio: bytes):
    """Play audio."""
    play(audio)

