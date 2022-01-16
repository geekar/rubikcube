#!/usr/bin/python
# -*- coding: utf-8 -*-

import Adafruit_PCA9685
import time

# Initialise the PCA9685 using desired address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)


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
    
openGrips()
closeGrips()
rotateCubeToRight()
