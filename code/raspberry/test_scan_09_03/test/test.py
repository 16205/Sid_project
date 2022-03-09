import cv2 


path = r"C:\Users\rapha\OneDrive\Documents\master1\Q2\projetRobotique\Sid_project\code\raspberry\test_scan_09_03\test\test_scan_09_03_L_2_complet.jpg"
img = cv2.imread(path)
blue, green, red = cv2.split(img)
hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
h, s, v = cv2.split(hsv)
ret,thresh1 = cv2.threshold(green,200,255,cv2.THRESH_BINARY)
while True:
    cv2.imshow('img',img)
    cv2.imshow('red',red)
    cv2.imshow('blue',blue)
    cv2.imshow('green',green)
    cv2.imshow('gray',gray)
    cv2.imshow('tresh',thresh1)
    # cv2.imshow('h',h)
    # cv2.imshow('s',s)
    # cv2.imshow('v',v)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()