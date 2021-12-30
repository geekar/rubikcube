# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 17:23:58 2021

@author: alber
"""
import cv2
import numpy as np
from rubik_solver import utils

font = cv2.FONT_HERSHEY_SIMPLEX


def detectColor(h,s,v):
   #print("color=")
    #print(h)
    #print(s)
    #print(v)
    for color, (lower, upper) in colors.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        if (lower[0] <= h and upper[0] >= h) and (lower[1] <= s and upper[1] >= s) and (lower[2] <= v and upper[2] >= v):
            if (len(color)==2):
                color = color[:1]
            return color
    return 'w'
    

def getColorName(img,x,y):
    h,s,v=img[y,x]
    color = detectColor(h,s,v)
   # print("h={}, s={}, v={}, color={} ".format(h,s,v,color))
    return color
    
def debugDetectedFace(img, face):
    for piece in face:
        #cnts.append(component.get('contour'))
        (x, y, radius,   color) = piece
       # radius = piece.get('radius')
       # cv2.circle(img,(x,y), radius, (0,0,255), 2)
        color2 = getColorName(img,x,y)
        h,s,v=img[y,x]
        texto = "h="+str(h)+" s="+str(s)+" v="+str(v)+" color="+color2
        print(texto)
       # print(color,end='')
       # print('')
   #cv2.drawContours(img, face.get('contour'), -1, (0, 0, 255), 3)   
    
def drawDetectedFace(img, face):
    for piece in face:
        #cnts.append(component.get('contour'))
        (x, y, radius,   color) = piece
       # radius = piece.get('radius')
       # cv2.circle(img,(x,y), radius, (0,0,255), 2)
        #color2 = getColorName(img,x,y)
       # h,s,v=img[y,x]
        #texto = "h="+str(h)+" s="+str(s)+" v="+str(v)+" color="+color2
       # print(texto)
        cv2.putText(img,color,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
       # print(color,end='')
       # print('')
   #cv2.drawContours(img, face.get('contour'), -1, (0, 0, 255), 3)
        
    return img

def buildFace(pieces):
    str = ''
    if (len(pieces) != 9):
        str = "Error face not well build!"
    else:
        colors = []
        for piece in pieces:
            (x, y, radius,  color ) = piece
            colors.append(color)
            
#        templatePrint = ("    {}{}{}\n"
#                    "    {}{}{}\n"
#                    "    {}{}{}\n"
#                    )
        
        template = ("{}{}{}{}{}{}{}{}{}")
       
        str=  template.format(*colors).strip()
    print(str)
    return str

    

def ashFrame(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   # cv2.imshow("image", gray)
    return gray
    
def blurredFrame(img):
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
   # blurred = img
  #  cv2.imshow("blurred", blurred)
    return blurred

def cannyFrame(img):
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
#    threshold1 = 23
#    threshold2 = 20

    canny = cv2.Canny(img, threshold1, threshold2)
    cv2.imshow("canny", canny)
    return canny

def erodeFrame(img):
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.erode(img, kernel, iterations=2)
    cv2.imshow("erode", dilated)
    return dilated

def lineexpandFrame(img):
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(img, kernel, iterations=2)
    cv2.imshow("expand", dilated)
    return dilated

def findPieces(cx,cy,perimeter,frame):
    longBigSquare = perimeter/4
    l = longBigSquare/4
    face = []
    radius = int(l/2)
    
   
    for j in (-1, 0, 1):
        for i  in (-1, 0, 1):
            x = int(i*l + cx)
            y = int(j*l + cy)
            if (x>0) and (x<640) and (y>0) and (y<480):
                color =  getColorName(frame,x,y)
                piece = (x, y, radius, color)
                #piece = {'x': x, 'y': y, 'radius': radius, 'color':color}
                face.append(piece)
     
    return face
    

    
        

def findsCandidateEdges(img,imgHSV,face):
#    (contours, hierarchy) = cv2.findContours(img.copy(),
#                                         cv2.RETR_TREE,
#                                         cv2.CHAIN_APPROX_SIMPLE)
   
    #contours,hierarchy  = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    contours,hierarchy  = cv2.findContours(img.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
  
    index = 0
    pieces = []
    face = {}
    final_contours = []
    maxAreaFound = 0
    # Step 1/4: filter all contours to only those that are square-ish shapes.
    for contour in contours:
        area = cv2.contourArea(contour)
#        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        areaMin=12000
        areaMax=120000
        if (areaMax > area):
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * peri, True)
            corners = len(approx)
            x,y,w,h = cv2.boundingRect(approx)
            if corners==4:                   
                aspect_ratio = float(w)/h 
                if aspect_ratio > 0.8 and aspect_ratio < 1.2:
                    
                    # compute the center of the contour
                    M = cv2.moments(contour)
                
                    if M["m00"]:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                    else:
                        cX = None
                        cY = None
                
                   # if areaMin < area < areaMax and cX is not None:
                    color =  getColorName(frameHSV,cX,cY)
                    square = (x,y,w,h, color)
                    if (area  >  maxAreaFound):
                        maxAreaFound = area
                        pieces =  findPieces(cX,cY,peri,frameHSV)          
                        
                   # if w >= 30 and w <= 60 and area / (w * h) > 0.4:
                    if area / (w * h) > 0.4:
                        final_contours.append(square)
                    
                   #pieces =  findPieces(cX,cY,peri,frameHSV)
                    
                    #face = {'index': index, 'cx': cX, 'cy': cY, 'contour': approx, 'color':color}
        
    if (len(final_contours) < 9) or (maxAreaFound <  areaMin): 
        return []
    print("More than 8 squares detected and big Sqare Detected!")
    
    return pieces
    
 

def empty(a):
    pass

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)960,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink")
cap.set(3, 640)
cap.set(4, 480)

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",0,255,empty)
cv2.createTrackbar("Threshold2","Parameters",115,255,empty)
cv2.createTrackbar("Area","Parameters",15000,80000,empty)


#ret,frame =  cap.read()
#image = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#original = image.copy()

#mask = np.zeros(image.shape, dtype=np.uint8)

colors = {
    'b': ([79, 50, 56], [171, 255, 255]),    # Blue
    'g1': ([40, 80,94], [78, 255, 255]),    # Green
    'g2': ([6, 80, 100], [7, 255, 102]),    # Green
    'g3': ([125,7, 105], [127, 8, 109]),    # Green
    'g4': ([81,14, 55], [170, 32, 65]),    # Green
    'y': ([17, 25, 114], [39, 255, 255]),   # Yellow
    'o1': ([2, 80, 125], [16, 255, 255]),     # Orange
    'o2': ([0, 80, 125], [16, 160, 255]),     # Orange
    'r1': ([0, 90, 20], [2, 255, 255]),     # Red
    'r2': ([1, 161, 20], [1, 255, 255]),     # Red
    'r3': ([172, 100, 20], [180, 255, 255]),     # Red  
    'w': ([0, 0, 190], [255, 255, 255])        #White
    }

strCube = ''
face = []
i = 0
numFaces = 0
cube = 'oyyoyyoyygggggggggwoowoowoobbbbbbbbbrryrryrryrwwrwwrww'
print(utils.solve(cube, 'Kociemba'))
while True:
  ret,frame = cap.read()
  if ret == True:
    frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    gray = ashFrame(frame)
    blurred = blurredFrame(gray)
    canny = cannyFrame(blurred)
    dilated = lineexpandFrame(canny)
    eroded = erodeFrame(dilated)
    face = findsCandidateEdges(eroded,frameHSV,face)
    debugDetectedFace(frameHSV, face)
    frame = drawDetectedFace(frame, face)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        if (len(face) == 9):
            strCube = strCube+buildFace(face)
            numFaces = numFaces +1
            face.clear()
            while cv2.waitKey(1) & 0xFF != ord('s'):
                continue
        if (numFaces == 6):
            numFaces = 0
            print("Cubo:")
            print(strCube)
            print(utils.solve(strCube, 'Kociemba'))
            
        
#    if cv2.waitKey(1) & 0xFF == ord('s'):
#      break

cap.release()
cv2.destroyAllWindows()
# Color threshold to find the squares


  

cv2.waitKey()

