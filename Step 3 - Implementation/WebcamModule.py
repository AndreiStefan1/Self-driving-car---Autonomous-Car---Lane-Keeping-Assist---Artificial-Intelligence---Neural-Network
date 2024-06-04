import cv2
from picamera2 import Picamera2

# Initialize the Picamera2
picam2 = Picamera2()
picam2.preview_configuration.main.size = (240, 120)  # Adjusted size for capture
picam2.preview_configuration.main.format = "RGB888"
picam2.start()

def getImg(display=False, size=[480, 240]):
    # Capture image from the camera
    img = picam2.capture_array()
    img = cv2.resize(img, (size[0], size[1]))
    if display:
        cv2.imshow('IMG', img)
    return img

if __name__ == '__main__':
    while True:
        img = getImg(True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    picam2.stop()
    cv2.destroyAllWindows()