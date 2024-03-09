from transformers import YolosImageProcessor, YolosForObjectDetection
from PIL import Image, ImageDraw
import torch
import cv2
import numpy as np

# Load the processor and model with torch.device for optimization on Raspberry Pi
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny").to(device)

def draw_boxes_with_labels(image, results, id2label):
    draw = ImageDraw.Draw(image)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i) for i in box.tolist()]
        draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)
        draw.text((box[0], box[1]), f"{id2label[label.item()]}: {round(score.item(), 3)}", fill="red")
    return image

def process_frame(frame):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    inputs = processor(images=image, return_tensors="pt").to(device)
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]]).to(device)
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    annotated_image = draw_boxes_with_labels(image, results, model.config.id2label)
    return cv2.cvtColor(np.array(annotated_image), cv2.COLOR_RGB2BGR)

cap = cv2.VideoCapture(0)
cv2.setNumThreads(4)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    processed_frame = process_frame(frame)
    cv2.imshow('Video with Boxes and Labels', processed_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
