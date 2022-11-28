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

def object_info(img, img_width, img_height):
    # img = np.array(img[])
    # img = cv2.imread('./test1.jpg')
    object_data = [] #center point, area
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    im, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of contours = {}".format(str(len(contours))))
    for i in contours:
        M = cv2.moments(i)
        area = 0
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            if (area < (img_height * img_width) / 2 ):

                # cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
                # cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                # cv2.putText(img, "center", (cx - 20, cy - 20),
                #        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                object_data.append([(cy,cx), area])
    # cv2.imwrite("./test1.jpg", img)

    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return object_data

def zombie_berry_info(object_data, image, img_width, img_height):
    R = 0
    G = 0
    B = 0
    c = 0
    view = []
    for i in range(len(object_data)):
        x,y = object_data[i][0]
        for cx in range(x - 5, x + 5):
            for cy in range(y - 5, y + 5):
                if (0 < cx < img_width and 0 < cy < img_height):
                    R  += image[cx][cy][0]
                    G  += image[cx][cy][1]
                    B  += image[cx][cy][2]
                    c += 1
        color = getColorName(R/c,G/c,B/c)
        color = color.lower()
        if (color.find("red") != -1 or color.find("rose") != -1 or color.find("wine") != -1):
            view.append(["red berry",object_data[i][0],color])
        elif (color.find("yellow") != -1):
            view.append(["yellow berry",object_data[i][0],color])
        elif (color.find("orange") != -1):
            view.append(["orange berry",object_data[i][0],color])
        elif (color.find("pink")!= -1):
            view.append(["pink berry",object_data[i][0],color])
        elif (color.find("green") != -1):
            view.append(["green zombie",object_data[i][0],color])
        elif (color.find("blue")!= -1):
            view.append(["blue zombie",object_data[i][0],color])
        elif (color.find("aqua") != -1):
            view.append(["aqua zombie",object_data[i][0],color])
        elif (color.find("purple") != -1):
            view.append(["purple zombie",object_data[i][0],color])
    return view

        


