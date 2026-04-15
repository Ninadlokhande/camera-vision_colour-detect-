import numpy  as np
import cv2 


def limits_range(color):

    c= np.uint8([[color]])
    hsv_c = cv2.cvtColor(c , cv2.COLOR_BGR2HSV)
    lower = np.array([hsv_c[0][0][0] - 4 , 200 , 180])
    upper = np.array([hsv_c[0][0][0] + 4 , 255 , 255])

    lower = np.array(lower,dtype = np.uint8)
    upper = np.array(upper,dtype = np.uint8)
    return lower , upper