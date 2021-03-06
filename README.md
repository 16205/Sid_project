# **SID Project**

#### A Robotic project - Stereo Imaging Device  
![alt text](https://github.com/16205/Sid_project/blob/main/res/sid_front.jpg)

## Project participants  

- Nicolas SAMELSON 17288
- Raphaël JADIN 21295
- Gabriel LOHEST 16205

## Introduction

The goal of this project was to design a 3D scanner, develop an interface and scripts to output the scanned object into a 3D STL file, ready to import into a 3D CAD design software.  

This project is still in a phase of a prototype and therefore not a finnished product.  
All the files for the interface, the script, the PCB and the 3D CAD designs were developped in an "Open-Box" extensibility model. The ```main``` branch contains the code, the ```pcb``` branch contains the PCB design files and the ```3D-printed-hardware-CAD``` branch contains the models to print.  

## 1. Material used

- 2 Raspberry pi 4
- 2 Raspberry pi camera (module V2.1)
- 1 Stepper motor (Nema 17 10:1)
- 1 driver (A4988)
- 1 Power supply AC/DC 5V and 12V
- 1 display 11"
- 1 red line laser (HLM1230)


## 2. Interface (Kivy)

The interface files are stored inside the folder [/code/screen/](https://github.com/16205/Sid_project/tree/main/code/screens). 
Inside, there are 4 files, each for a specific screen interface.  

### 2.1. HomePageScreen
This corresponds to the home page of the interface. The user is presented with 4 buttons : 
- **Run**, to access the ```RunScreen```;
- **Settings**, to access the ```SettingsScreen```;
- **Storage**, to access the ```StorageScreen```;
- **Exit**, to exit the application.

![alt text](https://github.com/16205/Sid_project/blob/main/res/HomePage.png?raw=true)
### 2.2. RunScreen
This interface contains all the quick parameters to set before a scan and the button to start a scan :
- **Resolution** is used to set the number of pictures taken;
- **Scale** is used to set the size of the object to scan;
- **Laser power** is used to adjust the intensity of the laser;
- **The set of 3 radio buttons** helps visualize the pictures taken in different color spaces.

![alt text](https://github.com/16205/Sid_project/blob/main/res/Run.png?raw=true)

### 2.3. Settings
This interface is used to setup the calibration needed to scan (only the first time the application is launched) :
- **Connect** helps setting up the video stream of the slave raspberry pi camera;
- **Slave(L)** and **Master(R)** are used to have a video feedback of the 2 cameras;
- **Capture/Calibrate** launches the script of ```calibration```.

![alt text](https://github.com/16205/Sid_project/blob/main/res/Settings.png?raw=true)

### 2.4. Storage
The storage interface helps the user to manage its scans, as well as convert it in a 3D STL file.

![alt text](https://github.com/16205/Sid_project/blob/main/res/Storage.png?raw=true)

## 3. Scripts

### 3.1. Main.py

Run the script [main.py](https://github.com/16205/Sid_project/blob/main/code/main.py) to launch the interface

### 3.2. On the Raspberry pi Master

#### 3.2.1. Different Files
In the [/code/raspberry/](https://github.com/16205/Sid_project/tree/main/code/raspberry) folder, you can find the following scripts :
- ```GPIO_setup.py``` : used to set the correct pins in read/write at the start of the application;
- ```copy_slave_pics.py``` : after a scan , the master will copy the pictures taken by the slave in its own folder;
- ```laser.py``` : used to turn on/off and adjust the intensity of the laser;
- ```prise_image_bon.py``` : takes a picture from the master and writes it into a folder with the name of the scan;
- ```scan.py``` : main script that manages the scan (turns the laser, takes pictures, turn the stepper and copy the slave pics);
- ```sshTools.py``` : used to run commands from the master to the slave via the SSH protocol;
- ```stepper.py``` : used to command the stepper and turn a determinated number of steps;
- ```stream.py``` : used to command the slave to stream its video feed through rtsp.

#### 3.2.2. Stereovision Folder
The stereovision folder contains the scripts to calibrate the cameras, but also to transform the pictures in a cloud of 3D points : 
- ```calibration.py```: calibrates the cameras;
- ```prepross.py```: generate a new binarized image with in white the laser and the rest in black
- ```image_processing.py```: contain the stereovision methods 
- ```scan_processing.py```: run the stereovision methods on a scan and then generate a JSON file with the world coordinates in the opencv calibration referential.
- ```post_processing.py```: achieve the revolution of all the laser lines and save the point cloud to a json.
- ```jsonTools.py```: Library to create json files and get data from json files
- ```mathTools.ty```: Library with mathematical functions for the image processing

#### 3.2.3. Post-processing Folder
This folder contains the scritps to transform a cloud of points into a 3D STL file : 
- ```create_stl.py``` : takes in input a json file in a 3 dimensions matrix and outputs a STL file;
- ```create_points.py``` : creates json files to get examples of working models.

### 3.3. On the Raspberry pi Slave
- ```prise_image_bon.py```: take picture and save it into the asked folder. Runned from the master in ssh.

## 4. PCB design
The [pcb](https://github.com/16205/Sid_project/tree/pcb) branch contains the Gerber files to print through JLCPCB.  
You can find the scematics and the design in the [pdf](https://github.com/16205/Sid_project/tree/pcb/pdf) folder.

The point of this PCB is to have one board, connecting all the needed cables as well as having easy access to the pins. It contains a footprint for :
- A A4988 driver;
- 2 USB-A 2.0 female ports;
- 1 capacitor (12V)
- 1 potentiometer
- pins for the stepper, the alimentation (5 and 12V), the laser and the raspberry pi (master)

## 5. Continue the project

Please Fork the repository if you want to continue our project. If you just want to test it, just clone it.

### 5.1. Dependencies

The project needs you to have a python version of ```3.8.10``` or older, with the following pip modules installed : 
- ```numpy```
- ```numpy-stl```
- ```opencv-python```
- ```mathutils```
- ```kivy```
- ```RpiMotorlib```

