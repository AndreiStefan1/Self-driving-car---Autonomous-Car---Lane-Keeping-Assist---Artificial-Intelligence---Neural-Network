import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor():
    def __init__(self,EnA,In1,In2,In3,In4,EnB):
        self.EnA= EnA
        self.In1 = In1
        self.In2 = In2
        self.EnB= EnB
        self.In3 = In3
        self.In4 = In4
        #Motoare stanga
        GPIO.setup(self.EnA,GPIO.OUT)
        GPIO.setup(self.In1,GPIO.OUT)
        GPIO.setup(self.In2,GPIO.OUT)
        #Motoare dreapta
        GPIO.setup(self.EnB,GPIO.OUT)
        GPIO.setup(self.In3,GPIO.OUT)
        GPIO.setup(self.In4,GPIO.OUT)
        self.pwmA = GPIO.PWM(self.EnA, 100);
        self.pwmB = GPIO.PWM(self.EnB, 100);
        self.pwmA.start(0);
        self.pwmB.start(0);

    def start(self,viteza=50,viraj=0,t=0):

        #if (viteza < 60): viteza = 60
        #if (viteza > 85): viteza = 85

        vitezastanga = viteza+viraj
        vitezadreapta = viteza-viraj

        if vitezastanga>100: vitezastanga =100
        elif vitezastanga<0: vitezastanga = 0
        if vitezadreapta>100: vitezadreapta =100
        elif vitezadreapta<0: vitezadreapta = 0
        print('vitezastanga' , vitezastanga)
        print('vitezadreapta' , vitezadreapta)
        sleep(0.5)

        self.pwmA.ChangeDutyCycle(abs(vitezastanga))
        self.pwmB.ChangeDutyCycle(abs(vitezadreapta))

        GPIO.output(self.In1,GPIO.LOW);GPIO.output(self.In2,GPIO.HIGH)
        GPIO.output(self.In3,GPIO.HIGH);GPIO.output(self.In4,GPIO.LOW)

        sleep(t)

    def stop(self,t=0):
        self.pwmA.ChangeDutyCycle(0);
        self.pwmB.ChangeDutyCycle(0);
        sleep(t)

def main():
   Motor.start(60,0,3)
   Motor.stop(2)

if __name__ == '__main__':
    Motor= Motor(2,3,4,17,27,22)
    main()