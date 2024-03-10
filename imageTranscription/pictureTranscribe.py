import os
import base64
from openai import OpenAI
import requests
import cv2
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv


load_dotenv()  # Loads the .env file into environment variables
api_key = os.getenv('OPENAI_API_KEY')

image_path = "/home/blackhat/Desktop/transcribe/opencv_frame.png"


def button_press():
    BUTTON_GPIO = 16
    DELAY = 500
    last_ms = 0
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
                return True
        # button not pressed (or released)
        else:
            pressed = False
        time.sleep(0.1)


def save_image(directory="/home/blackhat/Desktop/transcribe/"):
    # Create the directory if it doesn't exist
    
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cam.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    
    img_name = os.path.join(directory, f"opencv_frame.png")
    cv2.imwrite(img_name, frame)
    print(f"{img_name} written!")

    cam.release()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')


def story_classify(base64_image, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
    "model":"gpt-4-vision-preview",
    "messages":[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Provide a comprehensive description of the image, without mentioning its a photograph or scene to the user, for a visually impaired person, focusing on identifying key objects, characters, and any text, including their arrangement and interactions within the scene. Describe the setting, atmosphere, and highlight any notable emotional or thematic elements. Include details on colors, shapes, and textures to enrich the description. If present, accurately transcribe text within the image. This description should help a visually impaired individual visualize the content and context as if they were seeing it themselves, all within a concise limit of three sentences",
            },
            {
            "type": "image_url",
            "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    "max_tokens" : "300",
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
    except Exception as e:
        print(e)

def label_classify(base64_image, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
    "model":"gpt-4-vision-preview",
    "messages":[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Imagine a revolutionary wearable device designed specifically for the visually impaired—a smart hat equipped with a state-of-the-art camera. This innovative hat is not just a fashion statement; it's a groundbreaking tool that enhances the way visually impaired people interact with the world around them. At the heart of this device is an advanced camera system, discreetly integrated into the hat's design, which scans the wearer's surroundings in real-time. As the user approaches objects, the camera focuses on the nearest labels, from product descriptions at a grocery store to street signs and informational placards, instantly converting the visual data into audible information. This smart hat empowers users with greater independence and confidence, allowing them to navigate public spaces, shop, and explore their environment with an unprecedented level of clarity and ease. Be as concise as possible.",
            },
            {
            "type": "image_url",
            "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    "max_tokens" : "300",
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
    except Exception as e:
        print(e)

def closest_classify(base64_image, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
    "model":"gpt-4-vision-preview",
    "messages":[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Provide a comprehensive description of the image, without mentioning its a photograph or scene to the user, for a visually impaired person, focusing on identifying key objects, characters, and any text, including their arrangement and interactions within the scene. Describe the setting, atmosphere, and highlight any notable emotional or thematic elements. Include details on colors, shapes, and textures to enrich the description. If present, accurately transcribe text within the image. This description should help a visually impaired individual visualize the content and context as if they were seeing it themselves, all while being consise as possible",
            },
            {
            "type": "image_url",
            "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    "max_tokens" : "300",
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response.json())
    except Exception as e:
        print(e)








if button_press():
    save_image()
    base64_image = encode_image(image_path)
    story_classify(base64_image, api_key)
    


