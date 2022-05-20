import cv2 
import numpy as np
import os 


def getLaser(scan_name):
    dirleft = scan_name + "/generated/3tresh/Left/"
    dirRight = scan_name + "/generated/3tresh/Right/"
    length = len(os.listdir(scan_name+"/scanLeft"))
    count = 0
    for i in range(1,length,1):
        print(i)
        if i < 10:
            pict_name_left = '000' + str(i) + '.png'
            pict_name_right = 'scan000' + str(i) + '.png'
        else :
            pict_name_left = '00' + str(i) + '.png'
            pict_name_right = 'scan00' + str(i) + '.png'
        # pict_name_left = scan_name+"_L_" + str(i) + ".jpg"
        # pict_name_right = scan_name+"_R_" + str(i) + ".jpg"

        print(pict_name_left)
        print(pict_name_right)

        img_left = cv2.imread(scan_name+"/scanLeft/"+pict_name_left)
        img_right = cv2.imread(scan_name+"/scanRight/"+pict_name_right)     

        lowerBound = np.array([0, 0, 230])
        upperBound = np.array([255, 255, 255])

        mask_left = cv2.inRange(img_left, lowerBound, upperBound)
        mask_right = cv2.inRange(img_right, lowerBound, upperBound)

        cv2.imwrite(dirleft+str(count)+".jpg", mask_left)
        cv2.imwrite(dirRight+str(count)+".jpg", mask_right)
        print(np.shape(mask_left))

        count+=1


getLaser("scan")