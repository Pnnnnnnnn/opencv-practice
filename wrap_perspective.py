import cv2
from cv2 import waitKey
from cv2 import getPerspectiveTransform
from cv2 import warpPerspective
import numpy as np
import os

img = cv2.imread(os.path.join("Resources","box.png"))

width,height = 250,360
pts1 = np.float32([[163,166],[578,123],[170,896],[562,821]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOut = cv2.warpPerspective(img,matrix,(width,height))

cv2.imshow("test",imgOut)
cv2.imwrite("box.png",imgOut)
cv2.waitKey(0)