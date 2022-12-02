"""youbot_controller controller."""

from controller import Robot, Motor, Camera, Accelerometer, GPS, Gyro, LightSensor, Receiver, RangeFinder, Lidar
from controller import Supervisor
import numpy as np



from youbot_zombie import *
from img_detection import *
import struct
#...
MAX_SPEED = 14
Speed = 4.0

#------------------CHANGE CODE BELOW HERE ONLY--------------------------
#define functions here for making decisions and using sensor inputs

def robot_reset(fr, fl, br, bl):
    fr.setVelocity(0)
    fl.setVelocity(0)
    br.setVelocity(0)
    bl.setVelocity(0)
def turn_left(fr, fl, br, bl,  speed =  MAX_SPEED):
    print("turning left")
    fr.setVelocity(speed/2)
    fl.setVelocity(-speed)
    br.setVelocity(speed/2)
    bl.setVelocity(-speed)


def turn_right(fr, fl, br, bl, speed =  MAX_SPEED):
    print("turning right")
    fr.setVelocity(-speed)
    fl.setVelocity(speed/2)
    br.setVelocity(-speed)
    bl.setVelocity(speed/2)


def go_straight(fr, fl, br, bl, speed =  MAX_SPEED):
    print("go straight")
    fr.setVelocity(speed)
    fl.setVelocity(speed)
    br.setVelocity(speed)
    bl.setVelocity(speed)


#------------------CHANGE CODE ABOVE HERE ONLY--------------------------

def main():
    robot = Supervisor()

    # get the time step of the current world.
    timestep = int(robot.getBasicTimeStep())

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


    i=0
    zombie_list = ['green zombie','blue zombie','aqua zombie','purple zombie']
    berry_list = ['red berry','yellow berry','orange berry','pink berry','possible berries']


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
        print(camera1.hasRecognition()," 1")
        print(camera2.hasRecognition()," 2")
        print(camera3.hasRecognition()," 3")
        print(camera4.hasRecognition()," 4")
        print(camera5.hasRecognition()," 5")
        print(camera6.hasRecognition()," 6")
        print(camera7.hasRecognition()," 7")
        print(camera8.hasRecognition()," 8")
        # object = camera1.getRecognitionObjects()

        # if object:
    # display the components of each pixel
          # for x in range(0,camera1.getWidth()):
             # for y in range(0,camera1.getHeight()):
                # red   = image[x][y][0]
                # green = image[x][y][1]
                # blue  = image[x][y][2]
                # gray  = (red + green + blue) / 3
                # print('r='+str(red)+' g='+str(green)+' b='+str(blue))
                # print(object)

     #------------------CHANGE CODE BELOW HERE ONLY--------------------------
         #called every timestep

        robot_reset(fr, fl, br, bl)
        print("camera image\n")
        print(camera3.getWidth())
        print(camera3.getHeight())

        image = camera3.getImageArray()
        view_info = {}
        object_data = []
        if image:
            # for x in range(0,camera2.getWidth()):
            #     for y in range(0,camera2.getHeight()):
            #         red.append(image[x][y][0])
            #         green.append(image[x][y][1])
            #         blue.append(image[x][y][2])
            #         gray.append((image[x][y][0] + image[x][y][1] + image[x][y][2]) / 3)
            data = np.array(image, dtype = np.uint8)
            object_data = object_info(data, camera3.getHeight(), camera3.getWidth())
            view_info = zombie_berry_info(object_data, image, camera3.getWidth(), camera3.getHeight(), )
            print("view info", view_info)

            for zombie in zombie_list:

                if(view_info[zombie]):
                    for singleZombie in view_info[zombie]:
                        if(singleZombie[2] == "center"):
                            turn_right(fr, fl, br, bl)
                        elif (singleZombie[2] == "right"):
                            turn_left(fr, fl, br, bl)
                        else:
                            turn_right(fr, fl, br, bl)

            maxBerry = 0
            move = "center"
            for berry in berry_list:
                if(view_info[berry]):
                    for singleBerry in view_info[berry]:
                        if(singleBerry[1] > maxBerry):
                            maxBerry = singleBerry[1]
                            move = singleBerry[2]
            print("move", move)
            if(move == "center"):
                go_straight(fr, fl, br, bl)
            elif (move == "right"):
                go_straight(fr, fl, br, bl)
                turn_right(fr, fl, br, bl)
            else:
                go_straight(fr, fl, br, bl)
                turn_left(fr, fl, br, bl)

        #possible pseudocode for moving forward, then doing a 90 degree left turn
        #if i <100
            #base_forwards() -> can implement in Python with Webots C code (/Zombie world/libraries/youbot_control) as an example or make your own

        #if == 100
            # base_reset()
            # base_turn_left()
            #it takes about 150 timesteps for the robot to complete the turn

        #if i==300
            # i = 0

        #i+=1

        #make decisions using inputs if you choose to do so

        #------------------CHANGE CODE ABOVE HERE ONLY--------------------------


    return 0


main()
