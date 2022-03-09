import os
import time
scan_name = "test_code"
name_picture_r = "nikmouk"
print(type(scan_name))
print(type(name_picture_r))
os.system('python3 prise_image_bon.py '+scan_name+' '+name_picture_r)
time.sleep(10)
