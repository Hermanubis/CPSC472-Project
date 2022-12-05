"""youbot_controller controller."""

from controller import Robot, Motor, Camera, Accelerometer, GPS, Gyro, LightSensor, Receiver, RangeFinder, Lidar
from controller import Supervisor




from youbot_zombie import *
# from img_detection import *
#...
MAX_SPEED = 14
Speed = 4.0

#------------------CHANGE CODE BELOW HERE ONLY--------------------------
#define functions here for making decisions and using sensor inputs

import cv2
import pandas as pd
import numpy as np
import copy

#---------------------------Gripper---------------------------------------
LEFT = 0
RIGHT = 1

MIN_POS = 0.0
MAX_POS = 0.025
OFFSET_WHEN_LOCKED = 0.021
fingers = {}

def bound(v, a, b):
    if v > b:
        return b
    else:
        if v < a:
            return a
        else:
            return v

def gripper_init(robot):
    fingers[LEFT] = robot.getDevice("finger1")
    fingers[RIGHT] = robot.getDevice("finger2")

    fingers[LEFT].setVelocity(0.03)
    fingers[RIGHT].setVelocity(0.03)

def gripper_grip():
    fingers[LEFT].setPosition(MIN_POS)
    fingers[RIGHT].setPosition(MIN_POS)

def gripper_release():
    fingers[LEFT].setPosition(MAX_POS)
    fingers[RIGHT].setPosition(MAX_POS)


def gripper_set_gap(gap):
  v = bound(0.5 * (gap - OFFSET_WHEN_LOCKED), MIN_POS, MAX_POS)
  fingers[LEFT].setPosition(v)
  fingers[RIGHT].setPositionn(v)

# -------------------------------------ARM---------------------------
arm_elements = {}
from enum import Enum

class Height(Enum):
  ARM_FRONT_FLOOR = 0
  ARM_FRONT_PLATE = 1
  ARM_HANOI_PREPARE = 2
  ARM_FRONT_CARDBOARD_BOX = 3
  ARM_RESET = 4
  ARM_BACK_PLATE_HIGH = 5
  ARM_BACK_PLATE_LOW = 6
  ARM_MAX_HEIGHT = 7

class Orientation(Enum):
  ARM_BACK_LEFT = 0
  ARM_LEFT = 1
  ARM_FRONT_LEFT = 2
  ARM_FRONT = 3
  ARM_FRONT_RIGHT = 4
  ARM_RIGHT = 5
  ARM_BACK_RIGHT = 6
  ARM_MAX_SIDE = 7

class Arm(Enum):
  ARM1 = 0
  ARM2 = 1
  ARM3 = 2
  ARM4 = 3
  ARM5 = 4


current_height = Height.ARM_RESET.value
current_orientation = Orientation.ARM_FRONT.value

