from xmlrpc.client import _HostType
import pexpect
from pexpect import pxssh

'''
method to get a picture from a slave

parameter 1 : local name of the raspberry ex : piSlave.local or piMaster.local
parameter 2 : the name of the scan from which we want the picture
parameter 3 : the name of the picture we want 
'''
def getPictureFromSlave(slave_name, scan_name, picture_name):
    #create the ocject for the connection
    child = pexpect.spawn('scp pi@'+slave_name+':'+scan_name+'/'+picture_name+'.jpg '+scan_name+'/'+picture_name+'.jpg')
    #waiting for the terminal to ask for the password of the slave
    child.expect('pi@'+slave_name+'\'s password:')
    #writing the password of the slave
    child.sendline('pi')
    #reading the data
    data = child.read()
    print('job done, file loaded')



'''
method to take a picture with the camera of the slave

parameter 1 : local name of the raspberry ex : piSlave.local or piMaster.local
parameter 2 : the name of the scan from which we want the picture
parameter 3 : the name of the picture we want  
'''
def takePictureWithSlave(slave_name, scan_name, picture_name):
    try:
        ssh = pxssh.pxssh() #creating the ssh client
        username, password = 'pi', 'pi'
        ssh.login(slave_name, username, password) #connecting the ssh client 
        ssh.sendline('cd '+scan_name) #going into the folder of the scan
        ssh.sendline('libcamera-still -r -o '+picture_name+'.jpg')#taking and saving the picture)
        ssh.logout()
    
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed to login")
        print(str(e))

'''
method to take a picture with the camera of the slave

parameter 1 : local name of the raspberry ex : piSlave.local or piMaster.local
parameter 2 : the name of the scan from which we want the picture  
'''
def createFolderSlave(slave_name, scan_name):
    try:
        ssh = pxssh.pxssh()#creating ssh client
        username, password = 'pi', 'pi'
        ssh.login(slave_name, username, password)

    except pxssh.ExceptionPxssh as e:
        print("pxssh failed to login")
        print(str(e))

'''
method to delete the folder of a scan on a slave

parameter 1 : local name of the raspberry ex : piSlave.local or piMaster.local
parameter 2 : the name of the scan from which we want the picture  
'''
def cleanFolderSlave(slave_name, scan_name):
    try:
        ssh = pxssh.pxssh() #creating the ssh client
        username, password = 'pi', 'pi'
        ssh.login(slave_name, username, password)
        ssh.sendline('rm -rf scan_name')
        ssh.logout()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed to login")
        print(str(e))
