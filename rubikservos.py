#!/usr/bin/python
# -*- coding: utf-8 -*-

import Adafruit_PCA9685
import time
import RPi.GPIO as GPIO
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Initialise the PCA9685 using desired address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)
# Initialise the GPIO to use push buttons
GPIO.setmode(GPIO.BOARD)
# jetson nano startButton=15

startButton=16
GPIO.setup(startButton, GPIO.IN)

#Initialize display 128x64
RST= None
SCL=32
SDA=31
disp=Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_bus=1, gpio=1)
disp.begin()
disp.clear()
disp.display()



def offset(grados):
	return (round ((servo_max - servo_min) * grados / 180))



# Number of serv 
leftwristservo = 0
rightwristservo = 1
leftgripservo = 2
rightgripservo = 3


# Configure min and max servo pulse lengths
servo_min    = 132 # min. pulse length - 0
servo_max    = 635 # max. pulse length -180#
#servo_max    = 1270 # max. pulse length -180#
#servo_offset = 251 # 90
# Set frequency to 60[Hz]
pwm.set_pwm_freq(60)

## WRIST CORE SERVO FUNCTIONS
def moveForward(servo,grados):
	return pwm.set_pwm(servo, 0, servo_min+offset(grados))

def moveBackward(servo,grados):
	return pwm.set_pwm(servo, 0, servo_max-offset(grados))

## GRIP CORE SERVO FUNCTIONS
def openLeftGrip():
    for i in range(45):
        moveForward(leftgripservo,i)
        time.sleep(0.03)
 
def closeLeftGrip():
    for i in range(45):
        moveForward(leftgripservo,45-i)
        time.sleep(0.03) 

def openRightGrip():
    for i in range(35):
        moveForward(rightgripservo,i)
        time.sleep(0.03)
        
def closeRightGrip():
    for i in range(35):
        moveForward(rightgripservo,35-i)
        time.sleep(0.03)        
        
##  RUBIK ROBOT MOVEMENT FUNCTIONS    
def openGrips():
    moveForward(leftwristservo,0)
    moveForward(rightwristservo,0)
    openLeftGrip()
    openRightGrip()
    
def closeGrips():
    moveForward(leftwristservo,0)
    moveForward(rightwristservo,0)
    closeLeftGrip()
    closeRightGrip()
    
def rotateCubeToRight():
    moveForward(rightgripservo,0)
    openLeftGrip()
    moveForward(rightwristservo,90)
    closeLeftGrip()
    openRightGrip()
    moveForward(rightwristservo,0)
    closeRightGrip()
    
def start():
    print("Starting cube detection")
    openGrips()
    closeGrips()

def stop():
    print("Stop cube detection")
    openGrips()
    
def drawInit():
    width=disp .width
    height=disp.height
    image=Image.new('1', (width, height))
    draw=ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    padding=-2
    top=padding
    bottom=height-padding
    return draw,  image

def drawText(str, draw, image):
    width=disp .width
    height=disp.height
    padding=-2
    top=padding
    x=0
    font=ImageFont.load_default()
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((x, top), str, font=font,  fill=255)
    disp.image(image)
    disp.display()
    time.sleep(.1)
 
draw, image = drawInit() 
while True:
    startValue= GPIO.input(startButton)
    drawText("hola", draw, image)
    if (startValue== 0):
        start()
        drawText("adios", draw, image)
        GPIO.cleanup(startButton)
        exit()
    else: 
        stop()
    
 
GPIO.cleanup(startButton)
 
openGrips()
closeGrips()
rotateCubeToRight()

