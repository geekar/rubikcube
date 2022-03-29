"""
@author: alber
"""
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from operator import itemgetter

from PIL import Image, ImageFilter

colors = {
    'b': ([79, 55, 56], [150, 255, 255]),    # Blue
    'g1': ([40, 80,94], [78, 255, 255]),    # Green
    'g2': ([6, 80, 100], [7, 255, 102]),    # Green
    'g3': ([125,7, 105], [127, 8, 109]),    # Green
    'g4': ([81,14, 55], [170, 32, 65]),    # Green
    'y': ([11, 50, 114], [39, 255, 255]),   # Yellow
    #'o1': ([0, 60, 20], [16, 180, 255]),     # Orange
    'o1': ([173, 100, 50], [180, 255, 255]),     # Orange
    'o2': ([173, 100, 50], [180, 255, 255]),     # Orange
    'r1': ([0, 150, 20], [10, 255, 255]),     # Red
    'r2': ([159, 150, 20], [172, 255, 255]),     # Red
    'r3': ([159, 150, 20], [172, 255, 255]),    # Red
   # 'r3': ([160, 150, 100], [180, 255, 255]),     # Red  
    'w': ([0, 0, 125], [255, 50, 255])        #White
    }

color_names = ['b','g','y','o','r','w']

DS_SQUARE_SIDE_RATIO = 1.5
DS_MORPH_KERNEL_SIZE = 5
DS_MORPH_ITERATIONS = 2
DS_MIN_SQUARE_LENGTH_RATIO = 0.08
DS_MIN_AREA_RATIO = 0.68
DS_MIN_SQUARE_SIZE = 0.2 #times the width of image
DS_MAX_SQUARE_SIZE = 0.3

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
    print("h={}, s={}, v={}, color={} ".format(h,s,v,color))
    return color

def colorNombreLargo(color_name):
    switcher = {
    'r': "ROJO",
    'b': "AZUL",
    'g': "VERDE",
    'y': "AMARILLO",
    'o': "NARANJA",
    'w': "BLANCO"
    }
    return switcher.get(color_name)

def mshow(im, titles = None):
    if str(type(im)) != str(type([])):
        plt.imshow(im)
        if titles:
            plt.title(
            label=titles,
            fontsize=30,
            color="black")
        plt.show()
    else:
        m = int(pow(len(im), 0.5))
        n = int(math.ceil(len(im)/float(m)))
        for i in range(len(im)):
            plt.subplot(m, n, i+1)
            plt.imshow(im[i])
            if titles:
                plt.title(titles[i])
        plt.show()
        

def index_to_cube(pts):
    print("pts=")
    print(pts)
    print(len(pts))
    

    if len(pts) != 9:
        return None
    
    pts = [list(pts[i])+[i] for i in range(len(pts))]
    pts.sort(key=itemgetter(1))
    mat = [[pts[3*i+j] for j in range(3)] for i in range(3)]
    print("mat=")
    print(mat)
    
    for i in range(3):
        mat[i].sort(key=itemgetter(0))

    for i in range(3):
        for j in range(3):
            mat[i][j] = mat[i][j][2]

    return mat

def get_black_mask(img, smoothed=False, isBGR=False):
    DEBUG_SHOW_MASK = False
    
    if isBGR:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
  
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#   
#     ret, thresh = cv2.threshold(gray, 15, 255, cv2.THRESH_BINARY_INV)
#     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#     
#     black_image = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
#     
#     mask = cv2.drawContours(black_image, contours, -1,(0,0,255),3)

    
     #tuple([0, 0, 0]), tuple([255, 10, 255])
    
    mask = cv2.inRange(img, tuple([0, 0, 0]), tuple([120, 255, 120]))
    
    if smoothed:
        kernel = np.ones(tuple([DS_MORPH_KERNEL_SIZE]*2))
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1) 

    if DEBUG_SHOW_MASK:
        mshow([mask], ['black mask in function'])

    return mask

def get_color_mask(im, color_name, smoothed=True, isBGR=False):
    DEBUG_SHOW_MASK = False

    if isBGR:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    
    
    print(color_name)
 
    
    if color_name == "g":
        mask = cv2.inRange(im, tuple(colors["g1"][0]), tuple(colors["g1"][1]))|cv2.inRange(im, tuple(colors["g2"][0]), tuple(colors["g2"][1]))|cv2.inRange(im, tuple(colors["g3"][0]), tuple(colors["g3"][1]))| cv2.inRange(im, tuple(colors["g4"][0]), tuple(colors["g4"][1]))
    elif color_name == "r":
        mask = cv2.inRange(im, tuple(colors["r1"][0]), tuple(colors["r1"][1]))|cv2.inRange(im, tuple(colors["r2"][0]), tuple(colors["r2"][1]))|cv2.inRange(im, tuple(colors["r3"][0]), tuple(colors["r3"][1]))
    elif color_name == "o":
        mask = cv2.inRange(im, tuple(colors["o1"][0]), tuple(colors["o1"][1]))|cv2.inRange(im, tuple(colors["o2"][0]), tuple(colors["o2"][1]))
    else:
        color = colors[color_name]
        mask = cv2.inRange(im, tuple(color[0]), tuple(color[1]))
        
    if smoothed:
        kernel = np.ones(tuple([DS_MORPH_KERNEL_SIZE]*2))
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1) 

    if DEBUG_SHOW_MASK:
        mshow([mask], [color_name + ' mask in function'])

    return mask

