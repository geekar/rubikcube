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

leftgripclosed = False
rightgripclosed = False
leftwristturned = False
leftwristcenter = False



def offset(grados):
	return (round ((servo_max - servo_min) * grados / 180))

def offsetgrip(grados):
	return (round ((servo_max_grip - servo_min_grip) * grados / 180))



# Number of serv 
leftwristservo = 0
rightwristservo = 1
leftgripservo = 2
rightgripservo = 3


# Configure min and max servo pulse lengths
servo_min    = 132 # min. pulse length - 0
servo_max    = 650 # max. pulse length -180#
servo_min_grip    = 132 # min. pulse length - 0
servo_max_grip    = 700 # max. pulse length -180#
#servo_max    = 1270 # max. pulse length -180#
#servo_offset = 251 # 90
# Set frequency to 60[Hz]
pwm.set_pwm_freq(60)

## WRIST CORE SERVO FUNCTIONS
def moveForward(servo,grados):
    print(servo_min+offset(grados))
    return pwm.set_pwm(servo, 0, servo_min+offset(grados))

def moveBackward(servo,grados):
	return pwm.set_pwm(servo, 0, servo_max-offset(grados))

def moveForwardGrips(servo,grados):
	return pwm.set_pwm(servo, 0, servo_min_grip+offsetgrip(grados))

## GRIP CORE SERVO FUNCTIONS
def openLeftGrip():
    global leftgripclosed
    if leftgripclosed:
        for i in range(30):
            moveForwardGrips(leftgripservo,i)
            time.sleep(0.02)
        leftgripclosed = False
    else:
        moveForwardGrips(leftgripservo,30)    
 
def closeLeftGrip():
    global leftgripclosed
    if not leftgripclosed:
        for i in range(30):
            moveForwardGrips(leftgripservo,30-i)
            time.sleep(0.02)
        leftgripclosed = True
    else:
        moveForwardGrips(leftgripservo,0)

def openRightGrip():
    global rightgripclosed
    if rightgripclosed:    
        for i in range(30):
            moveForwardGrips(rightgripservo,i)
            time.sleep(0.02)
        rightgripclosed = False
    else:
        moveForwardGrips(rightgripservo,30)
    
        
def closeRightGrip():
    global rightgripclosed
    if not rightgripclosed:    
        for i in range(30):
            moveForwardGrips(rightgripservo,30-i)
            time.sleep(0.02)
        rightgripclosed = True
    else:
        moveForwardGrips(rightgripservo,0)
        
def turnWrist(servo):
    moveForward(servo,180)
    

def turnPrimaWrist(servo):
    moveForward(servo,0)
                
def centerWrist(servo):
    moveForward(servo,90)
    

def centerLeftWrist():
    global leftwristcenter
    if not leftwristcenter:    
        for i in range(90):
            moveForward(leftwristservo,i)
            time.sleep(0.03)
        leftwristcenter = True
    else:
        moveForward(leftwristservo,0)   
        
##  RUBIK ROBOT MOVEMENT FUNCTIONS    
def openGrips():
    moveForward(leftwristservo,90)
    moveForward(rightwristservo,90)
    openLeftGrip()
    openRightGrip()
    
def closeGrips():
    moveForward(leftwristservo,0)
    moveForward(rightwristservo,0)
    closeLeftGrip()
    closeRightGrip()
    
def rotateCubeToRight():
    closeRightGrip()
    openLeftGrip()
    time.sleep(0.5)
    moveForward(rightwristservo,90)
    time.sleep(0.5)
    closeLeftGrip()
    time.sleep(1)
    openRightGrip()
    time.sleep(1)
    moveForward(rightwristservo,0)
    time.sleep(0.5)
    closeRightGrip()

def D_movement():
    closeRightGrip()
    moveForward(rightwristservo,90)
    time.sleep(0.5)
    openRightGrip()
    time.sleep(1)
    moveForward(rightwristservo,0)
    closeRightGrip()

def Dprima_movement():
    closeRightGrip()
    moveBackward(rightwristservo,90)
    time.sleep(0.5)
    openRightGrip()
    time.sleep(1)
    moveForward(rightwristservo,0)
    closeRightGrip()
    
def start():
    print("Starting cube detection")
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
openGrips()
while True:
    startValue= GPIO.input(startButton)
    drawText("hola", draw, image)
    if (startValue== 0):
        #rotateCubeToRight()
        #D_movement()
        #moveForward(rightwristservo,0)
        pwm.set_pwm(rightwristservo, 0, servo_min)
        time.sleep(5)
        stop()
        drawText("adios", draw, image)
        GPIO.cleanup(startButton)
        exit()
    else:
        openRightGrip()
        time.sleep(2)
        closeRightGrip()
        turnWrist(rightwristservo)
        time.sleep(2)
        centerWrist(rightwristservo)
        time.sleep(2)
        turnPrimaWrist(rightwristservo)
        time.sleep(2)
        centerWrist(rightwristservo)
        time.sleep(2)
        openRightGrip()
        centerWrist(leftwristservo)
        openLeftGrip()
        time.sleep(2)
        closeLeftGrip()
        turnWrist(leftwristservo)
        time.sleep(2)
        centerWrist(leftwristservo)
        time.sleep(2)
        turnPrimaWrist(leftwristservo)
        time.sleep(2)
        centerWrist(leftwristservo)
        time.sleep(2)
       
      

    

    
 
GPIO.cleanup(startButton)
openGrips()
closeGrips()
rotateCubeToRight()

