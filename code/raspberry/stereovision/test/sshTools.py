import os
import pexpect
from pexpect import pxssh
'''
method to get a picture back from the slave

the parameters is the name of the picture and the name o the scan
'''
def getPictureSlave(scan_name, picture_name):
    #create the object to interact with the terminal
    child = pexpect.spawn('scp pi@piSlave.local:'+scan_name+'/'+picture_name+'.jpg ' +picture_name+'.jpg')
    #waiting for the terminal to ask for the password of the slave
    child.expect('pi@pislave.local\'s password:')
    #writing the password of the slave
    child.sendline('pi')
    #reading the data 
    data = child.read()
    print(data)
    #closing the conenection
    child.close()
    print('job done file loaded', )

'''
method to take a picture with the camera of the slave
the picture will be stored in the folder of the current scan

the parameters are the ssh client, the name of the scan and the name of the picture to take
'''
def  takePictureWithSlave(scan_name, picture_name):
    try:
        ssh  = pxssh.pxssh()
        hostname, username, password ='piSlave.local', 'pi', 'pi'
        ssh.login(hostname, username, password, sync_multiplier=5, auto_prompt_reset=False) #on connecte le client
        ssh.sendline('python3 prise_image_bon.py '+scan_name+' '+picture_name)#taking and saving the picture
        ssh.logout()

    except pxssh.ExceptionPxssh as e:
        print("pxssh failed to login")
        print(str(e))

'''
method to create a folder to store the pictures of a scan

param1 : the ssh client to connect 
param2 : the name of the folder to create
'''
def createFolderSlave(folder_name):
    try:
        ssh = pxssh.pxssh()
        hostname, username, password ='piSlave.local', 'pi', 'pi'
        ssh.login(hostname, username, password, sync_multiplier=5, auto_prompt_reset=False) #on connecte le client
        ssh.sendline('mkdir '+folder_name)
        ssh.logout()
    except pxssh.ExceptionPxssh as e:
        print("connection failed to login")
        print(str(e))


def scan (name_scan, step_number):
     ############################################################
    #first we create ssh client and connect it to the slave 
    try:
        ssh = pxssh.pxssh() #on crée le client 
        hostname, username, password ='piSlave.local', 'pi', 'pi'
        ssh.login(hostname, username, password) #on connecte le client

        ############################################################
        #second we create a directories to store the images in the master and in the slave
        os.system('mkdir '+name_scan) #create the directory
        ssh.sendline('mkdir '+name_scan)#creating a directory in the slave to store the images

        ############################################################
        #third we make a loop to take all the pictures with the slave and with the master
        for i in range(step_number):
            name_picture_r = name_scan+"_R_"+str(i) #create the file name for the i th picture from the rigth camera
            name_picture_l = name_scan+"_L_"+i #create the filename for the i th picture from the left camera

            #we assume that the master has the rigth camera and the slave the left one 
            os.system('raspistill -o '+name_picture_r+".jpg") #taking the image from the master 
            ssh.sendline('libcamera-still -o '+name_picture_l+'.jpg')#taking picture with the slave
            getPictureSlave(name_scan,name_picture_l)#loadinf the picture from the slave in the master's directory



    except pxssh.ExceptionPxssh as e:
        print(str(e))

