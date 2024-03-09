from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image, ImageDraw
import torch
import cv2
import numpy as np

# Model and device setup
model_path = "models/yolos-tiny"
device = torch.device('cpu') 
processor = YolosImageProcessor.from_pretrained(model_path)
model = YolosForObjectDetection.from_pretrained(model_path).to(device)

def draw_boxes_with_labels(image, results, id2label):
    draw = ImageDraw.Draw(image)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i) for i in box.tolist()]
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)
        draw.text((box[0], box[1]), f"{id2label[label.item()]}: {round(score.item(), 3)}", fill="red")
    return image

def process_frame(frame):
    # Reduce the resolution of the frame to improve performance
    frame_small = cv2.resize(frame, (640, 480))  # Adjust the target resolution as needed
    image = Image.fromarray(cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB))
    inputs = processor(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]]).to(device)
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    annotated_image = draw_boxes_with_labels(image, results, model.config.id2label)
    return cv2.cvtColor(np.array(annotated_image), cv2.COLOR_RGB2BGR)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    for _ in range(10):  # Adjust this value based on performance vs. real-time need
        cap.grab()

    processed_frame = process_frame(frame)
    cv2.imshow('Video with Boxes and Labels', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
