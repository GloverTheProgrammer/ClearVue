import cv2
import os


def save_image(directory="/home/blackhatDesktop/transcribe/"):
    # Create the directory if it doesn't exist
    
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    ret, frame = cam.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        return
    
    img_name = os.path.join(directory, f"opencv_frame.png")
    cv2.imwrite(img_name, frame)
    print(f"{img_name} written!")

    cam.release()
