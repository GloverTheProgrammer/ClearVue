"""
Author: Jaydin Freeman
Date: 03/10/2024
Description: ToDo
"""

import time
import os
import sys
import tempfile
import threading
from collections import Counter
import cv2
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf
from gtts import gTTS
import pygame
import pygame.mixer
import RPi.GPIO as GPIO

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
from objectDetection.labels import classes

stream_stop_event = threading.Event()


def monitor_button():
    """
    Monitors the state of a button connected to the GPIO pin.
    If the button is pressed, it prints a message and exits the function.

    Args:
        None

    Returns:
        None
    """
    BUTTON_GPIO = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        if not GPIO.input(BUTTON_GPIO):  # Button is pressed
            print("Button pressed, exiting.")
            return
        time.sleep(0.1)  # Debounce delay


def button_press():
    """
    Creates a new thread to monitor the button and starts it. 
    It then waits for the thread to complete using the `join` method.
    Finally, it sets the `stream_stop_event` to stop the stream.

    Args:
    None

    Returns:
    None
    """
    monitor_button_thread = threading.Thread(target=monitor_button)
    monitor_button_thread.start()
    monitor_button_thread.join()
    stream_stop_event.set()


class ObjectDetectionStreamer:
    """
    A class for streaming object detection using EfficientDet model.

    Args:
        model_path (str): The path to the EfficientDet model file.
        frame_resize_dims (tuple, optional): The dimensions to resize the frames to. Defaults to (320, 320).
        skip_frames (int, optional): The number of frames to skip between detections. Defaults to 10.
        flip_camera (bool, optional): Whether to flip the camera input. Defaults to False.
        text_to_speech (bool, optional): Whether to enable text-to-speech for detected objects. Defaults to False.
    """

    def __init__(self, model_path, frame_resize_dims=(320, 320), skip_frames=10,
                 flip_camera=False, text_to_speech=False):
        self.model_path = model_path
        self.frame_resize_dims = frame_resize_dims
        self.skip_frames = skip_frames
        self.flip_camera = flip_camera
        self.text_to_speech = text_to_speech
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.labels = classes
        self.previous_summary = set()
        self.last_tts_time = time.time()
        self.tts_delay = 5

    def draw_boxes_with_labels(self, image, boxes, class_ids, scores, labels):
        """
        Draws bounding boxes with labels on the given image.

        Args:
            image (PIL.Image.Image): The input image.
            boxes (list): A list of bounding box coordinates in the format [ymin, xmin, ymax, xmax].
            classes (list): A list of class IDs corresponding to each bounding box.
            scores (list): A list of confidence scores for each bounding box.
            labels (dict): A dictionary mapping class IDs to class names.

        Returns:
            None
        """
        draw = ImageDraw.Draw(image)
        for box, class_id, score in zip(boxes, class_ids, scores):
            class_id = int(class_id) + 1
            if score > 0.5:
                ymin, xmin, ymax, xmax = box
                (left, right, top, bottom) = (xmin * image.width, xmax * image.width,
                                              ymin * image.height, ymax * image.height)
                draw.rectangle([(left, top), (right, bottom)],
                               outline="red", width=3)

                class_name = f"Classes: {labels.get(class_id, class_id)}"
                score = float(score)
                rounded_score = labels.get(
                    round(score, 3), f"Confidence: {round(score, 3):.3f}")
                coordinates = f"({left:.1f}, {top:.1f}), ({right:.1f}, {bottom:.1f})"
                draw.text((left, top), class_name, fill="red")
                draw.text((left, top + 20), rounded_score, fill="red")
                draw.text((left, top + 40), coordinates, fill="red")

    def process_frame(self, frame):
        """
        Processes a single frame for object detection.

        Args:
            frame: The input frame to be processed.

        Returns:
            A tuple containing the processed frame with bounding boxes drawn and the summary of detected objects.
        """
        if self.flip_camera:
            frame = cv2.flip(frame, -1)
        frame_small = cv2.resize(frame, self.frame_resize_dims)
        frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(frame_small, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        detected_classes = self.interpreter.get_tensor(
            self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(
            self.output_details[2]['index'])[0]
        image = Image.fromarray(frame_small)
        self.draw_boxes_with_labels(
            image, boxes, detected_classes, scores, self.labels)
        summary = self.summarize_detected_objects(
            boxes, detected_classes, scores, self.labels)

        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), summary

    def start_stream(self):
        """
            Starts the video stream and performs object detection on each frame.

            This method opens the video stream, reads each frame, processes it using the
            `process_frame` method, and displays the processed frame with bounding boxes
            and labels. It also checks for user input to stop the stream or if the
            `stream_stop_event` is set.

            If the `text_to_speech` flag is set to True, it summarizes the detected objects
            using the `tts_summarize` method.

            Note:
            - The video stream is captured from the default camera (index 0).
            - The `skip_frames` attribute determines the number of frames to skip before
              processing a frame.

            Args:
            None

            Returns:
            None
        """
        global stream_stop_event
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                for _ in range(self.skip_frames):
                    cap.grab()
                processed_frame, summary = self.process_frame(frame)
                print(summary)
                cv2.imshow('Video with Boxes and Labels', processed_frame)
                if cv2.waitKey(1) & 0xFF == ord('q') or stream_stop_event.is_set():
                    break
                if not self.text_to_speech:
                    continue
                current_objects = {(class_name, coordinates)
                                   for class_name, coordinates in summary}
                self.tts_summarize(current_objects)
        finally:
            cap.release()
            cv2.destroyAllWindows()
            stream_stop_event.clear()

    def take_picture(self, warmup_frames=30):
        """
        Takes a picture using the webcam and displays it with bounding boxes and labels.

        Args:
            warmup_frames (int): Number of frames to discard during warmup.

        Returns:
            None
        """
        cap = cv2.VideoCapture(0)
        try:
            for _ in range(warmup_frames):
                ret, frame = cap.read()
                if not ret:
                    raise ValueError("Failed to capture image during warmup")

            ret, frame = cap.read()

            if not ret:
                raise ValueError("Failed to capture image")

            processed_frame = self.process_frame(frame)
            cv2.imshow('Image with Boxes and Labels', processed_frame)
            cv2.waitKey(0)
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def summarize_detected_objects(self, boxes, class_ids, scores, labels):
        """
        Summarizes the detected objects based on the provided bounding boxes, class IDs, scores, and labels.

        Args:
            boxes (list): A list of bounding boxes in the format [ymin, xmin, ymax, xmax].
            class_ids (list): A list of class IDs corresponding to the detected objects.
            scores (list): A list of scores indicating the confidence level of the detected objects.
            labels (dict): A dictionary mapping class IDs to class names.

        Returns:
            set: A set containing tuples of (class_name, coordinates) for objects with scores greater than 0.5.
        """
        summary = set()
        for box, class_id, score in zip(boxes, class_ids, scores):
            if score > 0.5:
                class_id = int(class_id) + 1
                ymin, xmin, ymax, xmax = box
                coordinates = f"Coordinates: ({xmin:.2f}, {ymin:.2f}), ({xmax:.2f}, {ymax:.2f})"
                class_name = labels.get(class_id, "Unknown")
                summary.add((class_name, coordinates))
        return summary

    def tts_summarize(self, current_objects):
        """
        Summarizes the current objects detected and plays the summary as audio.

        Args:
            current_objects (list): A list of tuples containing the names and counts of the current objects detected.

        Returns:
            None
        """
        current_time = time.time()
        if current_time - self.last_tts_time < self.tts_delay:
            return
        # Determine new and lost objects by comparing current and previous Counter objects
        object_names = Counter([name for name, _ in current_objects])

        if object_names:
            details = ', '.join(
                [f"{count} {name}{'s' if count > 1 else ''}" for name, count in object_names.items()])
            message = f"In view: {details}."
        else:
            return

        tts = gTTS(text=message, lang='en')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        temp_file.close()

        self.play_audio_async(temp_file.name)

        # Update previous summary with current object names for the next comparison
        self.last_tts_time = current_time
        self.previous_summary = set([name for name, _ in current_objects])

    def play_audio_async(self, file_path):
        """
        Plays an audio file asynchronously.

        Args:
            file_path (str): The path to the audio file.

        Returns:
            None
        """
        def play_audio(file_path):
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        threading.Thread(target=play_audio, args=(file_path,)).start()

    def main():
        """
        The main method of the EfficientDet class.

        This method starts a button thread, loads the model, initializes an ObjectDetectionStreamer,
        and starts the stream. It waits for the button thread to finish before exiting.
        """
        button_thread = threading.Thread(target=button_press)
        button_thread.start()
        model_path = os.path.join(
            project_dir, "objectDetection/models/lite-model/lite-model_efficientdet_lite0_detection_metadata_1.tflite")
        streamer = ObjectDetectionStreamer(
            model_path=model_path, flip_camera=True, text_to_speech=True)
        streamer.start_stream()
        button_thread.join()


if __name__ == "__main__":
    ObjectDetectionStreamer.main()