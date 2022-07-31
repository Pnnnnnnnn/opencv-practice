import cv2
import numpy as np
import time

pTime = 0
cTime = 0

param_and_max = [["hue",179],["sat",255],["val",255]]
param_val = {
            "hue_min" : 91,
            "hue_max" : 115,
            "sat_min" : 107,
            "sat_max" : 255,
            "val_min" : 97,
            "val_max" : 255
            }
all_point = [] # set of point to draw in the canvas

def do_nothing(val):
    pass

def init_trackbar():
    cv2.namedWindow("TrackBarsWindow")
    cv2.resizeWindow("TrackBarsWindow",640,300)
    for param,maxval in param_and_max:
        cv2.createTrackbar(param + "_min","TrackBarsWindow",param_val[param + "_min"],maxval,do_nothing)
        cv2.createTrackbar(param + "_max","TrackBarsWindow",param_val[param + "_max"],maxval,do_nothing)

def get_val():
    param_val = dict()
    for param,_ in param_and_max:
        param_val[param + "_min"] = cv2.getTrackbarPos(param + "_min","TrackBarsWindow")
        param_val[param + "_max"] = cv2.getTrackbarPos(param + "_max","TrackBarsWindow")
    return param_val

def get_mask(param_val,imgHSV):
    lower = np.array([param_val["hue_min"],param_val["sat_min"],param_val["val_min"]])
    upper = np.array([param_val["hue_max"],param_val["sat_max"],param_val["val_max"]])
    # mask คือ array ที่ ถ้าpixelไหนของรูปมีค่าอยู่ในช่วงhue,sat,valที่กำหนดช่องนั้นจะเป็น255(ถ้าไม่อยู่จะเป็น0)
    mask = cv2.inRange(imgHSV,lower,upper)
    return mask

def add_points(frame,img,canvas,show_contours=False):
    contours,_ = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        if show_contours:
            cntImg = frame.copy()
            cv2.drawContours(cntImg,cnt,-1,(255,0,0))
            cv2.imshow("cntImg",cntImg)
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*peri,True)
        area = cv2.contourArea(approx)
        if area > 300:
            x, y, w, h = cv2.boundingRect(approx)
            center_x = x + w//2
            center_y = y + h//2
            all_point.append((center_x,center_y))
    draw(canvas)

def draw(canvas):
    for point in all_point:
        cv2.circle(canvas,point,10,(0,255,255),cv2.FILLED)
    cv2.imshow("Canvas",canvas)
    # print(len(all_point))

init_trackbar()
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    frame = cv2.flip(frame,1)
    mask = get_mask(get_val(),cv2.cvtColor(frame,cv2.COLOR_BGR2HSV))

    add_points(frame,mask,frame,show_contours=False)

    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    print(f"fps = {fps}")

    if cv2.waitKey(1) == ord('c'):
        all_point = []
    elif cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()