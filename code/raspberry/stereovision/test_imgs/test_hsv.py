import cv2 


path = r"C:\Users\rapha\OneDrive\Documents\master1\Q2\projetRobotique\Sid_project\code\raspberry\stereovision\test_imgs\airpods_test_bis_complet.jpg"
img = cv2.imread(path)
hsv =cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
while True:
    cv2.imshow('img',img)
    cv2.imshow('hsv',hsv)
    cv2.imshow('h',h)
    cv2.imshow('s',s)
    cv2.imshow('v',v)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cv2.destroyAllWindows()