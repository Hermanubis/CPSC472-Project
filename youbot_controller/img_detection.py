import cv2
import pandas as pd
import numpy as np


index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('./colors.csv', names=index, header=None)

# return the name of the color based on the RGB value
def getColorName(R,G,B):
    minimum = 1000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<minimum):
            minimum = d
            color_name = csv.loc[i,"color_name"]
    return color_name

def object_info(img, size_image):
    # arr_3D = np.array([[[0, 1, 1], [1, 0, 1], [1, 1, 0]]]) # create numpy 3D array which contain integer values

    # img = np.array(img[])
    # img = cv2.imread('./test1.jpg')
    object_data = [] #center point, area
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of contours = {}".format(str(len(contours))))
    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
            cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
            cv2.putText(img, "center", (cx - 20, cy - 20),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
            area = cv2.contourArea(i)
        if (area < size_image):
            object_data.append([(cx,cy), area])
    return object_data

