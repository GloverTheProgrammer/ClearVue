import os
import base64
import requests
import cv2
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv

load_dotenv()  # Loads the .env file into environment variables
api_key = os.getenv('OPENAI_API_KEY')

image_path = "/home/blackhat/Desktop/transcribe/opencv_frame.png"

system_ready = True

def button_press():
    BUTTON_GPIO = 16
    DELAY = 0.05  # Debounce delay in seconds
    HOLD_TIME = 2  # Time in seconds to differentiate between press and hold

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pressed_time = None
    mode = 0

    while True:
        if GPIO.input(BUTTON_GPIO) == GPIO.LOW:  # Button is pressed
            if pressed_time is None:
                pressed_time = time.time()
            elif (time.time() - pressed_time) > HOLD_TIME:
                # Button has been held down long enough to count as a hold
                mode = (mode + 1) % 3
                print("Button held. Mode changed to:", mode)
                pressed_time = None  # Reset pressed_time after changing mode
                return (False, mode)  # No action initiated, only mode changed
        else:
            if pressed_time is not None:
                if (time.time() - pressed_time) < HOLD_TIME:
                    # Button was pressed and released before the hold time: initiate action
                    print("Button pressed quickly. Action initiated for mode:", mode)
                    return (True, mode)  # Action should be initiated for the current mode
                pressed_time = None  # Reset pressed_time
            time.sleep(DELAY)


def save_image(directory="/home/blackhat/Desktop/transcribe/"):
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cam.read()
    cam.release()
    if not ret:
        print("Can't receive frame. Exiting ...")
        return

    frame = cv2.rotate(frame, cv2.ROTATE_180)
    img_name = os.path.join(directory, "opencv_frame.png")
    cv2.imwrite(img_name, frame)
    print(f"{img_name} written!")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')

def classify_image(base64_image, api_key, mode):
    if mode == 0:
        text_prompt = "Provide a comprehensive description of the image, without mentioning its a photograph or scene to the user, for a visually impaired person, focusing on identifying key objects, characters, and any text, including their arrangement and interactions within the scene. Describe the setting, atmosphere, and highlight any notable emotional or thematic elements. Include details on colors, shapes, and textures to enrich the description. If present, accurately transcribe text within the image. This description should help a visually impaired individual visualize the content and context as if they were seeing it themselves, all within a concise limit of three sentences"
    elif mode == 1:
        text_prompt = "Imagine a revolutionary wearable device designed specifically for the visually impaired—a smart hat equipped with a state-of-the-art camera. This innovative hat is not just a fashion statement; it's a groundbreaking tool that enhances the way visually impaired people interact with the world around them. At the heart of this device is an advanced camera system, discreetly integrated into the hat's design, which scans the wearer's surroundings in real-time. As the user approaches objects, the camera focuses on the nearest labels, from product descriptions at a grocery store to street signs and informational placards, instantly converting the visual data into audible information. This smart hat empowers users with greater independence and confidence, allowing them to navigate public spaces, shop, and explore their environment with an unprecedented level of clarity and ease. Be as concise as possible."
    elif mode == 2:
        text_prompt = "Provide a comprehensive description of the image, without mentioning its a photograph or scene to the user, for a visually impaired person, focusing on identifying key objects, characters, and any text, including their arrangement and interactions within the scene. Describe the setting, atmosphere, and highlight any notable emotional or thematic elements. Include details on colors, shapes, and textures to enrich the description. If present, accurately transcribe text within the image. This description should help a visually impaired individual visualize the content and context as if they were seeing it themselves, all while being consise as possible"

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": text_prompt,
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                },
            }],
        }],
        "max_tokens": 300,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
    except Exception as e:
        print(e)

def main():
    global system_ready
    mode = 0  # Initial mode

    while True:
        if system_ready:
            action_initiated, new_mode = button_press()  # Check for button action and mode

            if action_initiated:  # If a press is detected, classify the image for the current mode
                system_ready = False  # Prevent further actions until this one completes
                save_image()
                base64_image = encode_image(image_path)
                classify_image(base64_image, api_key, mode)
                system_ready = True  # Ready for a new action
            else:  # Mode changed on hold
                mode = new_mode  # Update the mode based on the button hold

if __name__ == "__main__":
    main()

