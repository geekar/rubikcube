import cv2
import numpy as np
from rubik_solver import utils

cap = cv2.VideoCapture(0)
# Jetson nano cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink")
cap.set(3, 640)
cap.set(4, 480)
