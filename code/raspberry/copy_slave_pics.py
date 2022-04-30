import os
import shutil


def copy_slave_pics(scan_folder):
    source_folder = f"/mnt/home/pi/scans/{scan_folder}/"
    dest_folder = "/home/pi/Sid_project/scans/{scan_folder}/"

    # copy folder name
    shutil.copytree(source_folder, dest_folder)

    # copy files in the folder
    for file_name in os.listdir(source_folder):
        source = source_folder + file_name
        dest = dest_folder + file_name
        
        try:
            if os.path.isfile(source):
                shutil.copy(source, dest)
                print('copied', file_name)
        except os.error as e:
            print(str(e))