def arm_set_height(height):
    if height == Height.ARM_FRONT_FLOOR.value:
        arm_elements[Arm.ARM2.value].setPosition(-0.97)
        arm_elements[Arm.ARM3.value].setPosition(-1.55)
        arm_elements[Arm.ARM4.value].setPosition(-0.61)
        arm_elements[Arm.ARM5.value].setPosition(0.0)

    elif height == Height.ARM_FRONT_PLATE.value:
        arm_elements[Arm.ARM2.value].setPosition(-0.62)
        arm_elements[Arm.ARM3.value].setPosition(-0.98)
        arm_elements[Arm.ARM4.value].setPosition(-1.53)
        arm_elements[Arm.ARM5.value].setPosition(0.0)

    elif height == Height.ARM_FRONT_CARDBOARD_BOX.value:
        arm_elements[Arm.ARM2.value].setPosition(0.0)
        arm_elements[Arm.ARM3.value].setPosition(-0.77)
        arm_elements[Arm.ARM4.value].setPosition(-1.21)
        arm_elements[Arm.ARM5.value].setPosition(0.0)

    elif height == Height.ARM_RESET.value:
        arm_elements[Arm.ARM2.value].setPosition(1.57)
        arm_elements[Arm.ARM3.value].setPosition(-2.635)
        arm_elements[Arm.ARM4.value].setPosition(1.78)
        arm_elements[Arm.ARM5.value].setPosition(0.0)


    elif height == Height.ARM_BACK_PLATE_HIGH.value:
        arm_elements[Arm.ARM2.value].setPosition(0.678)
        arm_elements[Arm.ARM3.value].setPosition(0.682)
        arm_elements[Arm.ARM4.value].setPosition(1.74)
        arm_elements[Arm.ARM5.value].setPosition(0.0)


    elif height == Height.ARM_BACK_PLATE_LOW.value:
        arm_elements[Arm.ARM2.value].setPosition(0.92)
        arm_elements[Arm.ARM3.value].setPosition(0.42)
        arm_elements[Arm.ARM4.value].setPosition(1.78)
        arm_elements[Arm.ARM5.value].setPosition(0.0)


    elif height == Height.ARM_HANOI_PREPARE.value:
        arm_elements[Arm.ARM2.value].setPosition(-0.4)
        arm_elements[Arm.ARM3.value].setPosition(-1.2)
        arm_elements[Arm.ARM4.value].setPosition(-1.57)
        arm_elements[Arm.ARM5.value].setPosition(1.57)


    else:
      print("arm_height() called with a wrong argument")

    current_height = height
    return current_height

def arm_set_orientation(orientation):

    if orientation == Orientation.ARM_BACK_LEFT.value:
        arm_elements[Arm.ARM1.value].setPosition(-2.949)

    elif orientation == Orientation.ARM_LEFT.value:
        arm_elements[Arm.ARM1.value].setPosition(-1.57)
    elif orientation == Orientation.ARM_FRONT_LEFT.value:
        arm_elements[Arm.ARM1.value].setPosition(-0.2)
    elif orientation == Orientation.ARM_FRONT.value:
        arm_elements[Arm.ARM1.value].setPosition(0.0)
    elif orientation == Orientation.ARM_FRONT_RIGHT.value:
        arm_elements[Arm.ARM1.value].setPosition(0.2)
    elif orientation == Orientation.ARM_RIGHT.value:
        arm_elements[Arm.ARM1.value].setPosition(1.57)
    elif orientation == Orientation.ARM_BACK_RIGHT.value:
        arm_elements[Arm.ARM1.value].setPosition(2.949)
    else:
      print("arm_set_side() called with a wrong argument")

    current_orientation = orientation
    return current_orientation




def arm_init(robot):
  print(Arm.ARM1.value)
  arm_elements[Arm.ARM1.value] = robot.getDevice("arm1")
  arm_elements[Arm.ARM2.value] = robot.getDevice("arm2")
  arm_elements[Arm.ARM3.value] = robot.getDevice("arm3")
  arm_elements[Arm.ARM4.value] = robot.getDevice("arm4")
  arm_elements[Arm.ARM5.value] = robot.getDevice("arm5")

#   arm_elements[Arm.ARM2.value].setVelocity(0.5)

#   arm_set_height(Height.ARM_RESET.value)
#   arm_set_orientation(Orientation.ARM_FRONT.value)
  arm_reset()

def arm_reset():
  # initial the arm in the best pos
  arm_elements[Arm.ARM1.value].setPosition(0.0)
  arm_elements[Arm.ARM2.value].setPosition(1.3)
  arm_elements[Arm.ARM3.value].setPosition(-0.5)
  arm_elements[Arm.ARM4.value].setPosition(-1.7)
  arm_elements[Arm.ARM5.value].setPosition(0.0)


def arm_increase_height(current_height):
  current_height += 1
  if current_height >= Height.ARM_MAX_HEIGHT.value:
    current_height = Height.ARM_MAX_HEIGHT.value - 1
  arm_set_height(current_height)

def arm_decrease_height(current_height):
  current_height -= 1
  if int(current_height) < 0:
    current_height = 0
  arm_set_height(current_height)

def arm_increase_orientation(current_orientation):
  current_orientation += 1
  if (current_orientation >= Height.ARM_MAX_SIDE.value):
    current_orientation = Height.ARM_MAX_SIDE.value - 1
  arm_set_orientation(current_orientation)

