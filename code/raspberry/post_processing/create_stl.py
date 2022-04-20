from stl import mesh
import numpy as np
import json

def create_stl(columns):
    """
    Function to transform an array of xyz points vertices and faces.\n
    Parameters : columns corresponds to the number of slices the scanner did
    or the number of steps\n
    Returns : (vertices, faces), both are arrays    
    """
    # create vertices (or points)
    with open('code/raspberry/post_processing/sablier.json') as json_file:
        data = json.load(json_file)
    vertices = np.array(data)

    # number of points per collumn
    lines = (int)(len(data)/columns)

    top = lines - 1

    # get the sum of the top and bottom points coordinates to then get the mean
    top_points_sum = [0,0,0]
    bottom_points_sum = [0,0,0]

    # create triangles
    triangles = []
    for i in range(columns):
        k = 0
        # if last column, connect to the first one
        if i == columns -1: 
            k = len(data)
        # take the top and bottom points of each column and add it
        top_points_sum = np.add(top_points_sum, vertices[i*lines + top])
        bottom_points_sum = np.add(bottom_points_sum, vertices[i*lines])
       
        # triangles must be constructed clock-wise from an outside point of view
        for j in range(lines-1):
            # first triangle ex [0,3,1] (if 3 lines)
            triangles.append([
                i * lines + j, 
                i * lines + j + lines - k, 
                i * lines + j + 1])
            # second triange ex [1,3,4]
            triangles.append([
                i * lines + j + 1, 
                i * lines + j + lines - k, 
                i * lines + j + lines + 1 - k])

    # create the mean point coordinates
    mean_top_point = np.array((list) (map(lambda p: p/columns, top_points_sum)))
    mean_bottom_point = np.array((list) (map(lambda p: p/columns, bottom_points_sum)))

    vertices = np.vstack((vertices,mean_top_point))
    vertices = np.vstack((vertices,mean_bottom_point))
    
    # top and bottom triangles
    for i in range(columns):

        if (i != columns - 1):
            # bottom triangles
            triangles.append([i*lines + lines, i*lines,len(vertices)-1])
            # top triangles
            triangles.append([i*lines + top, i * lines + lines + top, len(vertices)-2])
        else:
            # bottom
            triangles.append([0,i*lines, len(vertices)-1])
            #top
            triangles.append([i * lines + top, top,len(vertices)-2])

    # transform to numpy array
    faces = np.array(triangles)

    # print(vertices)
    minmax = [0,0]
    for i in range(len(vertices)):
        if np.amax(vertices[i]) > np.amax(vertices[minmax[1]]):
            minmax[1] = i
        if np.amin(vertices[i]) < np.amin(vertices[minmax[0]]):
            minmax[0] = i
    
    
    return vertices, faces



def create_mesh(vertices, faces):
    """
    Function to transform vertices and faces into a 3D mesh.\n
    Output : creates a 3D stl file from the mesh.
    """
    new_stl = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            new_stl.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "new_stl.stl"
    new_stl.save('code/raspberry/post_processing/new_stl.stl')

# do
vertices, faces = create_stl(6)
create_mesh(vertices, faces)
