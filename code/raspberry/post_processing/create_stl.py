from stl import mesh
import numpy as np
import json
import math


    
def create_stl(data, columns, rows):
    """
    Function to transform an array of xyz points vertices and faces.\n
    Parameters : columns corresponds to the number of slices the scanner did
    or the number of steps\n
    Returns : (vertices, faces), both are arrays    
    """
    # create vertices (or points)
    # with open('code/raspberry/post_processing/sablier.json') as json_file:
    #     data = json.load(json_file)
    vertices = data

    # number of points per collumn
    lines = rows
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


def add_missing_points(points):
    """
    Function to add_missing_points.\n
    Parameters : 3D array of points\n
    Returns : (vertices, columns, rows)
    """
    
    # get the max number of points per column (best resolution)
    max_rows = 0
    for col in points:
        size = len(col)
        max_rows = max(size,max_rows)

    # add missing points by approximating
    new_points = []
    a = 0
    for col in points:

        # add extreme missing points
        if (len(col) < max_rows):
            if a == 0:
                bottom_mean = np.add(points[-1][0],points[a+1][0]) /2
                top_mean = np.add(points[-1][-1],points[a+1][-1]) /2
            elif a == len(col) -1:
                bottom_mean = np.add(points[a-1][0],points[-1][0]) /2
                top_mean = np.add(points[a-1][-1],points[-1][-1]) /2
            else:
                bottom_mean = np.add(points[a-1][0],points[a+1][0]) /2
                top_mean = np.add(points[a-1][-1],points[a+1][-1]) /2

            if (abs(bottom_mean[2] - col[0][2]) > col[0][2]*0.1):
                col =  [[col[0][0],col[0][1],bottom_mean[2]]] + col
                # col = col[:index] + [bottom_mean]
                # print([bottom_mean] + col[:index])
            if (abs(top_mean[2] - col[-1][2])> col[-1][2]*0.1):            
                col = col[:-1] + [[col[-1][0],col[-1][1],top_mean[2]]]
        
        # calculate step 
        column = np.array(col)
        highest = column[column.argmax(axis=0)[2]][2]
        smallest = column[column.argmin(axis=0)[2]][2]
        height = highest - smallest + 1
        discrete_height = height / max_rows
        step = smallest + discrete_height
        index = 0

        # middle points
        while (len(col) < max_rows):
            oui = [i for i, e in enumerate(col) if (e[2] - col[i - 1][2]) > step ]
            index = oui[0]            

            mean_x = (col[index - 1][0] + col[index][0])/2
            mean_y = (col[index - 1][1] + col[index][1])/2
            # print(step * index)
            
            # add new points in column
            if index == len(col):
                col = col[:index] + [[mean_x,mean_y,step * index]]                
            else:
                col = col[:index] + [[mean_x,mean_y,step * index]] + col[index:]

        new_points.append(col)
        a += 1
        # print(col, "\n")
            
    vertices = np.array(new_points)
    shape = np.shape(vertices)

    vertices = vertices.reshape(shape[0]*shape[1],shape[2])
    columns = shape[0]
    rows = shape[1]
    return vertices, columns, rows


def create_mesh(vertices, faces, folderName):
    """
    Function to transform vertices and faces into a 3D mesh.\n
    Output : creates a 3D stl file from the mesh.
    """
    new_stl = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            new_stl.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "new_stl.stl"
    # new_stl.save('code/raspberry/post_processing/newdzadz_stl.stl')
    name = f'{folderName}_by_SID.stl'
    new_stl.save(f'scans/{folderName}/{name}')
    print(f"mesh {name} created!")

# do

def run(folderName):
    with open(f'scans/{folderName}/NUAAAGE.json') as json_file:
        data = json.load(json_file)


    points, columns, rows = add_missing_points(data)
    vertices, faces = create_stl(points, columns, rows)
    create_mesh(vertices, faces, folderName)
    
