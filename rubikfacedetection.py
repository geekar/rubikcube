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

def detectColor(h,s,v):
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


def vickNeshFrame(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    gray = cv2.adaptiveThreshold(gray,40,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,5,0)
    return gray

def ashFrame(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray
    
def blurredFrame(img):
    blurred = cv2.blur(img, (3, 3), 2)
    return blurred

def cannyFrame(img):
#    threshold1 = 20
#    threshold2 = 30
#    threshold1 = 25
#    threshold2 = 25
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    canny = cv2.Canny(img, threshold1, threshold2,3)
    return canny

def erodeFrame(img):
    #kernel = np.ones((3,3), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
    dilated = cv2.erode(img, kernel, iterations=2)
    return dilated

def lineexpandFrame(img):
    #kernel = np.ones((3,3), np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))
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

def findMinimumPiece(pieces):
    minimumPiece = (5000,5000,3,(255,0,0))
    (xmin, ymin, radiusmin,  colormin ) = minimumPiece
    pos = 0
    position = pos
    valorMinPiece = 500000
    for piece in pieces:
        (x, y, radius, color ) = piece
        valorPiece = y*10
        valorPiece = x + valorPiece
        if (valorPiece < valorMinPiece):
             minimumPiece = piece
             position = pos
             valorMinPiece = valorPiece
        pos = pos+1
    return minimumPiece,position         
         

def sortPieces(pieces):
    orderedPieces = []
    while (len(orderedPieces)!=9):
        minimumPiece,position = findMinimumPiece(pieces)
        print("--")
        print(minimumPiece)
        orderedPieces.append(minimumPiece)
        del pieces[position]       
    return orderedPieces
                



def findsCandidateEdges(img,frameHSV):
    contours,hierarchy  = cv2.findContours(img.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#     contours,hierarchy  = cv2.findContours(img.copy(), cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
    index = 0
    pieces = []
    face = {}
    final_contours = []
    maxAreaFound = 0
    
    areaMin=10000
#     areaMax=1200000
    areaMax = cv2.getTrackbarPos("AreaMax", "Parameters")
    
    i = 0

    print("******************")
    # Step 1/4: filter all contours to only those thcaptureRubikFace()at are square-ish shapes.
    for contour in contours:
        area = cv2.contourArea(contour)
        if (areaMax > area) and (area > areaMin) :
            print("area=")
            print(area)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.15 * peri, True)
            corners = len(approx)
            print("corners=")
            print(corners)
            x,y,w,h = cv2.boundingRect(approx)
            if corners==4:
                i=i+1
                aspect_ratio = float(w)/h
                if aspect_ratio > 0.79 and aspect_ratio < 1.21:  
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
                    piece = (cX, cY, w, color)               
                    pieces.append(piece)
#                     if (area  >  maxAreaFound):
#                         maxAreaFound = area
#                         pieces =  findPieces(cX,cY,peri,frameHSV)          
                   # if w >= 30 and w <= 60 and area / (w * h) > 0.4:
                    if area / (w * h) > 0.4:
                        final_contours.append(square)
                        cv2.rectangle(frameHSV,(x,y),(x+w,y+h),(255,0,0),1)      
    print("Num final contours=")    
    print(len(final_contours))
    print("Max Area=")
    print(maxAreaFound)
#     if (len(final_contours) < 9) or (maxAreaFound <  areaMin):
    if (len(final_contours) < 9):
        return [],frameHSV
    print("More than 8 squares detected and big Square Detected!")
    print(pieces)
    print("****")
    pieces = sortPieces(pieces)
    print(pieces)
    
    return pieces,frameHSV

def detectFacefromImage(img):
    imgClean = cleanImage(img)
    detected = False
    cv2.imshow("image", imgClean)
    cv2.waitKey(0)
    face,img = findsCandidateEdges(imgClean,img)
    cv2.imshow("imageDetect", img)
    if (len(face)==9):
        detected = True
    return face,detected

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


def empty(a):
    pass

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",60,255,empty)
cv2.createTrackbar("Threshold2","Parameters",23,255,empty)
cv2.createTrackbar("AreaMax","Parameters",1000000,1200000,empty)

def closeCamera():
    cap.release()
    cv2.destroyAllWindows()

def captureRubikFace():
    ret,frame = cap.read()
    face = []
    if (ret == True):
        frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        face, detected = detectFacefromImage(frame)
        while (not detected):
            ret,frame = cap.read()
            frame = frame[0:400,0:480]
            face = []
            frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            face, detected = detectFacefromImage(frameHSV)
        imgResult = drawDetectedFace(frame,face)    
        cv2.imshow("result", imgResult)
        cv2.waitKey(0)
    return face    

