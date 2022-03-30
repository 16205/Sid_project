import matplotlib.pyplot as plt
import numpy as np
import random
from mpl_toolkits.mplot3d import axes3d
import json


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

# plot

# fig, ax = plt.subplots(1, 1, subplot_kw={'projection':'3d'})
# #ax.plot_wireframe(x, y, z, color='k', rstride=1, cstride=1)
# ax.scatter(x, y, z, s=100, c='r', zorder=10)
# ax.set_title('Example of a uniformly sampled sphere', fontdict={'fontsize':20})
# plt.show()

# create file

coords = []
for i in range(len(x)):
    coords.append([x[i],y[i],z[i]])

with open('code/raspberry/post_processing/json_data.json', 'w') as outfile:
    json.dump(coords, outfile)