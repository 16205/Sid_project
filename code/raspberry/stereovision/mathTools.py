from mathutils import Vector

def pixelBelong2Epiline(coefs,pixel):
    a, b, c = coefs
    x, y, z = pixel
    if y==int(-(c+a*x)/b):
        return True
    else : 
        return False

def arrayToVector(p):
    return Vector((p[0],p[1],p[2]))