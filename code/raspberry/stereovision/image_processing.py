import cv2
import numpy as np

def img_processing(ret, mtx, dist, rvecs, tvecs):
    #on transforme le rvecs en matrice 3x3
    #rotation matrix => convert vector to matrix
    rmatRight = cv2.Rodrigues(rvecs[0])[0]
    rmatLeft = cv2.Rodrigues(rvecs[2])[0]
    #full [R|t] matrix => add t in R
    rotMatRight = np.concatenate((rmatRight,tvecs[0]), axis=1)
    rotMatLeft = np.concatenate((rmatLeft,tvecs[0]), axis=1)
    #camera matrix (A [R|t])
    camLeft = mtx @ rotMatLeft #matrice de projection de la caméra de gauche
    camRight = mtx @ rotMatRight #matrice de projectio de ma caméra de droite
    # find cx and cy for both cameras
    camWorldCenterLeft = np.linalg.inv(np.concatenate((rotMatLeft,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
    camWorldCenterRight = np.linalg.inv(np.concatenate((rotMatRight,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
