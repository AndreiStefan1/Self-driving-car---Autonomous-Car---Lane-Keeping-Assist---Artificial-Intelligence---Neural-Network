import WebcamModule as wM
import DataCollectionModule as dcM
import JoyStickModule3 as jsM
import MotorModule as mM
import cv2
from time import sleep

motor = mM.Motor(2, 3, 4, 17, 27, 22)

record = 0
while True:
    joyVal = jsM.getJS()
    steering = joyVal['axis4']*100
    throttle = joyVal['axis2']*60
    print('throttle=',throttle)
    print('steering=', steering)
    if joyVal['A'] == 1:
        if record == 0:
            print('Recording Started ...')
            record = 1
            sleep(0.300)
        elif record == 1:
            print('Recording Stopping ...')
            dcM.saveLog()  # Save log when stopping recording
            record = 0

    if record == 1:
        img = wM.getImg(True, size=[240, 120])
        dcM.saveData(img, steering)

    motor.start(-throttle, steering)
    cv2.waitKey(1)