def arm_decrease_orientation(current_orientation):
  current_orientation -= 1
  if (int(current_orientation) < 0):
    current_orientation = 0
  arm_set_orientation(current_orientation)

#----------------------grip the berries--------------------------------

def grip_berries():
    arm_elements[Arm.ARM2.value].setPosition(-0.3)
    gripper_grip()
    print("here",arm_elements[Arm.ARM1.value].getPositionSensor().getValue())
    grap_time = 3
    while grap_time:
        arm_elements[Arm.ARM1.value].setPosition(-1)
        grap_time -= 1
    grap_time = 3
    while grap_time:
        arm_elements[Arm.ARM1.value].setPosition(1)
        grap_time -= 1
    
    gripper_release()
    arm_reset()


#-------------------------------------------------------------------

def robot_reset(fr, fl, br, bl):
    fr.setVelocity(0)
    fl.setVelocity(0)
    br.setVelocity(0)
    bl.setVelocity(0)

def turn_left(fr, fl, br, bl,  speed =  8):
    print("turning left")
    fr.setVelocity(speed)
    fl.setVelocity(-speed)
    br.setVelocity(speed)
    bl.setVelocity(-speed)

    # fr.setPosition(speed)
    # fl.setPosition(-speed)
    # br.setPosition(speed)
    # bl.setPosition(-speed)


def turn_right(fr, fl, br, bl, speed =  8):
    print("turning right")
    fr.setVelocity(-speed)
    fl.setVelocity(speed)
    br.setVelocity(-speed)
    bl.setVelocity(speed)


def go_straight(fr, fl, br, bl, speed =  8):
    print("go straight")
    fr.setVelocity(speed)
    fl.setVelocity(speed)
    br.setVelocity(speed)
    bl.setVelocity(speed)

def go_back(fr, fl, br, bl, speed =  5.0):
    print("go back")
    if speed > 14:
        speed = MAX_SPEED
    fr.setVelocity(-speed)
    fl.setVelocity(-speed)
    br.setVelocity(-speed)
    bl.setVelocity(-speed)


BERRY_DISTANCE = 10 #unit in pixel
ZOMBIE_DISTANCE = 30

# -------------------image detection------------------------------------
# return the name of the color based on the RGB value
def getColorName(r,g,b):
    minimum = 1000
    color_name = " "
    if  ((15 < r and r < 25) and (115 < g and g < 145) and (15 < b and b < 25)) or \
        ((15 < r and r < 25) and (85 < g and g < 100) and (15 < b and b < 25)) or \
        ((28 < r and r < 45) and (190 < g and g < 210) and (30 < b and b < 45)) or \
        ((7 < r and r < 15) and (45 < g and g < 58) and (8 < b and b < 19)):
        color_name = "green"
    if  ((5 < r and r < 15) and (30 < g and g < 50) and (86 < b and b < 108)) or \
        ((18 < r and r < 40) and (114 < g and g < 150) and (205 < b and b < 244)):
        color_name = "blue"
    if  ((7 < r and r < 16) and (59 < g and g < 74) and (59 < b and b < 74)) or \
        ((30 < r and r < 49) and (170 < g and g < 180) and (140 < b and b < 155)) or \
        ((30 < r and r < 49) and (180 < g and g < 195) and (158 < b and b < 173)) or \
        ((30 < r and r < 49) and (200 < g and g < 240) and (190 < b and b < 220)):
        color_name = "aqua"
    if  ((145 < r and r < 26) and (115 < g and g < 145) and (15 < b and b < 25)) or \
        ((43 < r and r < 65) and (15 < g and g < 30) and (90 < b and b < 130)) or \
        ((110 < r and r < 130) and (40 < g and g < 57) and (180 < b and b < 200)):
        color_name = "purple"
    if  ((60 < r and r < 78) and (13 < g and g < 28) and (13 < b and b < 28)) or \
        ((190 < r and r < 225) and (53 < g and g < 66) and (37 < b and b < 49)):
        color_name = "red"
    if  ((188 < r and r < 200) and (117 < g and g < 129) and (162 < b and b < 175)) or \
        ((56 < r and r < 68) and (33 < g and g < 44) and (62 < b and b < 73)):
        color_name = "pink"
    if  ((202 < r and r < 220) and (190 < g and g < 205) and (25 < b and b < 36)) or \
        ((65 < r and r < 75) and (63 < g and g < 74) and (8 < b and b < 18)):
        color_name = "yellow"
    if  ((188 < r and r < 200) and (117 < g and g < 129) and (77 < b and b < 89)) or \
        ((55 < r and r < 68) and (33 < g and g < 43) and (28 < b and b < 37)) :
        color_name = "orange"
    if  ((r > 50 and g-5 < r and r < g+5) and (g > b-15)) or \
        ((60 < r and r < 70) and (60 < g and g < 70) and (60 < b and b < 70)) or \
        ((65 < r and r < 75) and (70 < g and g < 80) and (90 < b and b < 100)) or \
        ((203 < r and r < 220) and (203 < g and g < 220) and (203 < b and b < 220)):
        color_name = "wall"
    if  ((5 < r and r < 15) and (5 < g and g < 15) and (8 < b and b < 19)) or \
        ((20 < r and r < 35) and (20 < g and g < 35) and (20 < b and b < 35)):
        color_name = "dark"
    # for i in range(len(csv)):
    #     d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
    #     if(d<minimum):
    #         minimum = d
    #         color_name = csv.loc[i,"color_name"]
    return color_name

