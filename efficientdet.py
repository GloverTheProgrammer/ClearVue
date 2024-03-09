import cv2
import numpy as np
from PIL import Image, ImageDraw
import tensorflow as tf

model_path = "models/lite-model/lite-model_efficientdet_lite0_detection_metadata_1.tflite"
frame_resize_dims = (320, 320) 

skip_frames = 10

interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def draw_boxes_with_labels(image, boxes, classes, scores, labels):
    draw = ImageDraw.Draw(image)
    for box, class_id, score in zip(boxes, classes, scores):
        if score > 0.5:
            ymin, xmin, ymax, xmax = box
            (left, right, top, bottom) = (xmin * image.width, xmax * image.width,
                                          ymin * image.height, ymax * image.height)
            draw.rectangle([(left, top), (right, bottom)], outline="red", width=3)
            label_text = f"{labels.get(class_id, 'N/A')}: {round(score, 3)}"
            draw.text((left, top), label_text, fill="red")

def process_frame(frame, interpreter, input_details, output_details):
    frame_small = cv2.resize(frame, frame_resize_dims)
    frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
    input_data = np.expand_dims(frame_small, axis=0)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    
    image = Image.fromarray(frame_small)
    labels = {0: 'Label 1', 1: 'Label 2'}
    draw_boxes_with_labels(image, boxes, classes, scores, labels)
    
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def main():
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            for _ in range(skip_frames):
                cap.grab()
            processed_frame = process_frame(frame, interpreter, input_details, output_details)
            cv2.imshow('Video with Boxes and Labels', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
