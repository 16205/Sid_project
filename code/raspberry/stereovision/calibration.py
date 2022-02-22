import cv2 
import numpy as np 
import os

#########################################################################################################
#################################   CALIRBRATION    #####################################################
#########################################################################################################
'''
methode qui retourne les caractéristiques du système nécessaires pour le traitement d'image
'''
def calibration():
    #on définit le chessboard
    number_of_square_X = 10
    number_of_square_Y = 8
    nX = number_of_square_X - 1 #le nombre de coins intérieur
    nY = number_of_square_Y - 1
    #les images sont dans le dossier configuration
    directory = "calibration"
    #on stocke les images modifiées dans un sous-dossier
    result_directory = "calibration/clalibration_result"
    #creating arrays to store the object points and the image points
    objpoints = [] #3D points in the real world space
    imgpoints = [] #2D points in the image plane
    #on prépare les coordonnées dans le chessboard des angles avec pour unité les cases
    objp = np.zeros((9*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2)
    #on fait une boucle for pout traiter automatiquement les images
    for filename in os.listdir(directory):
        filename = directory + '/' +filename
        print(filename)
        image = cv2.imread(filename)
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    
        # Find the corners on the chessboard
        success, corners = cv2.findChessboardCorners(gray, (nY, nX), None)
        
        # If the corners are found by the algorithm, draw them
        if success == True:
            objpoints.append(objp)
            #on ajoute les corners à la liste
            imgpoints.append(corners)
            # Draw the corners
            cv2.drawChessboardCorners(image, (nY, nX), corners, success)
            #on écrit les images modifiées dans un fichiers afin de les voir
            new_filename =  result_directory + filename[len(directory)+1::]    
            # Save the new image in the working directory
            cv2.imwrite(new_filename, image)
    print("calibration's images processing done")
    #on fait la calibration grâce à opencv
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return ret, mtx, dist, rvecs, tvecs

