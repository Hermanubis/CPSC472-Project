import cv2
import pandas as pd
import numpy as np

BERRY_DISTANCE = 10 #unit in pixel
ZOMBIE_DISTANCE = 30



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
                object_data.append([[cy,cx], area])
    # cv2.imwrite("./test1.jpg", img)

    # cv2.imshow('Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return object_data

def helper_contour(view, object_data, num, type):
    add = True
    removed_index = []
    if (view[type] == []):
        view[type].append([object_data[num][0],object_data[num][1]])
    else:
        for i in view[type]:
            if ((i[0][0] - object_data[num][0][0]) < 5 and (i[0][1] - object_data[num][0][1]) < 5):
                i[0][0] = 0.5 * (i[0][0] + object_data[num][0][0])
                i[0][1] = 0.5 * (i[0][1] + object_data[num][0][1])
                i[1] = i[1] + object_data[num][1]
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
            view[type].append([object_data[num][0],object_data[num][1]])
        # print(removed_index)
        # if removed_index != []:
        #     for i in removed_index: 
        #         view["possible berries"].pop(i)
        #     view["possible zombies"].append([object_data[num][0],object_data[num][1]])
        # else:
        #     view[type].append([object_data[num][0],object_data[num][1]])
    return view

def helper_contour_add_dir(view, img_width):
    for key, value in view.items():
        for object in value:
            if object[0][0] < 0.25 * img_width:
                object.append("left")
            elif object[0][0] > 0.75 * img_width:
                object.append("right")
            else:
                object.append("center")
    return view

def zombie_berry_info(object_data, image, img_width, img_height):
    R = 0
    G = 0
    B = 0
    c = 0
    view = {"red berry": [], "yellow berry": [], "orange berry": [], "pink berry": [],
            "green zombie": [], "blue zombie": [], "aqua zombie": [], "purple zombie": [], 
            "possible berries":[], "possible zombies":[],  "wall": []}
    for i in range(len(object_data)):
        x,y = object_data[i][0]
        for cx in range(x - 10, x + 10):
            for cy in range(y - 10, y + 10):
                if (0 < cx < img_width and 0 < cy < img_height):
                    R  += image[cx][cy][0]
                    G  += image[cx][cy][1]
                    B  += image[cx][cy][2]
                    c += 1
        color = getColorName(R/c,G/c,B/c)
        color = color.lower()
        # print(R/c,G/c,B/c,color)
        if (color.find("red") != -1 or color.find("rose") != -1 or color.find("wine") != -1):
            view = helper_contour(view, object_data, i, "red berry")
        elif (color.find("yellow") != -1):
            view = helper_contour(view, object_data, i, "yellow berry")
        elif (color.find("orange") != -1):
            view = helper_contour(view, object_data, i, "orange berry")
        elif (color.find("pink")!= -1):
            view = helper_contour(view, object_data, i, "pink berry")
        elif (color.find("green") != -1):
            # if (object_data[i][1] > 5):
                view = helper_contour(view, object_data, i, "green zombie")
            # elif (object_data[i][1] < 10): 
            #     view = helper_contour(view, object_data, i, "possible berries")
        elif (color.find("blue")!= -1 or color.find("outer space") != -1 or color.find("stormcloud") != -1 or color.find("charcoal") != -1):
            # if (object_data[i][1] > 5):
                view = helper_contour(view, object_data, i, "blue zombie")
            # elif (object_data[i][1] < 10): 
                # view = helper_contour(view, object_data, i, "possible berries")
        elif (color.find("aqua") != -1):
            # if (object_data[i][1] > 5):
                view = helper_contour(view, object_data, i, "aqua zombie")
            # elif (object_data[i][1] < 10): 
                # view = helper_contour(view, object_data, i, "possible berries")
        elif (color.find("purple") != -1):
            # if (object_data[i][1] > 5):
                view = helper_contour(view, object_data, i, "purple zombie")
            # elif (object_data[i][1] < 10): 
                # view = helper_contour(view, object_data, i, "possible berries")
        else:
            if (object_data[i][1] < 10):
                view = helper_contour(view, object_data, i, "possible berries")
    view = helper_contour_add_dir(view, img_width)
    return view






# def image_data(image,image_width,image_height):
#     view = {"red": [0,0,0], "yellow": [0,0,0], "orange": [0,0,0], "pink": [0,0,0],
#             "green": [0,0,0], "blue": [0,0,0], "aqua": [0,0,0], "purple": [0,0,0], "wall": 0}
#     objects = {"berries":[], "zombies": [], "others": []}
#     # display the components of each pixel
#     for x in range(0,image_width):
#         for y in range(0,image_height):
#             R = image[x][y][0]
#             G = image[x][y][1]
#             B = image[x][y][2]
#             print(R, G, B)
#             color =  rgb_to_colorname(R, G, B)
#             if color != None:
#                 if x < image_width/3:
#                     view[color][0] += 1
#                 elif x > image_width/3 and x < 2 * image_width/3:
#                      view[color][1] += 1
#                 else:
#                     view[color][2] += 1
            # if x == image_width/3:
            #     for key, value in view.items(): 
            #         print(value) 
            #         if (key == "red" or key == "yellow" or key == "orange" or key == "pink"):
            #             if value[0] > BERRY_DISTANCE: 
            #                 objects["berries"].append([key,"left"])
            #         else:
            #             if value[0] > ZOMBIE_DISTANCE: 
            #                 objects["zombies"].append([key,"left"])
            
            # if x == 2 * image_width/3:
            #     for key, value in view.items(): 
            #         print(value) 
            #         if (key == "red" or key == "yellow" or key == "orange" or key == "pink"):
            #             if value[1] > BERRY_DISTANCE: 
            #                 objects["berries"].append([key,"middle"])
            #         else:
            #             if value[1] > ZOMBIE_DISTANCE: 
            #                 objects["zombies"].append([key,"middle"])
            
            # if x == image_width:
            #     for key, value in view.items(): 
            #         print(value) 
            #         if (key == "red" or key == "yellow" or key == "orange" or key == "pink"):
            #             if value[2] > BERRY_DISTANCE: 
            #                 objects["berries"].append([key,"right"])
            #         else:
            #             if value[2] > ZOMBIE_DISTANCE: 
            #                 objects["zombies"].append([key,"right"])

    # return view