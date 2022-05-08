import cv2
import numpy as np
import os
import time
import sys
# from picamera.array import PiRGBArray
# from picamera import PiCamera

#########################################################################################################
#################################   CALIRBRATION    #####################################################
#########################################################################################################
'''
methode qui retourne les caractéristiques du système nécessaires pour le traitement d'image
'''
def calibration(nx = 10, ny = 8):
    
    # Capture calibration images
    captureCalibPics()
    
    #on définit le chessboard
    number_of_square_X = nx
    number_of_square_Y = ny
    nX = number_of_square_X - 1 #le nombre de coins intérieur
    nY = number_of_square_Y - 1
    #les images sont dans le dossier configuration
    directory = "calibration"
    #on stocke les images modifiées dans un sous-dossier
    os.system('mkdir calibration/calibration_result')
    result_directory = "calibration/calibration_result"
    #creating arrays to store the object points and the image points
    objpoints = [] #3D points in the real world space
    imgpoints = [] #2D points in the image plane
    #on prépare les coordonnées dans le chessboard des angles avec pour unité les cases
    objp = np.zeros((nX*nY,3), np.float32)
    objp[:,:2] = np.mgrid[0:nX,0:nY].T.reshape(-1,2)
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
            new_filename = result_directory + '/'+ filename[len(directory)+1::]
            # Save the new image in the working directory
            cv2.imwrite(new_filename, image)
    print("calibration's images processing done")
    #on fait la calibration grâce à opencv
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return mtx, dist, rvecs, tvecs
    
def captureCalibPics():
    
    # Camera init
    # camera = PiCamera()
    # rawCapture = PiRGBArray(camera)

    # get the slave video feed
    slave_cam = cv2.VideoCapture("rtsp://pislave.local:8080/",cv2.CAP_FFMPEG)
    slave_cam.set(cv2.CAP_PROP_BUFFERSIZE, 10) # 10 pics in the buffer

    # get master video feed
    master_cam = cv2.VideoCapture(0)
    
    # 1st prompt
    print("Please place the chessboard in both camera's views, and do not move it until next prompt.")

    # Timer display in terminal
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("1st capture in {:2d} seconds".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)
    
    # Capture c1Right.jpg from Master camera
    # camera.capture(rawCapture, format='bgr')
    # img = rawCapture.array
    # cv2.imwrite('./raspberry/stereovision/calibration/c1Right.jpg', img)

    # Capture slave & master
    ret_s, frame_s = slave_cam.read()
    ret_m, frame_m = master_cam.read()
    while True:
        if (ret_m == True):
            print("writing master pic 1")
            cv2.imwrite('./raspberry/stereovision/calibration/c1Right.jpg', frame_m)
            break
    while True:
        if (ret_s == True):
            print("writing slave pic 1")
            cv2.imwrite('./raspberry/stereovision/calibration/c1Left.jpg', frame_s)
            break
    
    sys.stdout.write("\rFirst step complete!         \n")
    
    # 2nd prompt 
    print("Please move the chessboard slightly by changing its perspective, without rotating it around its normal vector, and do not move it until next prompt.")
    
    # Timer display in terminal
    for remaining in range(10, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("2nd capture in {:2d} seconds".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)
        
    # Capture c2Right.jpg from Master camera
    # camera.capture(rawCapture, format='bgr')
    # img = rawCapture.array
    # cv2.imwrite('./raspberry/stereovision/calibration/c2Right.jpg', img)

    # Capture slave & master
    ret_s, frame_s = slave_cam.read()
    ret_m, frame_m = master_cam.read()
    while True:
        if (ret_m == True):
            print("writing master pic 2")
            cv2.imwrite('./raspberry/stereovision/calibration/c2Right.jpg', frame_m)
            break
    while True:
        if (ret_s == True):
            print("writing slave pic 2")
            cv2.imwrite('./raspberry/stereovision/calibration/c2Left.jpg', frame_s)
            break
    
    # slave_cam.release()
    master_cam.release()
    # 3rd prompt
    print("The image capture for the calibration is now complete, please wait until calibration is finished.")