def colorNombreLargo(color_name):
    switcher = {
    'r': "ROJO",
    'b': "AZUL",
    'g': "VERDE",
    'y': "AMARILLO",
    'o': "NARANJA",
    'w': "BLANCO"
    }
    return switcher.get(color_name)


#accepts BGR image
def detect_square(im, color_name, maskBorders, isBGR=True):

    DEBUG_SHOW_MASK = True
    DEBUG_SHOW_INSIDE_FUNC = True

    def remove_bad_contours(conts):
        new_conts = []
        
        for cont in conts:
            bound_rect = cv2.minAreaRect(cont)
            length, breadth = float(bound_rect[1][0]), float(bound_rect[1][1])
            try:
##                print length/breadth, cv2.contourArea(cont)/(length*breadth)
                if max((length/breadth, breadth/length)) > DS_SQUARE_SIDE_RATIO:
                    continue
                if cv2.contourArea(cont)/(length*breadth) < DS_MIN_AREA_RATIO:
                    continue
                if not DS_MAX_SQUARE_SIZE*im.shape[0] > max((length, breadth)) > DS_MIN_SQUARE_SIZE*im.shape[0]:
                    continue
##                print length/breadth, cv2.contourArea(cont)/(length*breadth)
                new_conts.append(cont)
            except ZeroDivisionError:
                continue

        return new_conts

    if isBGR:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    global debug_mask

    mask = get_color_mask(im, color_name,True)
    
    #mask = get_black_mask(im, True)
    
    
    maskBorders = cv2.bitwise_not(maskBorders)
    mask = cv2.bitwise_and(mask, mask, mask=maskBorders)
    

    debug_mask=[np.array(mask)]

    if DEBUG_SHOW_MASK:
        mshow(debug_mask, ['COLOR ' + colorNombreLargo(color_name)]*len(debug_mask))
    
    conts,hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    
    conts = remove_bad_contours(conts)

    if DEBUG_SHOW_INSIDE_FUNC:
        im2 = np.array(im)
        for cont in conts:
            pos = tuple(np.array(cv2.minAreaRect(cont)[0],dtype=int))
            #print(pos)
            getColorName(im2,pos[0],pos[1])
            cv2.circle(im2, tuple(np.array(cv2.minAreaRect(cont)[0],dtype=int)),
                       int(pow(cv2.contourArea(cont)/3.14159, 0.5)), (255,255,255),thickness=2)
        #mshow(cv2.cvtColor(im2, cv2.COLOR_HSV2RGB))
        mshow(cv2.cvtColor(im2, cv2.COLOR_HSV2RGB), 'COLOR ' + colorNombreLargo(color_name))
        
       
       

    return [cv2.minAreaRect(cont) for cont in conts]

#accepts BGR
def get_cube_state(im, imborders):

    colors_detected = []
    cube_state = [[None]*3 for _ in range(3)]
    
    for color_name in color_names:
        rects = detect_square(im, color_name, imborders )
        for rect in rects:
            colors_detected.append((color_name, rect))
        
    #from pprint import pprint
    print(colors_detected)

    index_mat = index_to_cube([prop[1][0] for prop in colors_detected])
    

    
    if index_mat != None:
        for i in range(3):
            for j in range(3):
                cube_state[i][j] = colors_detected[index_mat[i][j]][0]

        return cube_state,len(colors_detected)
    else:
        return None
    
def detectEdges(img):
    #define the vertical filter
    vertical_filter = [[-1,-2,-1], [0,0,0], [1,2,1]]

    #define the horizontal filter
    horizontal_filter = [[-1,0,1], [-2,0,2], [-1,0,1]]


    #get the dimensions of the image
    n,m,d = img.shape

    #initialize the edges image
    edges_img = img.copy()

    #loop over all pixels in the image
    for row in range(3, n-2):
        for col in range(3, m-2):
            
            #create little local 3x3 box
            local_pixels = img[row-1:row+2, col-1:col+2, 0]
            
            #apply the vertical filter
            vertical_transformed_pixels = vertical_filter*local_pixels
            #remap the vertical score
            vertical_score = vertical_transformed_pixels.sum()/4
            
            #apply the horizontal filter
            horizontal_transformed_pixels = horizontal_filter*local_pixels
            #remap the horizontal score
            horizontal_score = horizontal_transformed_pixels.sum()/4
            
            #combine the horizontal and vertical scores into a total edge score
            edge_score = (vertical_score**2 + horizontal_score**2)**.5
            
            #insert this edge score into the edges image
            edges_img[row, col] = [edge_score]*3

    #remap the values in the 0-1 range in case they went out of bounds
    edges_img = edges_img/edges_img.max()
    return edges_img

