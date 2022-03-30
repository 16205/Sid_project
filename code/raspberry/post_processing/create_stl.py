from pickletools import int4
from stl import mesh
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import json

"""
https://stackoverflow.com/questions/60066405/create-a-stl-file-from-a-collection-of-points
https://www.google.com/search?q=create+stl+file+from+3D+points&client=firefox-b-d&sxsrf=APq-WBtNJQR-aHtoFrPQ1u-YXHlYW6KtoA%3A1648658438709&ei=BohEYtfhKpr-sAfSo7vYCA&ved=0ahUKEwjX_OCko-72AhUaP-wKHdLRDosQ4dUDCA0&uact=5&oq=create+stl+file+from+3D+points&gs_lcp=Cgdnd3Mtd2l6EAM6BwgAEEcQsANKBAhBGABKBAhGGABQ0w1YlBhg6hpoAnABeACAAVKIAakCkgEBNJgBAKABAcgBCMABAQ&sclient=gws-wiz

other idea:
        - create XYZ file from 3D coordinates
        - then convert to stl file

STEPS : v get xyz coordinates
        v put it in an array of points with dtype mesh
        - /!\ COORDINATES MUST BE POSITIVE
        - create a mesh
        - generate normals
        - create triangles
        - generate stl file
        - voila
"""

with open('code/raspberry/post_processing/json_data.json') as json_file:
    data = json.load(json_file)


points = np.array(data, dtype=mesh.Mesh.dtype)

#TODO: faire en sorte que tous les points soient positifs (1er quadrant)

# test = np.zeros(100, dtype=mesh.Mesh.dtype)
# print(points)
your_mesh = mesh.Mesh(points, remove_empty_areas=False)

# The mesh normals (calculated automatically)
your_mesh.normals
# The mesh vectors
your_mesh.v0, your_mesh.v1, your_mesh.v2
# Accessing individual points (concatenation of v0, v1 and v2 in triplets)

# print(your_mesh.points[0][0:3])
# assert (your_mesh.points[0][0:3] == your_mesh.v0[0]).all()
# assert (your_mesh.points[0][3:6] == your_mesh.v1[0]).all()
# assert (your_mesh.points[0][6:9] == your_mesh.v2[0]).all()
# assert (your_mesh.points[1][0:3] == your_mesh.v0[1]).all()


your_mesh.save('code/raspberry/post_processing/new_stl_file.stl')


# from mpl_toolkits import mplot3d
# from matplotlib import pyplot

# # Create a new plot
# figure = pyplot.figure()
# axes = mplot3d.Axes3D(figure)

# # Load the STL files and add the vectors to the plot
# your_mesh = mesh.Mesh.from_file('code/raspberry/post_processing/new_stl_file.stl')
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# # Auto scale to the mesh size
# scale = your_mesh.points.flatten()
# axes.auto_scale_xyz(scale, scale, scale)

# # Show the plot to the screen
# pyplot.show()