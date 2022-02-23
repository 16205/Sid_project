import cv2
import numpy as np

'''
methode qui retourne les caractéristique de la camera 

param 1 : mtx, la matrice de la camera  f_x     0      c_x
                                        0       f_y    c_y
                                        0       0       1     
param 2 : dist, vecteur des coefficient de distorstion

param3 : rvecs, l'ensemble des vecteur de rotation (1 par image de calibration)

param4 : tvecs l'ensemble des vecteur de transpositions (1 par image de calibration)

out1 : rmatRight = matrice de rotation de la camera de droite
out2 : rmatLeft = matrice de rotation de la camera de gauche

out3 : rotMatRight = full [R|t] matrix pour la camera de droite
out4 : rotMatLeft = full [R|t] matrix pour la camera de gauche

out5 : camRight matrice de projection de la camera de droite
out6 : camLeft matrice de projection de la camera de gauche

out7 : camWorldCenterRight coordonnées monde du centre optique de la camera de droite
out8 : camWorldCenterLeft coordonnées monde du centre optique de la camera de gauche
'''
def comute_camera_caracteristics(mtx, dist, rvecs, tvecs):
    #on transforme le rvecs en matrice 3x3
    #rotation matrix => convert vector to matrix
    rmatRight = cv2.Rodrigues(rvecs[0])[0] #verrifier l'ordre des images de calibration
    rmatLeft = cv2.Rodrigues(rvecs[2])[0] #verrifier l'ordre des images de calibration
    #full [R|t] matrix => add t in R
    rotMatRight = np.concatenate((rmatRight,tvecs[0]), axis=1)
    rotMatLeft = np.concatenate((rmatLeft,tvecs[0]), axis=1)
    #camera matrix (A [R|t]) 
    camLeft = mtx @ rotMatLeft #matrice de projection de la caméra de gauche
    camRight = mtx @ rotMatRight #matrice de projectio de ma caméra de droite
    # find cx and cy for both cameras
    camWorldCenterLeft = np.linalg.inv(np.concatenate((rotMatLeft,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
    camWorldCenterRight = np.linalg.inv(np.concatenate((rotMatRight,[[0,0,0,1]]), axis=0)) @ np.transpose([[0,0,0,1]])
    return rmatRight, rmatLeft, rotMatRight, rotMatLeft, camRight, camLeft, camWorldCenterRight, camWorldCenterLeft

'''
methode qui retourne un vecteur dans une matrice afin de calculer
le produit vectoriel sous forme de produit matriciel

pour plus d'info : check : https://fr.wikipedia.org/wiki/Produit_vectoriel#Comme_produit_de_Lie

param1 : vector to transform

out1 : matrice 3x3 composée des coordonées du vecteur (check le return poir la compo )
'''
def vector2matrix (v):
    v = v[:,0]
    return np.array([ [ 0,-v[2],v[1] ],[ v[2],0,-v[0] ],[ -v[1],v[0],0 ] ])

'''
methode qui calcule la matrice fondamentale du système

param1 : matrice de projection de la camera de gauche
param2 : coordonnée monde du centre optique de la camera de droite
param3 : matrice de projection de la camera de droite

out1 : la matrice fondamentale du système

'''
def matFondamental(camLeft,centerRight,camRight):
        return np.array(vector2matrix(camLeft @ centerRight) @ camLeft @ np.linalg.pinv(camRight))

'''
methode qui retourne les lignes épipolaire sur base des points de l'autre images

param1 : F, la matrice fondamentale du système
param2 : points, les points de l'image de gauche si on veut les epilignes de droite et inversement

out :  les lignes epipolaires sur l'images souhaitée
'''
def getEpiLines(F,points):
    return F @ points
    
