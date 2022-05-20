from sys import setprofile
from tempfile import tempdir
import numpy as np
import jsonTools as js
import os 
import math
import matplotlib.pyplot as plt

def pre_revolution(scan_name):
    calib = js.getJsonData("calibration\calibration_params.json")
    camWorldCenterLeft, camWorldCenterRight = np.array(calib.get("camWorldCenterLeft")), np.array(calib.get("camWorldCenterRight"))
    #on recup le nuage de points depuis le json
    point_cloud = js.getJsonData(scan_name+"/world_coordinates(xyz).json")
    length = len(os.listdir(scan_name + "/scanLeft"))
    # ratio = (camWorldCenterLeft[0][2]-camWorldCenterRight[0][2])/20
    adjusted_points = {"scan" : {"scan name " : scan_name}}
    for i in range(length-1):
        points = point_cloud.get(str(i))
        print(type(points))
        temp_points = []
        for l in range(len(points)):
            points[l] = [points[l][0]-6.7, points[l][1]+2.25, points[l][2]-9.25 - 1.5]
            temp_points.append(points[l])
        adjusted_points.update({str(i):temp_points})
    js.buildJson(scan_name,'adjusted_world_coordinates',adjusted_points)
    return adjusted_points

def revolution(scan_name, adjusted_points):
    length = len(os.listdir(scan_name + "/scanLeft"))
    les_points_insoumis = {"scan" : {"scan name " : scan_name}}
    step_angle = 360/(length+1)
    for i in range(length-1):
        print(i)
        alpha = i*step_angle
        points = adjusted_points.get(str(i))
        temp_points = []
        for l in range(len(points)):
            points[l] = [points[l][2]*math.sin(alpha), points[l][1], points[l][2]*math.cos(alpha)]
            temp_points.append(points[l])
        les_points_insoumis.update({str(i):temp_points})
    js.buildJson(scan_name,"NUAAAAAAAAAAAAAAGE", les_points_insoumis)
    return les_points_insoumis

guillotinés = pre_revolution("test")
print("ok")
les_insoumis = revolution("test", guillotinés)
print("ok")

def plotDotWorld(scan_name, les_insoumis):

    x, y, z = [], [], []
    length = len(os.listdir(scan_name + "/scanLeft"))
    for i in range(length-1):
        points = les_insoumis.get(str(i))
        for l in range(len(points)):
            x.append(points[l][0])
            y.append(points[l][1])
            z.append(points[l][2])
    fig = plt.figure()
    ax = plt.axes(projection='3d')
        
    ax.scatter(x, y, z, c='r', marker='o')
    
    ax.scatter(0,0,0, c='b', marker = '*')
    ax.set_xlabel('$X$', fontsize=20, rotation=150)
    ax.set_ylabel('$Y$')
    ax.set_zlabel('$z$', fontsize=30, rotation=60)
    
    plt.show()

plotDotWorld("test", les_insoumis)