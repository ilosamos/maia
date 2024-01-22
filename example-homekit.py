
"""This is a sample server for triggering something using homekit"""
import os.path

from homekit import AccessoryServer
from homekit.model import Accessory, LightBulbService
from maia.elevenlabs.tts import text_to_speech
from maia.openai.llm import chat


def on_set(value):
    """Trigger something. Value is 1 or 0"""
    if value:
        print("CALL SOME PREDEFINED LLM PROMPT HERE")
        result = chat("Hi show me all my unread emails.")
        print(result)

        # You can use text to speech for example
        #text_to_speech(result)

if __name__ == '__main__':
    """Simple light switch accessory"""
    try:
        httpd = AccessoryServer(os.path.expanduser('homekit-sample-server.json'))

        accessory = Accessory('test_light', 'homekit_python', 'Demoserver', '0001', '0.1')
        lightService = LightBulbService()
        lightService.set_on_set_callback(on_set)
        accessory.services.append(lightService)
        httpd.accessories.add_accessory(accessory)

        httpd.publish_device()
        print('published device and start serving')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('unpublish device')
        httpd.unpublish_device()
