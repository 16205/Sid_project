import numpy as np
import json
import math

"""
File to create dummy json files with xyz points in an array
"""

def create_sablier():
    x = [0,0,1,1,       2,2,2,2, 1,1,0,0]
    y = [0,0,1,1,       0,0,2,2, 1,1,2,2]
    z = [0,2,0,2,       0,2,0,2, 0,2,0,2]

    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])
    
    # create file
    with open('code/raspberry/post_processing/sablier.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z
# create_sablier()

def create_sphere(columns=42, rows = 8):
    x = []
    y = []
    z = []

    colAngle = 360/columns
    rowAngle = 180/rows
    semirows = int(rows/2)

    for i in range(columns):
        alpha = math.radians(colAngle * i)
        for j in range(-semirows,semirows):
            beta = math.radians(rowAngle * j)
        
            x.append(math.cos(alpha)* math.cos(beta))
            y.append(math.sin(alpha)* math.cos(beta))
            z.append(math.sin(beta))
    
    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])

    with open('code/raspberry/post_processing/sphere.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z

# create_sphere(42,12)


def create_cube():
    x = [0,0,2,2,2,2,0,0]
    y = [0,0,0,0,2,2,2,2]
    z = [0,2,0,2,0,2,0,2]

    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])
    
    # create file
    with open('code/raspberry/post_processing/cube.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z

# x,y,z = create_cube()

def create_cylinder(columns=3, rows = 3):
    x = []
    y = []
    z = []

    angle = 360/columns

    for i in range(columns):
        alpha = math.radians(angle * i)

        for j in range(rows):        
            x.append(math.cos(alpha))
            y.append(math.sin(alpha))
            z.append(j)
    
    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])

    with open('code/raspberry/post_processing/cylinder.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z
# x,y,z = create_cylinder(42,4)

def create_cylinder_with_missing_points(columns=8, rows = 7):
    x = []
    y = []
    z = []

    angle = 360/columns
    coords = []

    for i in range(columns):
        alpha = math.radians(angle * i)

        column = []
        for j in range(rows): 
            xi = math.cos(alpha)
            yi = math.sin(alpha)
            zi = j

            column.append([xi,yi,zi])

        coords.append(column)


    with open('code/raspberry/post_processing/new_cylinder.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z

create_cylinder_with_missing_points()