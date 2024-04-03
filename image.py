import cv2
import numpy as np
import cont 

webcam = False
path = "5.jpg"
cap = cv2.VideoCapture(0)  #camera object
cap.set(10,160)  #brightness 
cap.set(3,1920)  #width
cap.set(4,1080)  #height
scale = 3
wP = 210 * scale
hP = 297 * scale

while True:
   # if webcam:
        #success,img = cap.read()
    img = cv2.imread(path)
    img = cv2.resize(img,(0,0),None, 0.5,0.5)
    imgCons, conts = cont.getContours(img, minArea=50000, filter=4 )
    if len(conts) != 0:
        biggest = conts[0][2]
        #print(biggest)
        imgWarp = cont.warpImg (img,biggest,wP,hP) 
        #cv2.imshow('A4', imgWarp)
        #imgWarp = cv2.resize(imgWarp, (img.shape[1], img.shape[0]))
        imgCont2, conts2 = cont.getContours(imgWarp, minArea=2000, filter=4, cThresh=[50,50],draw=False)
        if len(conts2) != 0:
            for obj in conts2:
                cv2.polylines(imgCont2,[obj[2]],True,(0,255,0),2)
                print("oogaa")
                print(obj[2])
                nPoints = cont.reorder(obj[2])
                nW = round((cont.findDis(nPoints[0][0]//scale,nPoints[1][0]//scale)/10),1)
                nH = round((cont.findDis(nPoints[0][0]//scale,nPoints[2][0]//scale)/10),1)
                print(nW,nH)
                cv2.arrowedLine(imgCont2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(imgCont2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = obj[3]
                cv2.putText(imgCont2, '{}cm'.format(nW), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
                cv2.putText(imgCont2, '{}cm'.format(nH), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1.5,
                            (255, 0, 255), 2)
        imgCont2=cv2.resize(imgCont2,(0,0),None,0.5,0.5)
        cv2.imshow('A4', imgCont2)
        
    
    cv2.imshow('Original',img)
    key=cv2.waitKey(1) & 0xFF
    if key == 27:  # Break out of the loop if esc is pressed
        break
cv2.destroyAllWindows()
    
