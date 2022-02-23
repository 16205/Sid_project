
import os
import pexpect
from pexpect import pxssh

def getPictureSlave(scan_name, picture_name):
    #create the object to interact with the terminal
    child = pexpect.spawn('scp pi@piSlave.local:'+scan_name+'/'+picture_name+'.jpg  '+scan_name+'/'+picture_name+'.jpg')
    #waiting for the terminal to ask for the password of the slave
    child.expect('pi@pislave.local\'s password:')
    #writing the password of the slave
    child.sendline('pi')
    #reading the data
    data = child.read()
    print(data)
    #closing the conenection
    child.close()
    print('job done file loaded')

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
        ssh.sendline('mkdir '+name_scan) #creating a directory in the slave to store the images


        ############################################################
        #third we make a loop to take all the pictures with the slave and with the master
        for i in range(step_number):
            name_picture_r = name_scan+"_R_"+str(i) #create the file name for the i th picture from the rigth camera
            name_picture_l = name_scan+"_L_"+str(i) #create the filename for the i th picture from the left camera

            #we assume that the master has the rigth camera and the slave the left one
            os.system('raspistill -o '+name_scan+'/'+name_picture_r+".jpg") #taking the image from the master
            ssh.sendline('raspistill -o '+name_scan+'/'+name_picture_l+'.jpg')#taking picture with the slave

    except pxssh.ExceptionPxssh as e:
        print(str(e))

def get_pictures(name_scan, step_number):
	for i in range(step_number):
		name_picture_l = name_scan+"_L_"+str(i) #create the filename for the i th picture from the left camera
		getPictureSlave(name_scan, name_picture_l)

scan('test_scan', 10)
get_pictures('test_scan', 10)

