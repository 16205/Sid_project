import os
import shutil


def copy_slave_pics(scan_folder):
    # os.system(f'mkdir /home/pi/Sid_project/scans/{scan_folder}/scanLeft') 
    source_folder = f"/mnt/home/pi/scans/{scan_folder}/"
    dest_folder = f"/home/pi/Sid_project/scans/{scan_folder}/scanLeft"

    # copy folder name
    shutil.copytree(source_folder, dest_folder)
