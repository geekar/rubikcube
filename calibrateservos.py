#!/usr/bin/python
# -*- coding: utf-8 -*-

import Adafruit_PCA9685
import time

# Initialise the PCA9685 using desired address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address = 0x40, busnum = 1)


def offset(grados):
	return (round ((servo_max - servo_min) * grados / 180))

def moveForward(servo,grados):
	return pwm.set_pwm(servo, 0, servo_min+offset(grados))

def moveBackward(servo,grados):
	return pwm.set_pwm(servo, 0, servo_max-offset(grados))


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
servo_offset =  offset(90) # 90 grados
print(servo_offset)
# Set frequency to 60[Hz]
pwm.set_pwm_freq(60)

moveForward(leftwristservo,0)
time.sleep(1)
moveForward(leftwristservo,90)
time.sleep(1)
moveForward(leftwristservo,180)
time.sleep(1)
moveForward(leftwristservo,0)
time.sleep(1)

""""
for i in range(180):
	moveForward(servo_num,i)
	time.sleep(0.03)

for i in range(180):
	moveBackward(servo_num,i)
	time.sleep(0.03)

moveForward(servo_num,0)
time.sleep(1)
moveForward(servo_num,45)
time.sleep(1)
moveForward(servo_num,90)
time.sleep(1)
moveForward(servo_num,135)
time.sleep(1)
moveForward(servo_num,180)
time.sleep(1)
moveBackward(servo_num,45)
time.sleep(1)
moveBackward(servo_num,90)
time.sleep(1)
moveBackward(servo_num,135)
time.sleep(1)
moveBackward(servo_num,180)
time.sleep(1)

while True:
	print('Moving servo on channel: ', servo_num)
	pwm.set_pwm(servo_num, 0, servo_min + servo_offset)
	time.sleep(2)
	print('Moving servo on channel: ', servo_num)
	pwm.set_pwm(servo_num, 0, servo_max - servo_offset)
	time.sleep(2)
"""
