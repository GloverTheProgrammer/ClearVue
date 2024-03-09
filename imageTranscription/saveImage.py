import cv2
import os


def save_image(directory="/home/blackhatDesktop/transcribe/"):
    # Create the directory if it doesn't exist
    
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = os.path.join(directory, f"opencv_frame_{img_counter}.png")
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

save_image()
