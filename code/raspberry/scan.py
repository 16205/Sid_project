#arg1 : the scan's name
#arg2 : the number of steps
import cv2
import os
import pexpect
from pexpect import pxssh
import sys
#import sshTools as sshTools
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
# import jsonTools as jt
# import red_pixs as rp
# from msilib.schema import Directory

try:
    import sshTools as sshTools
    from stepper import *
    from laser import *
    from copy_slave_pics import *
    from prise_image_bon import *
except:
    import raspberry.sshTools 
    from raspberry.stepper import *
    from raspberry.laser import *
    from raspberry.copy_slave_pics import *
    from raspberry.prise_image_bon import *
# reading the scan_name from the input
# scan_name = sys.argv[1]
# quality = sys.argv[2]

def runScan(quality, laser_power = 70, color_space="Red", scale=10, scan_name = "test1"):
    """
    Run the scan : activate stepper and take pictures\n
    Params:\n
    - quality = step size ("High","Medium","Low","test")\n
    - laser_power = output power in pwm (0 to 100)\n
    - color_space = color spectrum to work with ("Saturation", "Hue","Red")\n
    - scale = size of the piece to scan (5,10,15,20)\n
    - scan_name = name of the scan (if None => 'test')
    """
    # initialize the camera and grab a reference to the raw camera capture  
    camera = PiCamera()
    camera.resolution = (1640,1232)
    # on crée les dossier pour le scan dans le master et dans la slave 
    os.system('mkdir /home/pi/Sid_project/scans/'+ scan_name) #on crée le dossier dans le master
    os.system('mkdir /home/pi/Sid_project/scans/'+ scan_name+'/'+"scanRight") #on crée le sous dossier de scan qui sera pour les images de droite
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
        print(i)

        name_picture_r = scan_name +"_R_"+str(i) # create the file name for the i th picture from the rigth camera
        name_picture_l = scan_name+"_L_"+str(i)  # create the filename for the i th picture from the left camera
        # on prend les images
        print("name_picture_r = ", name_picture_r)
        print("name_picture_l = ", name_picture_l)

        # Master image capture
        imageCapture(scan_name, name_picture_r, camera) # Master = right camera
        print("Master captured image")

        # take picture on the slave
        try: 
            # TODO: put the pictures inside /mnt/home/pi/scans/{scan_name}
            
            sshTools.takePictureWithSlave(scan_name, name_picture_l, i)

            print("Slave captured image")
            
        except os.system.error as e:
            print(str(e))
        
        # Run the stepper
        time.sleep(5)
        makeStep(step_number,step_size, doEnd=True)
        time.sleep(0.2)

    # copy slave images into the master scan folder
    copy_slave_pics(scan_name)
        
    # for i in range(1, step_nbr):
    #     #on recup l'image qu'on vient de prendre

    #     sshTools.getPictureSlave(scan_name, scan_name+"_L_"+str(i) )
    #     time.sleep(2)
        
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
#arg1 : the scan's name
#arg2 : the number of steps
#arg1 : the scan's name
#arg2 : the number of steps
