"""
@author: alber
"""
import cv2
import numpy as np

colors = {
    'b': ([79, 55, 56], [171, 255, 255]),    # Blue
    'g1': ([40, 80,94], [78, 255, 255]),    # Green
    'g2': ([6, 80, 100], [7, 255, 102]),    # Green
    'g3': ([125,7, 105], [127, 8, 109]),    # Green
    'g4': ([81,14, 55], [170, 32, 65]),    # Green
    'y': ([17, 25, 114], [39, 255, 255]),   # Yellow
    'o1': ([2, 80, 125], [16, 255, 255]),     # Orange
    'o2': ([0, 80, 125], [16, 190, 255]),     # Orange
    'r1': ([0, 90, 20], [2, 255, 255]),     # Red
    'r2': ([1, 161, 20], [1, 255, 255]),     # Red
    'r3': ([172, 100, 20], [180, 255, 255]),     # Red  
    'w': ([0, 0, 190], [255, 255, 255])        #White
    }

def ashFrame(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray
    
def blurredFrame(img):
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    return blurred

def cannyFrame(img):
    threshold1 = 23
    threshold2 = 20
    canny = cv2.Canny(img, threshold1, threshold2)
    return canny

def erodeFrame(img):
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.erode(img, kernel, iterations=2)
    return dilated

def lineexpandFrame(img):
    kernel = np.ones((3,3), np.uint8)
    dilated = cv2.dilate(img, kernel, iterations=2)
    return dilated

def cleanImage(img):
    gray = ashFrame(img)
    blurred = blurredFrame(gray)
    canny = cannyFrame(blurred)
    dilated = lineexpandFrame(canny)
    eroded = erodeFrame(dilated)
    return eroded

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
                face.append(piece)
    return face

def findsCandidateEdges(img):
    contours,hierarchy  = cv2.findContours(img.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    index = 0
    pieces = []
    face = {}
    final_contours = []
    maxAreaFound = 0
    # Step 1/4: filter all contours to only those thcaptureRubikFace()at are square-ish shapes.
    for contour in contours:
        area = cv2.contourArea(contour)
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
        
    if (len(final_contours) < 9) or (maxAreaFound <  areaMin): 
        return []
    print("More than 8 squares detected and big Sqare Detected!")
    
    return pieces

def detectFacefromImage(img):
    cleanImage(img)
    detected = false
    while (not detected):
        face = findsCandidateEdges(img)
        if (len(face)==9):
            detected = true
    return face

def buildStringFace(pieces):
    str = ''
    if (len(pieces) != 9):
        str = "Error face not well build!"
    else:
        colors = []
        for piece in pieces:
            (x, y, radius,  color ) = piece
            colors.append(color)
        template = ("{}{}{}{}{}{}{}{}{}")
        str=  template.format(*colors).strip()
    return str
    
def drawDetectedFace(img, face):
    for piece in face:
        (x, y, radius,   color) = piece
        cv2.putText(img,color,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
    return img

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

def captureRubikFace():
    ret,frame = cap.read()
    face = []
    if (ret == True):
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        face = detectFacefromImage(frameHSV)
    return face    
