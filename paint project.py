import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)

mycolors = [[6,46,216,22,255,255],
            [27,88,166,158,255,255]]
myColorValues = [[51,153,255],           ##BGR format
                 [0,255,255]]

myPoints=[]  ## x , y , colorID


def findcolor(img,mycolors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in mycolors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgResult,(x,y),5,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count+=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)[-2:]
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 150), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x ,y ,w ,h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findcolor(img, mycolors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break
