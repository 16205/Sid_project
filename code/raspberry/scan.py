#arg1 : the scan's name
#arg2 : the number of steps
import cv2
import os
import pexpect
from pexpect import pxssh
import sys
import sshTools
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
# import jsonTools as jt
# import red_pixs as rp
# from msilib.schema import Directory
from stepper import *
from laser import *
# reading the scan_name from the input
# scan_name = sys.argv[1]
# quality = sys.argv[2]

def runScan(quality, laser_power = 30, color_space="Red", scale=10, scan_name = "test"):
    """
    Run the scan : activate stepper and take pictures\n
    Params:\n
    - quality = step size ("High","Medium","Low","test")\n
    - laser_power = output power in pwm (0 to 100)\n
    - color_space = color spectrum to work with ("Saturation", "Hue","Red")\n
    - scale = size of the piece to scan (5,10,15,20)\n
    - scan_name = name of the scan (if None => 'test')
    """

    # on crée les dossier pour le scan dans le master et dans la slave 
    os.system('mkdir '+ scan_name) #on crée le dossier dans le master
    sshTools.createFolderSlave(scan_name) #on crée le dossier dans le slave
    print("folders created")
    
    print(scan_name)
    print(quality)

    # define GPIO pins for the motor
    GPIO.setmode(GPIO.BCM)

    # defining the caracteristic of on step of the motor
    if quality == "test":
        step_number = 10
        step_size = "Full"
        step_nbr = 100
    elif quality == "Low":
        step_number = 10
        step_size = "1/4"
        step_nbr = 400
    elif quality == "Medium":
        step_number = 4
        step_size = "1/4"
        step_nbr = 1000
    elif quality == "High":
        step_number = 1
        step_size = "1/4"
        step_nbr = 4000
    
    # turn led On
    setDuty(laser_power)
    turnLaserOn()

    for i in range(1, step_nbr):

        name_picture_r = scan_name +"_R_"+str(i) # create the file name for the i th picture from the rigth camera
        name_picture_l = scan_name+"_L_"+str(i)  # create the filename for the i th picture from the left camera
        # on prend les images
        print("name_picture_r = ", name_picture_r)
        print("name_picture_l = ", name_picture_l)

        os.system('python3 prise_image_bon.py '+scan_name+' '+name_picture_r) #on pose que le master sera la camera de droite
        print("im master taken")
        sshTools.takePictureWithSlave(scan_name, name_picture_l)
        print("im slave taken")

        # Run the stepper
        time.sleep(4)
        makeStep(step_number,step_size, doEnd=True)
        time.sleep(0.2)
        
    for i in range(1, step_nbr):
        #on recup l'image qu'on vient de prendre
        sshTools.getPictureSlave(scan_name, scan_name+"_L_"+str(i) )
        time.sleep(2)
        
    # turn laser off
    turnLaserOff()




    GPIO.cleanup() # clear GPIO allocations after run
    
#runScan("test")

def scan2json(scan_name):
    jt.build_Json4scan(scan_name)
    files = os.listdir(scan_name)
    json_name = scan_name + '.json'
    for i in range(len(files)/2):
        if i != 113:
            #on intègre l'imagede gauche dans le json 
            picture_name = scan_name+'_L_'+str(i)+'.jpg'
            pict_path = scan_name+'/'+picture_name
            img = cv2.imread(pict_path)
            coords = rp.get_red_points_coordinates(img,'saturation')
            jt.addNpArray2Json(coords, json_name, picture_name)
            #on intègre l'image de droite dans le json 
            picture_name = scan_name+'_R_'+str(i)+'.jpg'
            pict_path = scan_name+'/'+picture_name
            img = cv2.imread(pict_path)
            coords = rp.get_red_points_coordinates(img,'saturation')
            jt.addNpArray2Json(coords, json_name, picture_name)


def scan2jsonFinal(scan_name, color):
        jt.build_Json4scan(scan_name)
        files = os.listdir(scan_name)
        json_name = scan_name + '.json'
        dico = {}
        for i in range(int(len(files)/2)):
            if i != 113:
                #on intègre l'imagede gauche dans le json 
                picture_name = scan_name+'_L_'+str(i)+'.jpg'
                pict2Dico(scan_name, picture_name, color, dico)
                #on intègre l'image de droite dans le json
                picture_name = scan_name+'_R_'+str(i)+'.jpg'
                pict2Dico(scan_name, picture_name, color, dico)
                print(i)
        jt.Dico2Array(dico, json_name)

def pict2Dico(scan_name, picture_name, color, dico):
    pict_path = scan_name+'/'+picture_name
    img = cv2.imread(pict_path)
    coords = rp.get_avg_red_pixs(img,color)
    list = coords.tolist()
    dico.update({picture_name:list})