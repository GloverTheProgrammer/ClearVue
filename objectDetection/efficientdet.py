import cv2
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf
from labels import classes
from gtts import gTTS
import subprocess
class ObjectDetectionStreamer:
    def __init__(self, model_path, frame_resize_dims=(320, 320), skip_frames=10, flip_camera=False):
        self.model_path = model_path
        self.frame_resize_dims = frame_resize_dims
        self.skip_frames = skip_frames
        self.flip_camera = flip_camera
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
                draw.rectangle([(left, top), (right, bottom)], outline="red", width=3)
                # Replace 'N/A' with actual class if missing
                class_name = f"Classes: {labels.get(class_id, class_id)}"
                score = float(score)
                rounded_score = labels.get(round(score, 3), f"Confience: {round(score, 3):.3f}")
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
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0]
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0]
        image = Image.fromarray(frame_small)
        self.draw_boxes_with_labels(image, boxes, classes, scores, self.labels)
        summary = self.summarize_detected_objects(boxes, classes, scores, self.labels)

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
                cv2.imshow('Video with Boxes and Labels', processed_frame)
                current_objects = {(class_name, coordinates) for class_name, coordinates in summary}
                self.tts_summarize(current_objects)  # Call tts_summarize with current detected objects
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
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
        summary = set()  # Use a set for efficient comparison in tts_summarize
        for box, class_id, score in zip(boxes, classes, scores):
            if score > 0.5:  # Filter objects with low confidence
                class_id = int(class_id) + 1  # Adjust class_id to match labels dictionary
                ymin, xmin, ymax, xmax = box
                coordinates = f"Coordinates: ({xmin:.2f}, {ymin:.2f}), ({xmax:.2f}, {ymax:.2f})"
                class_name = labels.get(class_id, "Unknown")
                summary.add((class_name, coordinates))  # Add tuple of class_name and coordinates
        return summary  # Return a set of tuples

    def tts_summarize(self, current_objects):
        """
        Uses gTTS to summarize changes in detected objects.

        :param current_objects: A set of tuples with class names and coordinates of currently detected objects.
        """
        current_summary = {name for name, _ in current_objects}
        new_objects = current_summary - self.previous_summary
        lost_objects = self.previous_summary - current_summary

        messages = []
        if new_objects:
            messages.append(f"New object{'s' if len(new_objects) > 1 else ''}: {', '.join(new_objects)}.")
        if lost_objects:
            messages.append(f"Lost object{'s' if len(lost_objects) > 1 else ''}: {', '.join(lost_objects)}.")
        if not messages:
            messages.append(f"Total {len(current_summary)} object{'s' if len(current_summary) != 1 else ''} detected.")
        
        message = ' '.join(messages)
        subprocess.call(['say', message])

        self.previous_summary = current_summary 

if __name__ == "__main__":
    model_path = "objectDetection/models/lite-model/lite-model_efficientdet_lite0_detection_metadata_1.tflite"
    streamer = ObjectDetectionStreamer(model_path=model_path, flip_camera=False)
    streamer.start_stream()