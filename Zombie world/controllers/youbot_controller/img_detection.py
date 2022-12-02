import cv2
import pandas as pd
import numpy as np
import copy

BERRY_DISTANCE = 10 #unit in pixel
ZOMBIE_DISTANCE = 30



index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('./colors.csv', names=index, header=None)

# return the name of the color based on the RGB value
def getColorName(R,G,B):
    minimum = 1000
    color_name = " "
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
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of contours = {}".format(str(len(contours))))
    for i in contours:
        M = cv2.moments(i)
        area = 0
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            area = cv2.contourArea(i)
            if (area < (img_height * img_width) / 2 ):

                # cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
                # cv2.circle(img, (cx, cy), 7, (0, 0, 255), -1)
                # cv2.putText(img, "center", (cx - 20, cy - 20),
                #        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                object_data.append([[cy,cx], area])
    # cv2.imwrite("./test1.jpg", img)

    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return object_data

def helper_contour(view, object_data, type):
    add = True
    if (type == "green" or type == "blue" or type == "aqua" or type == "purple"):
        limit = 20
    else:
        limit = 5
    if (view[type] == []):
        view[type].append(object_data)
    else:
        for i in view[type]:
            if ((i[0][0] - object_data[0][0]) < limit and (i[0][1] - object_data[0][1]) < limit):
                i[0][0] = 0.5 * (i[0][0] + object_data[0][0])
                i[0][1] = 0.5 * (i[0][1] + object_data[0][1])
                if (i[1] != 0):
                    i[1] = i[1] + object_data[1]
                else:
                    i[1] += 1
                add = False
                break
        if add:
        #     if (type == "possible berries" and len(view["possible berries"]) > 6):
        #         print("here1")
        #         for i in range(len(view[type])):
        #             if (5 < (view[type][i][0][0] - object_data[num][0][0]) < 25 and 5 < (view[type][i][0][1] - object_data[num][0][1]) < 25):
        #                 print("here2")
        #                 removed_index.append(i)
        #     else:
            view[type].append([object_data[0],object_data[1]])
        # print(removed_index)
        # if removed_index != []:
        #     for i in removed_index:
        #         view["possible berries"].pop(i)
        #     view["possible zombies"].append([object_data[num][0],object_data[num][1]])
        # else:
        #     view[type].append([object_data[num][0],object_data[num][1]])
    return view
def helper_contour_add_dir(image, view, img_width, img_height):
    for key, value in view.items():
        copy_data = copy.deepcopy(value)
        new_data  = []
        if (key == "green" or key == "blue" or key == "aqua" or key == "purple"):
            for object in copy_data:
                if object[1] > 30:
                    new_data.append(object)
            view[key] = new_data
        if (key == "possible berries"):
            for data in copy_data:
                if data[1] > 20:
                    new_data.append(data)
            view[key] = new_data
        for object in view[key]:
            if object[0][0] < 0.25 * img_width:
                object.append("left")
            elif object[0][0] > 0.75 * img_width:
                object.append("right")
            else:
                object.append("center")
    return view

# find the class based on various color name
def find_color(given):
    # color group info
    # first value of the each element is the class name
    color_info = [["red", "rose", "wine", "dark sienna"], ["yellow"], ["orange"], ["pink"], ["green"], ["blue"], ["aqua"], ["purple"]]
    for color_group in color_info:
            for color in color_group:
                if (given.find(color) != -1):
                    return color_group[0]
    return " "

# def object_data_fliter(bject_data):
def zombie_berry_info(object_data, image, img_width, img_height):
    R = 0
    G = 0
    B = 0
    c = 0

    view = {"red": [], "yellow": [], "orange": [], "pink": [],
            "green": [], "blue": [], "aqua": [], "purple": [],
            "possible berries":[], "possible zombies":[],  "wall": []}

    # print(object_data)

    for i in range(len(object_data)):
        color_flag = False
        x,y = object_data[i][0]
        for cx in range(x - 4, x + 8):
            if color_flag: break
            for cy in range(y, y + 1):
                if (0 < cx < img_width and 0 < cy < img_height):
                    R  += image[cx][cy][0]
                    G  += image[cx][cy][1]
                    B  += image[cx][cy][2]
                    c += 1
                    color = getColorName(image[cx][cy][0],image[cx][cy][1],image[cx][cy][2])
                    color = color.lower()
                    color = find_color(color)
                    if (color != " "):
                        color_flag = True
                        # print(color)
                        break
        # print(x, y, color_flag)
        if color_flag == False:
            if c == 0: c = 1
            color = getColorName(R/c,G/c,B/c)
            color = color.lower()
            # print(color)
            color = find_color(color)

        if (color != " "):
            view = helper_contour(view, object_data[i], color)
        else:
            view = helper_contour(view, object_data[i], "possible berries")
    view = helper_contour_add_dir(image, view, img_width, img_height)
    return view