def object_info(img, img_width, img_height):
    object_data = [] #center point, area
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 50, 255, 0)
    img, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print("Number of contours = {}".format(str(len(contours))))
    for i in contours:
        M = cv2.moments(i)
        area = 0
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            area = cv2.contourArea(i)
            if (area < (img_height * img_width) / 2 ):
                object_data.append([[cy,cx], area])
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
            view[type].append([object_data[0],object_data[1]])
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
        if key != "wall":
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
    color_info = [["red"], ["yellow"], ["orange"], ["pink"], ["green"], ["blue"], ["aqua"], ["purple"]]
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
            "possible berries":[], "possible zombies":[],  "wall": False}

    # print(object_data)
    # print("---------")
    # view = wall_test(view, object_data, image, img_width, img_height)
    # if (view["wall"] ==  True ):
    #     return view
    for i in range(len(object_data)):
        color_flag = False
        x,y = object_data[i][0]
        # print(image[x][y][0],image[x][y][1],image[x][y][2])
        # color = getColorName(image[x][y][0],image[x][y][1],image[x][y][2])
        # print(color)

        for cx in range(x - 2 , x + 1):
            if color_flag: break
            for cy in range(y - 2, y + 1):
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

def wall_test(image, img_width, img_height):
    # if (object_data == []):
    g_x = int(img_width /2)
    g_y = int(img_height * 5.8/10)
    R_g  = image[g_x][g_y][0]
    G_g  = image[g_x][g_y][1]
    B_g  = image[g_x][g_y][2]
    color_wall = getColorName(R_g,G_g,B_g)
    color_wall = color_wall.lower()
    print("wall color", color_wall)
    if (color_wall == "wall"):
        return True
    return False

# ---------------------------------------------------------------
# ---------------------------GPS(stuck)---------------------------
def is_stuck(new_gps, old_gps, stuck_time):
    diffx = abs(new_gps[0] - old_gps[0])
    diffy = abs(new_gps[1] - old_gps[1])
    is_stuck = False
    print("diff",diffx,diffy)
    if (diffx < 0.001 and diffy < 0.001):
      if (stuck_time <= 1):
        stuck_time += 2
      else:
        is_stuck = True
    else:
        stuck_time = 0
    return [stuck_time, is_stuck]




#------------------CHANGE CODE ABOVE HERE ONLY--------------------------

