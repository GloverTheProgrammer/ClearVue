import time
import RPi.GPIO as GPIO



def button_press():

    BUTTON_GPIO = 16
    DELAY = 500
    HOLD = 2200

    start_ms = 0
    start_press_ms = 0

    mode = 0
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pressed = False
    held = False

    while True:

        if not GPIO.input(BUTTON_GPIO):
            if not pressed and (time.time() * 1000 - start_ms > DELAY):
                pressed = True
                start_ms = time.time() * 1000
            if pressed and not held and (time.time() * 1000 - start_ms > HOLD):
                held = True
                if mode == 2:
                    mode = 0
                else
                    mode = mode + 1
                print(mode)

        else:
            if pressed and not held:
                print("pressed")
            pressed = False
            held = False
        time.sleep(0.1)