from collections import Counter
import cv2
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf
from labels import classes
from gtts import gTTS
import pygame
import os
import pygame.mixer
import tempfile
from gtts import gTTS
from threading import Thread

class ObjectDetectionStreamer:
    def __init__(self, model_path, frame_resize_dims=(320, 320), skip_frames=10, flip_camera=False, text_to_speech=False):
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

    def draw_boxes_with_labels(self, image, boxes, classes, scores, labels):
        draw = ImageDraw.Draw(image)
        for box, class_id, score in zip(boxes, classes, scores):
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
                    round(score, 3), f"Confience: {round(score, 3):.3f}")
                coordinates = f"({left:.1f}, {top:.1f}), ({right:.1f}, {bottom:.1f})"
                draw.text((left, top), class_name, fill="red")
                draw.text((left, top + 20), rounded_score, fill="red")
                draw.text((left, top + 40), coordinates, fill="red")

    def process_frame(self, frame):
        if self.flip_camera:
            frame = cv2.flip(frame, -1)
        frame_small = cv2.resize(frame, self.frame_resize_dims)
        frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(frame_small, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0]
        classes = self.interpreter.get_tensor(
            self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(
            self.output_details[2]['index'])[0]
        image = Image.fromarray(frame_small)
        self.draw_boxes_with_labels(image, boxes, classes, scores, self.labels)
        summary = self.summarize_detected_objects(
            boxes, classes, scores, self.labels)

        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR), summary

    def start_stream(self):
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
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                if not self.text_to_speech:
                    continue
                current_objects = {(class_name, coordinates)
                                   for class_name, coordinates in summary}
                self.tts_summarize(current_objects)
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def take_picture(self, warmup_frames=30):
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

    def summarize_detected_objects(self, boxes, classes, scores, labels):
        summary = set()
        for box, class_id, score in zip(boxes, classes, scores):
            if score > 0.5:
                class_id = int(class_id) + 1
                ymin, xmin, ymax, xmax = box
                coordinates = f"Coordinates: ({xmin:.2f}, {ymin:.2f}), ({xmax:.2f}, {ymax:.2f})"
                class_name = labels.get(class_id, "Unknown")
                summary.add((class_name, coordinates))
        return summary

    def tts_summarize(self, current_objects):
        # Create a Counter for the current and previous objects to manage counts
        current_objects_counter = Counter(
            [name for name, _ in current_objects])
        previous_objects_counter = Counter(self.previous_summary)

        # Determine new and lost objects by comparing current and previous Counter objects
        new_objects = current_objects_counter - previous_objects_counter
        lost_objects = previous_objects_counter - current_objects_counter

        messages = []
        if new_objects:
            new_obj_messages = [
                f"{count} {obj}{' has' if count == 1 else 's have'} been added." for obj, count in new_objects.items()]
            messages.append(' '.join(new_obj_messages))
        if lost_objects:
            lost_obj_messages = [
                f"{count} {obj}{' has' if count == 1 else 's have'} been lost." for obj, count in lost_objects.items()]
            messages.append(' '.join(lost_obj_messages))

        if not messages:
            return

        message = ' '.join(messages)
        tts = gTTS(text=message, lang='en')
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        temp_file.close()

        self.play_audio_async(temp_file.name)

        # Update previous summary with current object names for the next comparison
        self.previous_summary = set([name for name, _ in current_objects])

    def play_audio_async(self, file_path):
        def play_audio(file_path):
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        Thread(target=play_audio, args=(file_path,)).start()


if __name__ == "__main__":
    model_path = "objectDetection/models/lite-model/lite-model_efficientdet_lite0_detection_metadata_1.tflite"
    streamer = ObjectDetectionStreamer(
        model_path=model_path, flip_camera=True, text_to_speech=True)
    streamer.start_stream()
