import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import WebcamModule as wM
import MotorModule as mM

#######################################
steeringSen = 1.2  # Steering Sensitivity
maxThrottle = 0.60  # Forward Speed %
motor = mM.Motor(2, 3, 4, 17, 27, 22)  # Pin Numbers

# Ensure 'mse' is registered correctly
custom_objects = {"mse": MeanSquaredError()}
model = load_model('/home/pi/Desktop/Neural_Network_Demonstartion/model.h5', custom_objects=custom_objects)
######################################

def preProcess(img):
    img = img[54:120, :, :]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img

while True:
    img = wM.getImg(True, size=[240, 120])
    img = np.asarray(img)
    img = preProcess(img)
    img = np.array([img])
    steering = float(model.predict(img))
    print('steering*steerungSen=',steering * steeringSen)
    motor.start(maxThrottle, steering * steeringSen)
    cv2.waitKey(1)