#script to take the images for a scan
#arg1 : the scan's name
#arg2 : the number of steps
import cv2
import os
import pexpect
from pexpect import pxssh
import sys
import sshTools

#reading the scan_name from the input 
scan_name = sys.argv[1]
step_nbr = sys.argv[2]

#on crée le client ssh pout le slave
try:
    ssh  = pxssh.pxssh()
    hostname, username, password ='piSlave.local', 'pi', 'pi'
    ssh.login(hostname, username, password) #on connecte le client
except pxssh.ExceptionPxssh as e:
    print(str(e))

#on crée les dossier pour le scan dans le master et dans la slave 
os.system('mkdir '+ scan_name) #on crée le dossier dans le master
sshTools.createFolderSlave(ssh, scan_name) #on crée le dossier dans le slave


for i in range(step_nbr):
    name_picture_r = scan_name +"_R_"+str(i) #create the file name for the i th picture from the rigth camera
    name_picture_l = scan_name+"_L_"+i #create the filename for the i th picture from the left camera
    #on prend les images 
    os.system('python3 prise_image_bon.py '+scan_name+' '+name_picture_r) #on pose que le master sera la camera de droite
    sshTools.takePictureWithSlave(ssh, scan_name, name_picture_l)
    