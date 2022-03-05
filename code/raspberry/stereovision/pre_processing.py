#script to take out the red pixels of the image
import cv2
import os
import numpy as np

# function to display the coordinates of
# of the points clicked on the image
def click_event(event, x, y, flags, params):
 
    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, str(x) + ',' +
                    str(y), (x,y), font,
                    1, (255, 0, 0), 2)
        cv2.imshow('image', img)
 
    # checking for right mouse clicks    
    if event==cv2.EVENT_RBUTTONDOWN:
 
        # displaying the coordinates
        # on the Shell
        print(x, ' ', y)
 
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' +
                    str(g) + ',' + str(r),
                    (x,y), font, 1,
                    (255, 255, 0), 2)
        cv2.imshow('image', img)
 
# driver function
if __name__=="__main__":
 
    # reading the image
    img = cv2.imread(r'C:\Users\rapha\OneDrive\Documents\master1\Q2\projetRobotique\Sid_project\code\raspberry\stereovision\test_scan1_R_1_complet.jpg', 1)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
 
    # displaying the image
    cv2.imshow('image', img)
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()

# directory = "test_scan1"

# count = 0
# for filename in os.listdir(directory):
#     filename = directory + "/" + filename
#     image = cv2.imread(filename)
#     blue, green, red = cv2.split(image)
#     tresh = tresh_laser(red)
#     filename ='thresh' + str(count)+'result.jpg'
#     print(filename)
#     cv2.imwrite(filename,tresh)
#     count += 1
