import cv2
import numpy as np

def getContours(img,outImg):
    contours,_ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>100:
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True) #ใช้ลดความละเอียดของ cnt
            # cv2.drawContours(outImg,cnt,-1,(255,0,0),3)
            x, y, w, h = cv2.boundingRect(cnt)
            if(len(approx) == 5):
                print(f"contour = {cnt} approx = {approx}")
            cv2.putText(outImg,str(len(approx)),(x+w//2,y+h//2),cv2.FONT_ITALIC,0.7,(0,0,0),2)
            cv2.rectangle(outImg,(x,y),(x+w,y+h),(0,0,255),3)
    return outImg

path = r'Resources\shape.jpg'
img = cv2.imread(path)
img = cv2.resize(img,(750,600))

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray,(7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)
imgContour = getContours(imgCanny,img.copy())

cv2.imshow("imgGray",imgGray)
cv2.imshow("imgBlur",imgBlur)
cv2.imshow("imgCanny",imgCanny)
cv2.imshow("imgContour",imgContour)

cv2.waitKey(0)
