import cv2
from PIL import Image

# Create a VideoCapture object

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 224)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 224)
cap.set(cv2.CAP_PROP_FPS, 36)

ret, image = cap.read()
cap.release()

# Convert the image from OpenCV BGR format to PIL RGB format
image = image[:, :, [2, 1, 0]]

# Display the image using PIL
img = Image.fromarray(image)
img.show()
