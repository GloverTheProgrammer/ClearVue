import time
import threading
from pynput import keyboard

BOARD = "board"
BCM = "bcm"
OUT = "out"
IN = "in"
PUD_UP = "pud_up"

_gpio_state = {}
_mode = None
_button_state = {}
_button_callback = {}

def setmode(mode):
    global _mode
    _mode = mode
    print(f"GPIO mode set to: {mode}")

def setup(channel, direction, pull_up_down=None):
    _gpio_state[channel] = False
    if direction == IN:
        _button_state[channel] = True
    print(f"Setup GPIO {channel}: {direction}")

def output(channel, state):
    _gpio_state[channel] = state
    print(f"Set GPIO {channel} to: {state}")

def input(channel):
    return _button_state.get(channel, True)

def cleanup():
    global _gpio_state, _mode, _button_state, _button_callback
    _gpio_state = {}
    _mode = None
    _button_state = {}
    _button_callback = {}
    print("GPIO cleanup performed")

def add_event_detect(channel, edge, callback=None, bouncetime=None):
    _button_callback[channel] = callback
    print(f"Event detection added for GPIO {channel}")

def on_press(key):
    try:
        if key == keyboard.Key.space:
            for channel in _button_state:
                _button_state[channel] = False
                print(f"Simulated button press on GPIO {channel}")
    except AttributeError:
        pass

def on_release(key):
    try:
        if key == keyboard.Key.space:
            for channel in _button_state:
                _button_state[channel] = True
                print(f"Simulated button release on GPIO {channel}")
    except AttributeError:
        pass

def _key_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Start the key listener thread
threading.Thread(target=_key_listener, daemon=True).start()

print("Spacebar listener started. Press spacebar to simulate button press.")