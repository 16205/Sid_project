import pexpect
from pexpect import pxssh
'''
method to get a picture back from the slave

the parameters is the name of the picture and the name o the scan
'''
def getPictureSlave(scan_name, picture_name):
    #create the object to interact with the terminal
    child = pexpect.spawn('scp pi@piSlave.local:'+scan_name+'/'+picture_name+'.jpg '+scan_name+'/'+picture_name+'.jpg')
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

the parameters are the name of the scan and the name of the picture to take
'''
def  takePictureWithSlave(scan_name, picture_name):
    try:
        ssh = pxssh.pxssh() #creating the ssh client
        hostname = 'piSlave.local'
        username = 'pi'
        password = 'pi'
        ssh.login(hostname, username, password) #connecting the ssh client
        ssh.sendline('cd '+scan_name) #going into the folder of the scan
        ssh.sendline('libcamera-still -r -o '+picture_name+'.jpg')#taking and saving the picture
        ssh.logout()

    except pxssh.ExceptionPxssh as e:
        print("pxssh failed to login")
        print(str(e))

'''
method to create a folder to store the pictures of a scan

parameters is the name of the folder to create
'''
def createFolderSlave(folder_name):
    try:
        ssh = pxssh.pxssh() #creating the ssh client
        hostname = 'piSlave.local'
        username = 'pi'
        password = 'pi'
        ssh.login(hostname, username, password) #connecting the ssh client
    except pxssh.ExceptionPxssh as e:
        print("connection failed to login")
        print(str(e))

