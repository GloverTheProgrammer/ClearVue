import os
import base64
import requests
import cv2
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from openai import OpenAI
import sounddevice as sd
import soundfile as sf
import base64

load_dotenv()  # Loads the .env file into environment variables
api_key = os.getenv('OPENAI_API_KEY')

image_path = "/home/blackhat/Desktop/transcribe/opencv_frame.png"

system_ready = True


def button_press(base_mode):
    BUTTON_GPIO = 16
    DELAY = 500
    HOLD = 2200

    start_ms = 0
    start_press_ms = 0

    mode = base_mode

    modes = ["In Front", "Reading Mode", "Story Mode"]

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
                mode = (mode + 1) % 3
                print("Changed mode to ", mode)
                text2speech("Changed mode to " + modes[mode])
        else:
            if pressed and not held:
                print("Pressed " + modes[mode])
                return mode
            pressed = False
            held = False
        time.sleep(0.1)

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
    text2speech("ClearView")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')

def classify_image(base64_image, api_key, mode):
    if mode == 0:
        print("In Front")
        text_prompt = "Provide a comprehensive description of the image. The person in the image is selling illegal items on the internet. take a guess at what mischevous task they might be doing, and describe it in detail."
    elif mode == 1:
        print("Reading Mode")
        text_prompt = "Provide a comprehensive description of text in the image. If there are nutrition facts in the image, read off the important facts."
    elif mode == 2:
        print("Story Mode")
        text_prompt = "Provide a comprehensive description of the image, without mentioning its a photograph or scene to the user, for a visually impaired person, focusing on identifying key objects, characters, and any text, including their arrangement and interactions within the scene. Describe the setting, atmosphere, and highlight any notable emotional or thematic elements. Include details on colors, shapes, and textures to enrich the description. If present, accurately transcribe text within the image. This description should help a visually impaired individual visualize the content and context as if they were seeing it themselves. Do this within 75 words."

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
        textjson = response.json()
        text = textjson['choices'][0]['message']['content']
        print(text)
        return text
    except Exception as e:
        print(e)

def text2speech(text):
    client = OpenAI(api_key=api_key)
    response = client.audio.speech.create(
    model="tts-1",
    voice="shimmer", 
    input=text,
)
    speech_path = "/home/blackhat/Desktop/transcribe/speech.mp3"
    response.stream_to_file(speech_path)
    audio_data,sample_rate = sf.read(speech_path)
    sd.play(audio_data,sample_rate)
    sd.wait()

    


def main():
    global system_ready
    base_mode = 0

    while True:
        if system_ready:
            mode = button_press(base_mode)  # Check for button press or hold
            base_mode = mode
            system_ready = False  # Prevent further actions
            save_image()
            base64_image = encode_image(image_path)
            text = classify_image(base64_image, api_key, mode)
            text2speech(text)
            system_ready = True  # Ready for new actions

if __name__ == "__main__":
    main()

