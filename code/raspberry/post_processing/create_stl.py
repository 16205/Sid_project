from stl import mesh
import numpy as np
import json

"""
https://stackoverflow.com/questions/60066405/create-a-stl-file-from-a-collection-of-points
https://www.google.com/search?q=create+stl+file+from+3D+points&client=firefox-b-d&sxsrf=APq-WBtNJQR-aHtoFrPQ1u-YXHlYW6KtoA%3A1648658438709&ei=BohEYtfhKpr-sAfSo7vYCA&ved=0ahUKEwjX_OCko-72AhUaP-wKHdLRDosQ4dUDCA0&uact=5&oq=create+stl+file+from+3D+points&gs_lcp=Cgdnd3Mtd2l6EAM6BwgAEEcQsANKBAhBGABKBAhGGABQ0w1YlBhg6hpoAnABeACAAVKIAakCkgEBNJgBAKABAcgBCMABAQ&sclient=gws-wiz


STEPS : 
    - import xyz points
    - set number of columns
    - create triangles 
        - side : 2 triangles for 2 lines and 2 columns
        - top & bottom : (number of columns - 2) triangles
    - create mesh
    - tadaaaaaaaa
"""

def create_stl(columns):
    # create vertices (or points)
    with open('code/raspberry/post_processing/cylinder.json') as json_file:
        data = json.load(json_file)
    vertices = np.array(data)

    # number of points per collumn
    lines = (int)(len(data)/columns)
    
    # create triangles
    triangles = []
    for i in range(columns):
        k = 0
        # if last column, connect to the first one
        if i == columns -1: 
            k = len(data)
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

    # top and bottom triangles
    for i in range(columns-2):
        top = lines - 1
        # top triangle ex [2,5,8] (if 3 lines)
        triangles.append([top, i * lines + top + lines, i * lines + top + 2 * lines])
        # bottom triangle ex [0,6,3]
        triangles.append([0, i * lines + 2 * lines, i * lines + lines])

    # transform to numpy array
    faces = np.array(triangles)
    
    return vertices, faces



def create_mesh(vertices, faces):
    new_stl = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            new_stl.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "new_stl.stl"
    new_stl.save('code/raspberry/post_processing/new_stl.stl')

# do
vertices, faces = create_stl(12)
create_mesh(vertices, faces)