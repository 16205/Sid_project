import cv2
import numpy as np
import matplotlib as plt

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
    
'''
returns epilines (on right camera image) for all red points of the red line (of the left camera), from all images
'''
def findEpilines(path):
    epilines = []
    
    for l in range(26):
        #correct format to match file name
        if l<10:
            strp = path + '000' + str(l) +'.png'
        else:
            strp = path + '00' + str(l) +'.png'
            
        #get the red mask    
        red = getRed(strp)
        tempEpilines = []
        pointsLeft = [[],[],[]]
        
        #i is the number of the line
        for i, line in enumerate(red):
            for pixel in line:
                if pixel != 0:
                    pixel = 1
            try:
                #weighted average => (0*0 + 1*0 + 2*0 + ... + 1248 * 1 + 1249 * 0) / n° of red pixels
                #for instance => (1261+1262+1267)/3 = 1263.33
                #give position of the red line in x axis
                pointsLeft[0].append(np.average(range(1920), weights = line))
                pointsLeft[1].append(i) # y axis
                pointsLeft[2].append(1)
            except:
                pass
        #from red line on left image, find corresponding epiline on right image
        epilinesRight = getEpiLines(Fondamental, pointsLeft)
        tempEpilines.append(pointsLeft)
        tempEpilines.append(epilinesRight)
        epilines.append(tempEpilines)
    return epilines


Fondamental = matFondamental(camRight,camWorldCenterLeft,camLeft)
# epl = [ [ [Red_x_avg], [Y_avg], [1] ], [EpilineRight(i)] ] ]
epl = findEpilines('scanRight/')
print("ok")

def drawAvgPoint(fname,EplLeft):
    img = cv2.imread(fname)
    i = 0
    while i< len(EplLeft[0]):
        color = tuple(np.random.randint(0,255,3).tolist())
        img = cv2.circle(img,(int(EplLeft[0][i]),int(EplLeft[1][i])),5,color,-1)
        i += 10
    plt.imshow(img)
    plt.show()

'''equation of a ligne => returns a value for y for a given x and coefficients'''
def lineY(coefs,x):
    a,b,c = coefs
    return-(c+a*x)/b


def drawEpl(fname,EplRight):
    img = cv2.imread(fname)
    coef , length = EplRight.shape
    for i in range(0,length,40):
        #print a, b and c of epiline
        print(EplRight[:,i])
        plt.plot([0,1919],[lineY(EplRight[:,i],0),lineY(EplRight[:,i],1919)],'g')
        
    plt.imshow(img)
    plt.show()

drawAvgPoint('scanRight/0010.png',epl[10][0])
drawEpl('scanLeft/scan0010.png',epl[10][1])
print("done done ok ok")

'''Get x position of the red point of each line of pixels (only one point per line, hence the average position)'''
def getRedAvg(fname):
    red = getRed(fname)
    redPoints = [[],[],[]]

    for i, line in enumerate(red):
        for pixel in line:
            if pixel != 0:
                pixel = 1
        try:
            #same as in find epilines
            redPoints[0].append(np.average(range(1920), weights = line))
            redPoints[1].append(i)
            redPoints[2].append(1)
        except:
            pass
    return redPoints

'''Find red points that are on an epiline, for each picture'''
def eplRedPoints(path,EplRight):
    points = []
    for l in range(26):
        if l<10:
            strp = path + '000' + str(l) +'.png'
        else:
            strp = path + '00' + str(l) +'.png'
            
        redPoints = getRedAvg(strp)
        scan = cv2.imread(strp)

        pointsRight = [[],[],[]]
        eplImg = EplRight[l][1] #keep only epiline and not red points (EplRight[l][0])
        print(strp)
        for i in range(len(eplImg[0])):
            try : 
                x = int(redPoints[0][i]) #average position
                y = int(lineY(eplImg[:,i],x)) #use of y = (-ax+c)/b to find y position
                pointsRight[0].append(x)
                pointsRight[1].append(y)
                pointsRight[2].append(1)
                
                #color = tuple(np.random.randint(0,255,3).tolist())
                #scan = cv.circle(scan,(x,y),5,color,-1)
            except:
                pass
        points.append(pointsRight)
        # plt.imshow(scan)
        # plt.show()
    return points


pointsRight = eplRedPoints('scanRight/scan',epl)
print("done")

def arrayToVector(p):
    return Vector((p[0],p[1],p[2]))


def getIntersection(pointsLeft,pointsRight):
    
    pL = np.array(pointsLeft)
    pR = np.array(pointsRight)
    
    camCenterRight = np.transpose(camWorldCenterRight)[0]
    camCenterLeft = np.transpose(camWorldCenterLeft)[0]
    
    # get world/object 3D coordinates of all points 
    
    leftObject = (np.linalg.pinv(camLeft) @ pL)
    rightObject = (np.linalg.pinv(camRight) @ pR) 
    
    # characteristics points of retro projected lines
    
    leftEndVec = arrayToVector(leftObject)
    rightEndVec = arrayToVector(rightObject)
    
    leftStartVec = arrayToVector(camCenterLeft)
    rightStartVec = arrayToVector(camCenterRight)
    
    # display retro projected lines
    
    '''
    draw3DLine(camCenterLeft,leftObject)
    draw3DLine(camCenterRight,rightObject)
    plt.show()
    '''    
    
    # intersection between two retroprojected lines = real world point
    return pygeo.intersect_line_line(leftStartVec,leftEndVec,rightStartVec,rightEndVec)


def draw3DLine(start,end):
    figure = plt.figure()
    ax = Axes3D(figure)
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    
    x_start,y_start,z_start = start
    x_end,y_end,z_end = end

    print("start = ({},{},{})".format(x_start,y_start,z_start))
    print("end = ({},{},{})\n".format(x_end,y_end,z_end))

    ax.scatter(x_start,y_start,z_start,c='r',marker='o')
    ax.plot([x_start ,x_end],[y_start,y_end],[z_start,z_end])


def getObjectPoint():
    point = [[],[],[]]
    for l in range(26):
        pointsLeft = np.array(epl[l][0])
        
        pointRight = np.array(pointsRight[l])
        for i in range(len(pointsLeft[0])):
            try:
                
                # calcul du point d'intersection sur l'objet -> on obtient une liste de vector
                intersection = getIntersection(pointsLeft[:,i],pointRight[:,i])
                # print(intersection)
                for inter in intersection:
                    inter *= 1000
                    x,y,z = inter
                    point[0].append(x)
                    point[1].append(y)
                    point[2].append(z)
            except:
                pass
    return np.array(point)
        

def drawPointObject(points):
    figure = plt.figure()
    ax = Axes3D(figure)
    
    ax.scatter3D(points[0,:],points[1,:],points[2,:],c='black',marker='.')     
        
    ax.view_init(-105,-75)
    plt.axis('off')
    plt.show()
    

def drawSurfaceObject(points):
    figure = plt.figure()
    ax = Axes3D(figure)
    ax.plot_trisurf(points[0,:],points[1,:],points[2,:])     

    ax.view_init(-289,-80)
    plt.axis('off')
    plt.show()
    
    
def pointToJson(point):
    data = {'x':point[0,:].tolist(),'y':point[1,:].tolist(),'z':point[2,:].tolist()}
    with open('point.txt','+w') as file:
        json.dump(data,file)


point = getObjectPoint()
drawSurfaceObject(point)
drawPointObject(point)
pointToJson(point)
print("done again again")