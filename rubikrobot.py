#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: alber
"""
import numpy as np
import Adafruit_PCA9685
import time
import RPi.GPIO as GPIO
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from rubik_solver import utils
import rubikfacedetection
from rubikfacedetection import *

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
    centerWrist(leftwristservo)
    centerWrist(rightwristservo)
    openLeftGrip()
    openRightGrip()
    
def closeGrips():
    centerWrist(leftwristservo)
    centerWrist(rightwristservo)
    closeLeftGrip()
    closeRightGrip()
    
def rotateCubeToRight():
    closeRightGrip()
    openLeftGrip()
    time.sleep(0.5)
    turnWrist(rightwristservo)
    time.sleep(0.5)
    closeLeftGrip()
    time.sleep(1)
    openRightGrip()
    time.sleep(1)
    centerWrist(rightwristservo)
    time.sleep(0.5)
    closeRightGrip()
    
    
def rotateCubeToLeft():
    closeRightGrip()
    openLeftGrip()
    time.sleep(0.5)
    turnPrimaWrist(rightwristservo)
    time.sleep(0.5)
    closeLeftGrip()
    time.sleep(1)
    openRightGrip()
    time.sleep(1)
    centerWrist(rightwristservo)
    time.sleep(0.5)
    closeRightGrip()

def rotateCubeUpToRight():
    closeLeftGrip()
    openRightGrip()
    time.sleep(0.5)
    turnPrimaWrist(leftwristservo)
    time.sleep(0.5)
    closeRightGrip()
    time.sleep(1)
    openLeftGrip()
    time.sleep(1)
    centerWrist(leftwristservo)
    time.sleep(0.5)
    closeLeftGrip()
    

def rotateCubeUpToLeft():
    closeLeftGrip()
    openRightGrip()
    time.sleep(0.5)
    turnWrist(leftwristservo)
    time.sleep(0.5)
    closeRightGrip()
    time.sleep(1)
    openLeftGrip()
    time.sleep(1)
    centerWrist(leftwristservo)
    time.sleep(0.5)
    closeLeftGrip()
    
def rotateCubeToFront():
    rotateCubeUpToRight()
    rotateCubeToLeft()
    rotateCubeUpToRight()
    

def D_movement():
    closeRightGrip()
    turnWrist(rightwristservo)
    time.sleep(0.5)
    openRightGrip()
    time.sleep(1)
    centerWrist(rightwristservo)
    closeRightGrip()

def Dprima_movement():
    closeRightGrip()
    turnPrimaWrist(rightwristservo)
    time.sleep(0.5)
    openRightGrip()
    time.sleep(1)
    centerWrist(rightwristservo)
    closeRightGrip()
    
def Ddouble_movement():
    D_movement()
    D_movement()
    
def B_movement():
    closeLeftGrip()
    turnWrist(leftwristservo)
    time.sleep(0.5)
    openLeftGrip()
    time.sleep(1)
    centerWrist(leftwristservo)
    closeLeftGrip()

def Bprima_movement():
    closeLeftGrip()
    turnPrimaWrist(leftwristservo)
    time.sleep(0.5)
    openLeftGrip()
    time.sleep(1)
    centerWrist(leftwristservo)
    closeLeftGrip()

def Bdouble_movement():
    B_movement()
    B_movement()
    
def L_movement():
    rotateCubeUpToLeft()
    time.sleep(1)
    D_movement()
    time.sleep(1)
    rotateCubeUpToRight()

def Lprima_movement():
    rotateCubeUpToLeft()
    time.sleep(1)
    Dprima_movement()
    time.sleep(1)
    rotateCubeUpToRight()
    
def Ldouble_movement():
    rotateCubeUpToLeft()
    time.sleep(1)
    D_movement()
    D_movement()
    time.sleep(1)
    rotateCubeUpToRight()
    
def R_movement():
    rotateCubeUpToRight()
    time.sleep(1)
    D_movement()
    time.sleep(1)
    rotateCubeUpToLeft()

def Rprima_movement():
    rotateCubeUpToRight()
    time.sleep(1)
    Dprima_movement()
    time.sleep(1)
    rotateCubeUpToLeft()

def Rdouble_movement():
    rotateCubeUpToRight()
    time.sleep(1)
    D_movement()
    D_movement()
    time.sleep(1)
    rotateCubeUpToLeft()  
    
def U_movement():
    rotateCubeUpToRight()
    rotateCubeUpToRight()
    time.sleep(1)
    D_movement()
    time.sleep(1)
    rotateCubeUpToLeft()
    rotateCubeUpToLeft()
    
def Uprima_movement():
    rotateCubeUpToRight()
    rotateCubeUpToRight()
    time.sleep(1)
    Dprima_movement()
    time.sleep(1)
    rotateCubeUpToLeft()
    rotateCubeUpToLeft()
    
def Udouble_movement():
    rotateCubeUpToRight()
    rotateCubeUpToRight()
    time.sleep(1)
    D_movement()
    D_movement()
    time.sleep(1)
    rotateCubeUpToLeft()
    rotateCubeUpToLeft()    
    
def F_movement():
    rotateCubeToRight()
    rotateCubeToRight()
    time.sleep(1)
    B_movement()
    time.sleep(1)
    rotateCubeUpToLeft()
    rotateCubeUpToLeft()

def Fprima_movement():
    rotateCubeToRight()
    rotateCubeToRight()
    time.sleep(1)
    Bprima_movement()
    time.sleep(1)
    rotateCubeUpToLeft()
    rotateCubeUpToLeft()
    
def Fdouble_movement():
    rotateCubeToRight()
    rotateCubeToRight()
    time.sleep(1)
    B_movement()
    B_movement()
    time.sleep(1)
    rotateCubeUpToLeft()
    rotateCubeUpToLeft()    
    
def start():
    print("Starting cube detection")
    closeGrips()

def stop():
    print("Stop cube detection")
    openGrips()
    
def test():
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
    
def test2():
    time.sleep(2)
    R_movement()
    time.sleep(1)
    openGrips()
    time.sleep(10)
    
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
    
def movement(letter):
    switcher = {
       "L": L_movement(),
       "L'": Lprima_movement(),
       "L2": Ldouble_movement(),
       "R": R_movement(),
       "R'": Rprima_movement(),
       "R2": Rdouble_movement(),
       "U": U_movement(),
       "U'": Uprima_movement(),
       "U2": Udouble_movement(),
       "D": D_movement(),
       "D'": Dprima_movement(),
       "D2": Ddouble_movement(),
       "F": F_movement(),
       "F'": Fprima_movement(),
       "F2": Fdouble_movement(),
       "B": B_movement(),
       "B'": Bprima_movement(),
       "B2": Bdouble_movement(),       
    }
    return switcher.get(letter, "Invalid Operation! Please try again.")

def solve(solution):
    for letter in solution:
        movement(letter)
        
def formatFacesToStr(faces):
    strCube = ""
    for face in faces:
        strCube = strCube + buildStringFace(face)
    return strCube    
        
def captureRubikFaces():
#     strCube = ""
#     face = captureRubikFace()
#     strCube = strCube + buildStringFace(face)
    faces = np.empty(6, dtype=object)
    ##First face
    face[0] = captureRubikFace()
    ##Second face
    rotateCubeToRight()
    face[1] = captureRubikFace()
    ##Third face
    rotateCubeToRight()
    face[2] = captureRubikFace()
    ##Fourth face
    rotateCubeToRight()
    face[3] = captureRubikFace()
    ##Fifth face
    rotateCubeUpToFront()
    face[4] = captureRubikFace()
    ##Sixth face
    rotateCubeToRight()
    rotateCubeToRight()
    face[5] = captureRubikFace()
    rotateCubeUpToFront()
    rotateCubeToRight()
    cube = formatFacesToStr(faces)
    return cube





draw, image = drawInit()
cube = 'oyyoyyoyygggggggggwoowoowoobbbbbbbbbrryrryrryrwwrwwrww'
solution = utils.solve(cube, 'Kociemba')
print(solution)
#movement(solution)
faces = np.empty(1, dtype=object)
faces[0] = captureRubikFace()
print(buildStringFace(faces[0]))
drawText(buildStringFace(faces[0]), draw, image)

exit()

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
        test2()
#         Bprima_movement()
#         time.sleep(1)
#         openGrips()
#         time.sleep(10)
      

    

    
 
GPIO.cleanup(startButton)
openGrips()
closeGrips()
rotateCubeToRight()

