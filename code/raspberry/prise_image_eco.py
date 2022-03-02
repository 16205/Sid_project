import os
import cv2
import pexpect
from pexpect import pxssh
import prise_image

def scan (name_scan, step_number):
    #############################################################
    #first we create ssh client and connect it to the slave
    try:
        ssh = pxssh.pxssh() #on crée le client
        hostname, username, password ='piSlave.local', 'pi', 'pi'
        ssh.login(hostname, username, password) #on connecte le client
        cap = cv2.VideoCapture(0) #creating the opencv object to take frames

        ############################################################
        #second we create a directories to store the images in the master and in the slave
        os.system('mkdir '+name_scan) #create the directory
        ssh.sendline('mkdir '+name_scan) #creating a directory in the slave to store the image

        ############################################################
        #third we make a loop to take all the pictures with the slave and with the master
        for i in range(step_number):
            name_picture_r = name_scan+"_R_"+str(i) #create the file name for the i th picture from the rigth camera
            name_picture_l = name_scan+"_L_"+str(i) #create the filename for the i th picture from the left camera
            os.system('mkdir '+name_picture_r) #on lance le script de prise d'image sur le master
            ssh.sendline('mkdir '+name_picture_r) #on lance le script de prise d'image sur le master
            

    except pxssh.ExceptionPxssh as e:
        print(str(e))