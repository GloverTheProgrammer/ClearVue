from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image, ImageDraw
import torch
import cv2
import numpy as np

# Preload and constant setup
model_path = "models/yolos-tiny"
device = torch.device('cpu') 
processor = YolosImageProcessor.from_pretrained(model_path)
model = YolosForObjectDetection.from_pretrained(model_path).to(device)
frame_resize_dims = (640, 480)  # Reduced resolution for performance
skip_frames = 10  # Adjust based on performance vs. real-time need

def draw_boxes_with_labels(image, results, id2label):
    draw = ImageDraw.Draw(image)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i) for i in box.tolist()]
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)
        label_text = f"{id2label[label.item()]}: {round(score.item(), 3)}"
        draw.text((box[0], box[1]), label_text, fill="red")

def process_frame(frame):
    frame_small = cv2.resize(frame, frame_resize_dims)
    image = Image.fromarray(cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB))
    inputs = processor(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]]).to(device)
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    draw_boxes_with_labels(image, results, model.config.id2label)
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def main():
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            for _ in range(skip_frames):  # Skip frames to decrease processing load
                cap.grab()
            processed_frame = process_frame(frame)
            cv2.imshow('Video with Boxes and Labels', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()