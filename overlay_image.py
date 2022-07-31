import cv2
import numpy as np
import time

inserted = cv2.imread(r"Outputs\box.png")
# print(inserted.shape)
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
while True:
    _, frame = cap.read()
    # print(frame.shape)
    frame[0:360, 0:250] = inserted

    cv2.imshow("Overlay",frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()