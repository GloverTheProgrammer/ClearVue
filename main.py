# Author: Jaydin Freeman
# Date: 03/09/2024

import cv2
import time
import torch
from torchvision import transforms, models
from labels import classes

torch.backends.quantized.engine = 'qnnpack'
net = models.quantization.mobilenet_v3_large(pretrained=True, quantize=True)
net = torch.jit.script(net)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)

preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

frame_count = 0
started = time.time()
last_logged = time.time()

with torch.no_grad():
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit if failed to grab a frame

        # Preprocess without converting to RGB
        # Convert BGR to RGB here
        input_tensor = preprocess(frame[..., ::-1].copy())
        input_batch = input_tensor.unsqueeze(0)
        output = net(input_batch)

        # Added code starts here
        top = list(enumerate(output[0].softmax(dim=0)))
        top.sort(key=lambda x: x[1], reverse=True)
        for idx, val in top[:10]:
            print(f"{val.item()*100:.2f}% {classes[idx]}")

        frame_count += 1
        now = time.time()
        if now - last_logged > 1:
            print(f"{frame_count / (now-last_logged)} fps")
            last_logged = now
            frame_count = 0

cap.release()