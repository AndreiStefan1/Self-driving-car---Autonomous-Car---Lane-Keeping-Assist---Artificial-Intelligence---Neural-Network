# Lane-Assist-System---Autonomous-Car
Implementation of a real Lane Assist system on a project car . The car is using a Raspberry Pi and a dedicated camera to follow any given route . The whole project is based on image processing made possible by using NumPy and OpenCV libraries. 

## Components of the car : 
- Raspberry Pi 4B
- Raspberry camera Pi V1.3
- 5.000 mAh external baterry to power the Raspbery Pi microprocessor 
- L298N DC Motor Driver 
- 4 AAA batteries to power up the engines and L298N DC Motor Driver
- 4x D.C motors ~ 3V-6V 


## The concept 
Image processing is the use of a digital computer to process digital images through an algorithm. In this case we use a microprocessor (Raspberry PI 4) to make the process possible . In order for the process to work , the road must be white (or if any other color is chosed , then the color coordinates should be changed in the HSV color space). The camera should be positioned high and centered. 