def whiteBalanceImage(img):
    b,g,r = cv2.split(img)
    r_avg = cv2.mean(r)[0]
    g_avg = cv2.mean(g)[0]
    b_avg = cv2.mean(b)[0]
    
    # Find the gain of each channel
    k = (r_avg + g_avg + b_avg) / 3
    kr = k / r_avg
    kg = k / g_avg
    kb = k / b_avg

    r = cv2.addWeighted(src1=r, alpha=kr, src2=0, beta=0, gamma=0)
    g = cv2.addWeighted(src1=g, alpha=kg, src2=0, beta=0, gamma=0)
    b = cv2.addWeighted(src1=b, alpha=kb, src2=0, beta=0, gamma=0)

    balance_img = cv2.merge([b, g, r])
    #balance_img = cv2.cvtColor(balance_img, cv2.COLOR_BGR2RGB)
    return balance_img


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
    #image = img.filter(ImageFilter.FIND_EDGES)
    return canny

def crossFrame(img):
    cross = erodeFrame(img, cv2.MORPH_CROSS)
    cross = lineexpandFrame(cross, cv2.MORPH_CROS)
    return cross

def linesFrame(img):    
    lines = lineexpandFrame(img, cv2.MORPH_RECT)
#     lines = erodeFrame(lines, cv2.MORPH_RECT)
    return lines
    
def erodeFrame(img, kernel):
    #kernel = np.ones((3,3), np.uint8)
    kernel = cv2.getStructuringElement(kernel,(4,4))
    dilated = cv2.erode(img, kernel, iterations=3)
    return dilated

def lineexpandFrame(img, kernel):
    #kernel = np.ones((3,3), np.uint8)
    kernel = cv2.getStructuringElement(kernel,(3,3))
    dilated = cv2.dilate(img, kernel, iterations=3)
    return dilated

def cleanImage(img):
    #gray = ashFrame(img)
    #gray = detectEdges(img)
    gray = ashFrame(img)
    canny = blurredFrame(gray)
    canny = cannyFrame(canny)    
#     canny = crossFrame(canny)
    canny = linesFrame(canny)
    return canny

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
                        h,s,v=frameHSV[cY,cX]
                        #cl = (int(h),int(s),int(v))                                               
                        #cv2.rectangle(frameHSV,(x,y),(x+w,y+h),cl,1)
                        
                        #str = "h={}, s={}, v={}, color={} ".format(h,s,v,color)
                        #cv2.putText(frameHSV,str,(cX,cY),cv2.FONT_HERSHEY_SIMPLEX,1,cl,2)
                        
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

def detectFacefromImage(imgBGR):
    imgClean = cleanImage(imgBGR)
    detected = False
    cv2.imshow("image", imgClean)
    nfaces = 0
#     cv2.waitKey(0)    
    face,img = findsCandidateEdges(imgClean,imgBGR)
    face,nfaces = get_cube_state(imgBGR,imgClean)
    #cv2.imshow("imageDetect", imgBGR)
    cv2.imshow("imageColor", img)
    cv2.waitKey(0)
    print("nfaces=")
    print(nfaces)
    if (nfaces==9):
        detected = True
    return face,detected

def buildStringFaceOld(pieces):
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

def buildStringFace(face):
    str = ''
    colors = []
    for i in range(3):
        for j in range(3):            
            colors.append(face[i][j]) 
    template = ("{}{}{}{}{}{}{}{}{}")
    str=  template.format(*colors).strip()
    return str
    
def drawDetectedFace(img, face):
    print("face")
    for piece in face:
        (x, y, radius,   color) = piece
        h,s,v=img[y,x]
        str = "h={}, s={}, v={}, color={} ".format(h,s,v,color)
#         cv2.putText(img,color,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),2)
        cv2.putText(img,str,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(50,50,255),1)
         
    return img


def empty(a):
    pass

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters",16,255,empty)
cv2.createTrackbar("Threshold2","Parameters",10,255,empty)
cv2.createTrackbar("AreaMax","Parameters",1000000,1200000,empty)

def closeCamera():
    cap.release()
    cv2.destroyAllWindows()

def captureRubikFace():
    ret,frame = cap.read()
    face = []
    detected = False
    if (ret == True):
        while (not detected):
            ret,frame = cap.read()
            frame = whiteBalanceImage(frame)
            #frame = frame[0:400,0:480]
            face = []
            face, detected = detectFacefromImage(frame.copy())
            
        #imgResult = drawDetectedFace(frame,face)    
        #cv2.imshow("result", imgResult)
        #cv2.waitKey(0)
    return face    

