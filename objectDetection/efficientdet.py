import cv2
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf
from Object_Detection.labels import classes

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
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def start_stream(self):
        cap = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                for _ in range(self.skip_frames):
                    cap.grab()
                processed_frame = self.process_frame(frame)
                cv2.imshow('Video with Boxes and Labels', processed_frame)
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


if __name__ == "__main__":
    model_path = "models/lite-model/lite-model_efficientdet_lite0_detection_metadata_1.tflite"
    streamer = ObjectDetectionStreamer(model_path=model_path, flip_camera=True)
    streamer.start_stream()