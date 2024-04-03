import cv2
import numpy as np

def getContours(img, cThresh=[100,100], showCanny=False, minArea=1000, filter=0, draw=False):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),1)
    canny = cv2.Canny(blur,cThresh[0],cThresh[1])
    #canny=cv2.resize(canny,(0,0),None, 0.5,0.5)
    kernel = np.ones((5,5))
    #dilation and erosion to get good edges
    dilate=cv2.dilate(canny,kernel,iterations=3)
    thresh=cv2.erode(dilate,kernel,iterations=2)
    if showCanny: cv2.imshow('Canny', thresh)
    contours, heirarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #external for outer edges... next one for approximation
    finalContours = []
    for i in contours:
        area=cv2.contourArea(i)
        if area>minArea:
            peri=cv2.arcLength(i,True)
            approx=cv2.approxPolyDP(i,0.02*peri,True)
            bbox=cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx),area,approx,bbox,i])
            else:
                    finalContours.append([len(approx),area,approx,bbox,i])
    finalContours = sorted(finalContours,key=lambda x:x[1],reverse=True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img,con[4],-1,(0,0,225),3)
    return img, finalContours

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def reorder(myPoints):
    #print("ABC")
    print(myPoints.shape)
    myPointsNew = np.zeros_like(myPoints)
    myPoints=myPoints.reshape((4,2))
    add = myPoints.sum(1)
    myPointsNew[0]=myPoints[np.argmin(add)]
    myPointsNew[3]=myPoints[np.argmax(add)]
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1]=myPoints[np.argmin(diff)]
    myPointsNew[2]=myPoints[np.argmax(diff)]
    return myPointsNew


def warpImg (img,points,w,h, pad=20):
    print(points)
    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    imgWarp = imgWarp[pad:imgWarp.shape[0]-pad,pad:imgWarp.shape[1]-pad]
    #padding to remove edges, wont affect distance of objects later
    return imgWarp

def findDis(pts1,pts2):
    return ((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5