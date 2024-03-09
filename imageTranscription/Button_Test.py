import time
import RPi.GPIO as GPIO

BUTTON_GPIO = 16
DELAY = 500
last_ms = 0

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pressed = False

    while True:
        # button is pressed when pin is LOW
        if not GPIO.input(BUTTON_GPIO):
            if not pressed and (time.time() * 1000 - last_ms > DELAY):
                print("Button pressed!")
                pressed = True
                last_ms = time.time() * 1000
        # button not pressed (or released)
        else:
            pressed = False
        time.sleep(0.1)