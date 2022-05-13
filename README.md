# **SID Project**

#### A Robotic project - Stereo Imaging Device  


## Project participants  

- Nicolas SAMELSON 17288
- Raphaël JADIN 21295
- Gabriel LOHEST 16205

## Introduction

The goal of this project was to design a 3D scanner, develop an interface and scripts to output the scanned object into a 3D STL file, ready to import into a 3D CAD design software.  

This project is still in a phase of a prototype and therefore not a finnished product.  
All the files for the interface, the script, the PCB and the 3D CAD designs were developped in an "Open-Box" extensibility model. The ```main``` branch contains the code, the ```pcb``` branch contains the PCB design files and the ```3D CAD``` branch contains the models to print.  

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

### 2.2. RunScreen

## 3. Scripts

### 3.1. On the Raspberry pi Master

### 3.2. On the Raspberry pi Slave

## 4. PCB design

## 5. 3D CAD design

## 6. Assembly

## 7. Continue the project


