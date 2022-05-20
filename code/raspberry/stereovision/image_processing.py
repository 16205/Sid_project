from turtle import left
import cv2
import numpy as np
import os
import jsonTools as js
from mathTools import *
from mathutils import geometry as pygeo
from mathutils import Vector


#find the pixels of the laser and select one of the line
def getRedPixels(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = []
    y_line = 0
    for line in img_gray:
        x_pix = 0
        moy = 0
        count = 0
        for pixel in line:
            if pixel>100:
                moy = moy + x_pix
                count += 1
            x_pix+=1
        if count != 0:
            moy = moy/count
        if moy!=0:
            coord = np.array([[moy, y_line, 1]]) #on fixe le s = 1 cela fera aussi matcher les dimensions de points et de la mat fond
            coords.append(coord.tolist())
        y_line+=1
    return coords

def getEpilines(red_pixels, F):
    epilines = []
    for pixel in red_pixels:
        epilines.append(F @ pixel[0])
    return epilines


def matchLeftAndRightPixels(red_pixels_right, epilines, red_pixels_left):
    left_right_pixels = []
    for i in range(len(epilines)):
        for pixel_right in red_pixels_right:
            if pixelBelong2Epiline(epilines[i], pixel_right[0]):
                left_right_pixels.append([red_pixels_left[i][0], pixel_right[0]])
    return left_right_pixels


def computeWorldCoordinates(left_right_pixels, camWorldCenterRight, camWorldCenterLeft, camLeft, camRight):
    points = []
    leftObjects = []
    rightObjects = []
    for pixels in left_right_pixels:
        left_pixel = np.array(pixels[0])
        right_pixel = np.array(pixels[1])

        camCenterRight = np.transpose(camWorldCenterRight)[0]
        camCenterLeft = np.transpose(camWorldCenterLeft)[0]
    
        # Obtenir les coordonnées 3D monde/objet de tous les points
        leftObject = (np.linalg.pinv(camLeft) @ left_pixel)
        leftObjects.append(leftObject)
        rightObject = (np.linalg.pinv(camRight) @ right_pixel) 
        rightObjects.append(rightObjects)
        # Points caractéristiques des lignes rétro-projetées
        leftEndVec = arrayToVector(leftObject)
        rightEndVec = arrayToVector(rightObject)
        leftStartVec = arrayToVector(camCenterLeft)
        rightStartVec = arrayToVector(camCenterRight)

        # Intersection entre deux lignes rétroprojetées = point du monde réel
        try:
            points.append(list(pygeo.intersect_line_line(leftStartVec,leftEndVec,rightStartVec,rightEndVec))[0]*10)
        except:
            pass

    return points, leftObjects, rightObjects


   