def main():
    robot = Supervisor()

    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep()*2)

    #health, energy, armour in that order
    robot_info = [100,100,0]
    passive_wait(0.1, robot, timestep)
    pc = 0
    timer = 0

    robot_node = robot.getFromDef("Youbot")
    trans_field = robot_node.getField("translation")

    get_all_berry_pos(robot)

    robot_not_dead = 1

    #------------------CHANGE CODE BELOW HERE ONLY--------------------------

    #COMMENT OUT ALL SENSORS THAT ARE NOT USED. READ SPEC SHEET FOR MORE DETAILS
    accelerometer = robot.getDevice("accelerometer")
    accelerometer.enable(timestep)

    gps = robot.getDevice("gps")
    gps.enable(timestep)

    compass = robot.getDevice("compass")
    compass.enable(timestep)

    camera1 = robot.getDevice("ForwardLowResBigFov")
    camera1.enable(timestep)

    camera2 = robot.getDevice("ForwardHighResSmallFov")
    camera2.enable(timestep)

    camera3 = robot.getDevice("ForwardHighRes")
    camera3.enable(timestep)

    camera4 = robot.getDevice("ForwardHighResSmall")
    camera4.enable(timestep)

    camera5 = robot.getDevice("BackLowRes")
    camera5.enable(timestep)

    camera6 = robot.getDevice("RightLowRes")
    camera6.enable(timestep)

    camera7 = robot.getDevice("LeftLowRes")
    camera7.enable(timestep)

    camera8 = robot.getDevice("BackHighRes")
    camera8.enable(timestep)

    gyro = robot.getDevice("gyro")
    gyro.enable(timestep)

    lightSensor = robot.getDevice("light sensor")
    lightSensor.enable(timestep)

    receiver = robot.getDevice("receiver")
    receiver.enable(timestep)

    rangeFinder = robot.getDevice("range-finder")
    rangeFinder.enable(timestep)

    lidar = robot.getDevice("lidar")
    lidar.enable(timestep)

    fr = robot.getDevice("wheel1")
    fl = robot.getDevice("wheel2")
    br = robot.getDevice("wheel3")
    bl = robot.getDevice("wheel4")

    fr.setPosition(float('inf'))
    fl.setPosition(float('inf'))
    br.setPosition(float('inf'))
    bl.setPosition(float('inf'))
    
    #------------------------------GRIPPER---------------------------------
    gripper_init(robot)
    arm_init(robot)
    i=0
    zombie_list = ['green','blue','aqua','purple']
    berry_list = ['red','yellow','orange','pink']
    bestHealthBerry = ''
    bestHealthBerry=0
    bestEnergyBerry = ''
    bestBerryEnergy = 0
    lastHealth = [100]
    lastEnergy = [100]
    lastBerry = ''
    worstBerry=''
    #------------------CHANGE CODE ABOVE HERE ONLY--------------------------

    while(robot_not_dead == 1):
        
        if(robot_info[0] < 0):
            robot_not_dead = 0
            print("ROBOT IS OUT OF HEALTH")
            #if(zombieTest):
            #    print("TEST PASSED")
            #else:
            #    print("TEST FAILED")
            #robot.simulationQuit(20)
            #exit()

        if(timer%2==0):
            trans = trans_field.getSFVec3f()
            robot_info = check_berry_collision(robot_info, trans[0], trans[2], robot)
            robot_info = check_zombie_collision(robot_info, trans[0], trans[2], robot)

        if(timer%16==0):
            robot_info = update_robot(robot_info)
            timer = 0

        if(robot.step(timestep)==-1):
            exit()
        leftMotor = robot.getDevice('wheel1')
        rightMotor = robot.getDevice('wheel2')
        leftMotor.setPosition(float('inf'))
        rightMotor.setPosition(float('inf'))
        leftMotor.setVelocity(0.0)
        rightMotor.setVelocity(0.0)

        timer += 1
     #------------------CHANGE CODE BELOW HERE ONLY--------------------------
         #called every timestep
        if i == 0:
           gripper_release()
           robot_reset(fr, fl, br, bl)
           last_gps = []
           view_info = {}
           view_info_left = {}
           view_info_right = {}
           view_info_back = {}
           object_data = []
           object_data_left = []
           object_data_right = []
           object_data_back = []
           stuck_time = 0
           stuck_flag = False
           berry_stuck_tries = 0
           flag = True
           last_gps = gps.getValues()
        if i % 3 == 0:
            image = camera3.getImageArray()
            if image:
                data = np.array(image, dtype = np.uint8)
                object_data = object_info(data, camera3.getHeight(), camera3.getWidth())
                view_info = zombie_berry_info(object_data, image, camera3.getWidth(), camera3.getHeight() )
        if i % 3 == 0:
            imageR = camera6.getImageArray()
            if imageR:
                data = np.array(imageR, dtype = np.uint8)
                object_data_right = object_info(data, camera6.getHeight(), camera6.getWidth())
                view_info_right = zombie_berry_info(object_data_right, imageR, camera6.getWidth(), camera6.getHeight())
                print("view info R", view_info_right)

        if i % 3 == 0:
            imageL = camera7.getImageArray()

            if imageL:
               data = np.array(imageL, dtype = np.uint8)
               object_data_left = object_info(data, camera7.getHeight(), camera7.getWidth())
               view_info_left = zombie_berry_info(object_data_left, imageL, camera7.getWidth(), camera7.getHeight())
               print("view info L", view_info_left)

        if i % 3 == 0:
            imageB = camera5.getImageArray()
            if imageB:
                data = np.array(imageB, dtype = np.uint8)
                object_data_back = object_info(data, camera5.getHeight(), camera5.getWidth())
                view_info_back = zombie_berry_info(object_data_back, imageB, camera5.getWidth(), camera5.getHeight())
                print("view info B", view_info_back)
        print(lastHealth,lastEnergy,"test robot infor and energy")
        # if ((robot_info[1]-lastEnergy[-2])==-20):
        #     worstBerry = lastBerry

        # if(len(lastHealth)>2 and (robot_info[1]-lastHealth[-2]) == 20 ):

        #     if(bestBerryEnergy<(robot_info[1]-lastHealth[-2])):
        #         print(bestBerryEnergy,"best Health berry")
        #         bestHealthBerry = lastBerry

        # if(len(lastEnergy)>2 and (robot_info[1]-lastEnergy[-2])==40 ):

        #     if(bestBerryEnergy<(robot_info[1]-lastEnergy[-2])):
        #         print(bestBerryEnergy,"best berry score")
        #         bestEnergyBerry = lastBerry
        #         bestBerryEnergy = robot_info[1]-lastEnergy[-2]

        if(view_info["wall"] and view_info_left["wall"]):
            turn_right(fr, fl, br, bl)
        if(view_info["wall"] and view_info_right["wall"]):
            turn_left(fr, fl, br, bl)
        # if(view_info["boundary"] and view_info_left["boundary"]):
        #     turn_right(fr, fl, br, bl)
        # if(view_info["boundary"] and view_info_right["boundary"]):
        #     turn_left(fr, fl, br, bl)
        # if(view_info["boundary"]):
        #     turn_right(fr, fl, br, bl)
        if(view_info["wall"]):
            turn_right(fr, fl, br, bl)
        else:
            maxZombie = 0
            avoid = "center"
            front = False
            left = False
            right = False
            noZombie = True
            for zombie in zombie_list:
                if(view_info[zombie]):
                    noZombie = False
                    for singleZombie in view_info[zombie]:
                        if(len(singleZombie)>2 and singleZombie[1] > maxZombie):
                            maxZombie = singleZombie[1]
                            avoid = "center"
                            front = True
            for zombie in zombie_list:
                if(view_info_left[zombie]):
                    noZombie = False
                    for singleZombie in view_info_left[zombie]:
                        if(len(singleZombie)>2 and singleZombie[1] > maxZombie):
                            maxZombie = singleZombie[1]
                            avoid = "left"
                            left = True

            for zombie in zombie_list:
                if(view_info_right[zombie]):
                    noZombie = False
                    for singleZombie in view_info_right[zombie]:
                        if(len(singleZombie)>2 and singleZombie[1] > maxZombie):
                            maxZombie = singleZombie[1]
                            avoid = "right"
                            right = True
            for zombie in zombie_list:
                if(view_info_back[zombie]):
                    noZombie = False
                    for singleZombie in view_info_back[zombie]:
                        if(len(singleZombie)>2 and singleZombie[1] > maxZombie):
                            maxZombie = singleZombie[1]
                            avoid = "straight"
            maxBerry = 0
            move = "center"
            # noBerries = True
            for berry in berry_list:
                if(view_info[berry]):
                    # noBerries = False
                    for singleBerry in view_info[berry]:
                        if(len(singleBerry)>2 and singleBerry[1] > maxBerry ):
                            maxBerry = singleBerry[1]
                            lastBerry = berry
                            move = singleBerry[2]
                # noBerriesR = True
            for berry in berry_list:
                if(view_info_right[berry]):
                    # noBerriesR = False
                    for singleBerry in view_info_right[berry]:
                        if(len(singleBerry)>2 and singleBerry[1] > maxBerry):
                            maxBerry = singleBerry[1]
                            lastBerry = berry
                            move = "right"
            for berry in berry_list:
                if(view_info_left[berry]):
                    # noBerriesR = False
                    for singleBerry in view_info_left[berry]:
                        if(len(singleBerry)>2 and singleBerry[1] > maxBerry):
                            maxBerry = singleBerry[1]
                            lastBerry = berry
                            move = "left"
            go_straight(fr, fl, br, bl)
            if( not noZombie and maxZombie<110):
                print("avoid", avoid)
                if(front ==True and left == True and right == True):
                    go_straight(fr, fl, br, bl,14)
                elif(avoid == "center"):
                    turn_right(fr, fl, br, bl,14)
                elif (avoid == "right"):
                    turn_left(fr, fl, br, bl,14)
                elif(avoid == "straight"):
                    go_straight(fr, fl, br, bl,14)
                else:
                    turn_right(fr, fl, br, bl,14)
            if(robot_info[1]<25 or noZombie or(robot_info[1]<50 and maxZombie>110)):
                # if(maxBerry>maxZombie):
                #     print("chase berry first")
                print("move", move)
                if(move == "center"):
                    go_straight(fr, fl, br, bl)
                elif (move == "right"):
                    turn_right(fr, fl, br, bl)
                else:
                    turn_left(fr, fl, br, bl)
        # -----------------------stuck-------------------------------
        now_gps = gps.getValues()
        stuck_time, stuck_flag = is_stuck(now_gps,last_gps,stuck_time)
        print("stuck",stuck_time, stuck_flag)
        wall = wall_test(image,  camera3.getWidth(), camera3.getHeight())
        print("wall",wall)
        if (wall):
            turn_right(fr, fl, br, bl,14)
        if ((i > 10 and stuck_flag) and wall != True):
                
            for berry in berry_list:
                if view_info[berry] or view_info["possible berries"]:
                    print("berries")
                    go_straight(fr, fl, br, bl, 3)
                    # grip_berries()
                    stuck_flag = False
                    berry_stuck_tries += 1
                    break
            print("stuck",stuck_flag, berry_stuck_tries)
            if (stuck_flag or berry_stuck_tries > 2):
                berry_stuck_tries = 0
                if flag:
                    # speed += 2
                    grip_berries()
                    go_back(fr, fl, br, bl, 14)
                    flag = not flag
                else:
                    turn_right(fr, fl, br, bl, 14)
                    flag = not flag

        last_gps = gps.getValues()


        # -----------------------stuck-------------------------------

        #possible pseudocode for moving forward, then doing a 90 degree left turn
        #if i <100
            #base_forwards() -> can implement in Python with Webots C code (/Zombie world/libraries/youbot_control) as an example or make your own

        #if == 100
            # base_reset()
            # base_turn_left()
            #it takes about 150 timesteps for the robot to complete the turn

        #if i==300
            # i = 0
        lastEnergy.append(int(robot_info[1]))
        print(bestEnergyBerry,"best berry")
        i+=1

        #make decisions using inputs if you choose to do so

        #------------------CHANGE CODE ABOVE HERE ONLY--------------------------


    return 0


main()
