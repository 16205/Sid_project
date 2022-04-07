import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.mplot3d import axes3d
import json
import math

def create_sphere():
    x = []
    y = []
    z = []
    for i in range(2000):
        u = np.random.normal(0,1)
        v = np.random.normal(0,1)
        w = np.random.normal(0,1)
        norm = (u*u + v*v + w*w)**(0.5)
        xi,yi,zi = u/norm,v/norm,w/norm
        x.append(xi)
        y.append(yi)
        z.append(zi)

    
    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])
    
    # create file
    with open('code/raspberry/post_processing/json_data.json', 'w') as outfile:
        json.dump(coords, outfile)



def create_cube():
    x = [0,0,2,2,2,2,0,0]
    y = [0,0,0,0,2,2,2,2]
    z = [0,2,0,2,0,2,0,2]

    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])
    
    # create file
    with open('code/raspberry/post_processing/json_cube.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z

# x,y,z = create_cube()

def create_cylinder(columns=3):
    x = []
    y = []
    z = []

    angle = 360/columns

    for i in range(columns):
        alpha = math.radians(angle * i)
        for j in range(3):
        
            x.append(math.cos(alpha))
            y.append(math.sin(alpha))
            z.append(j)
    
    coords = []
    for i in range(len(x)):
        coords.append([x[i],y[i],z[i]])

    with open('code/raspberry/post_processing/cylinder.json', 'w') as outfile:
        json.dump(coords, outfile)

    return x,y,z
x,y,z = create_cylinder(12)

# plot

# fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d'})
# #ax.plot_wireframe(x, y, z, color='k', rstride=1, cstride=1)
# ax.scatter(x, y, z, s=100, c='r', zorder=10)
# ax.set_title('Example of a uniformly sampled sphere', fontdict={'fontsize':20})
# plt.show()