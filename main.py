# Author: Jaydin Freeman
# Date: 03/09/2024

import cv2
import time
import torch
from PIL import Image
from torchvision import transforms, models

torch.backends.quantized.engine = 'qnnpack'

# Create a VideoCapture object
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

ret, image = cap.read()

# Convert the image from OpenCV BGR format to PIL RGB format
image = image[:, :, [2, 1, 0]]

# Display the image using PIL
img = Image.fromarray(image)
img.show()

# Image Preprocessing

preprocess = transforms.Compose([
    # Convert the frame to a CHW torch tensor 
    transforms.ToTensor(),
    # Normalize the colors to the range that mobilenet_v2/3 expects
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


net = models.quantization.mobilenet_v2(pretrained=True, quantize=True)

# jit 
net = torch.jit.script(net)

started = time.time()
last_logged = time.time()
frame_count = 0

with torch.no_grad():
    while True:
        # read the frame
        ret, frame = cap.read()
        if not ret:
            raise RuntimeError("Failed to capture image")
        
        # Convert the frame from OpenCV BGR format to PIL RGB format
        image = frame[:, :, [2, 1, 0]]

        # Preprocess the image
        input_tensor = preprocess(image)

        #  create a mini batch as expected by the model
        input_batch = input_tensor.unsqueeze(0)

        # run the model
        output = net(input_batch)

        # log the model's performance
        frame_count += 1
        now = time.time()
        if now - last_logged > 1:
            print(f"{frame_count / (now - started)} FPS")
            last_logged = now
            frame_count = 0