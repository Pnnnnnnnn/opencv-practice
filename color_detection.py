import cv2
import numpy as np

param_and_max = [["hue",179],["sat",255],["val",255]]

def do_nothing(val):
    pass

def init_trackbar():
    cv2.namedWindow("TrackBarsWindow")
    cv2.resizeWindow("TrackBarsWindow",640,300)
    for param,maxval in param_and_max:
        cv2.createTrackbar(param + "_min","TrackBarsWindow",0,maxval,do_nothing)
        cv2.createTrackbar(param + "_max","TrackBarsWindow",maxval,maxval,do_nothing)

def get_val():
    param_val = dict()
    for param,_ in param_and_max:
        param_val[param + "_min"] = cv2.getTrackbarPos(param + "_min","TrackBarsWindow")
        param_val[param + "_max"] = cv2.getTrackbarPos(param + "_max","TrackBarsWindow")
    return param_val

def show_result(param_val,imgHSV):
    lower = np.array([param_val["hue_min"],param_val["sat_min"],param_val["val_min"]])
    upper = np.array([param_val["hue_max"],param_val["sat_max"],param_val["val_max"]])
    #mask คือ array ที่ ถ้าpixelไหนของรูปมีค่าอยู่ในช่วงhue,sat,valที่กำหนดช่องนั้นจะเป็น255(ถ้าไม่อยู่จะเป็น0)
    mask = cv2.inRange(imgHSV,lower,upper)
    cv2.imshow("mask",mask)

init_trackbar()
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()
    show_result(get_val(),cv2.cvtColor(frame,cv2.COLOR_BGR2HSV))
    cv2.imshow("camera",frame)
    if cv2.waitKey(10) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()