import json
from operator import length_hint
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
import cv2 as cv
import subprocess
import numpy as np

from functools import partial
from raspberry.stereovision.calibration import calibration
import raspberry.client

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)
        self.isMasterCamOn = False
        self.isSlaveCamOn = False
        self.FFMPEG_BIN = '/usr/bin/ffmpeg'

        # _____________the whole page_____________
        pageGrid = BoxLayout(orientation= 'vertical')

        # widget grid
        widgetsLayout = AnchorLayout(anchor_x='center', anchor_y='top',size_hint= (1, 0.80))
        widgetsLayout.add_widget(self.addPageWidgets())


        # Grid of bottom buttons
        bottomLayout = AnchorLayout(anchor_x='left', anchor_y='bottom',padding=[10, 10, 10, 10],size_hint= (0.4, 0.20))
        backBtn = Button(text='Back',font_size=24, background_color=self.BUTTON_COLOR)
        backBtn.bind(on_press=self.callback)
        bottomLayout.add_widget(backBtn)
        
        
        # add widgets
        pageGrid.add_widget(widgetsLayout)
        pageGrid.add_widget(bottomLayout)
        self.add_widget(pageGrid)


    def addPageWidgets(self):
        """adds the widgets for the page"""

        widgetsBox = BoxLayout(orientation="vertical")

        # cameras

        camsGrid = GridLayout(cols=2,size_hint=(1,0.5))
        self.img1 = Image(source='res/not_found.png') # master
        self.img2 = Image(source='res/not_found.png') # slave

        camsGrid.add_widget(self.img1)
        camsGrid.add_widget(self.img2)
        widgetsBox.add_widget(camsGrid)

        # labels on the left column
        connectLabel = Label(text="Connect slave raspberry to Master",size_hint_y=None, height=self.winSize[1]/10)
        camerasLabel = Label(text="Test the cameras",size_hint_y=None, height=self.winSize[1]/5)

        # buttons on the right column
        buttonsName = ["Connect", "Master (L)", "Slave (R)", "Capture/Calibrate"]
        buttons = []
        for i in range (len(buttonsName)):
            btn = Button(text=buttonsName[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            buttons.append(btn)

        # connection widgets
        widgetsGrid = GridLayout(cols=2,size_hint=(1,0.5))
        # spacing=(self.winSize[0]/50,self.winSize[1]/50),
        #                         padding = (self.winSize[0]/50,self.winSize[1]/50))
        widgetsGrid.add_widget(connectLabel)
        widgetsGrid.add_widget(buttons[0])

        # calibration
        widgetsGrid.add_widget(camerasLabel)

        calibBox= BoxLayout(orientation= 'vertical')
        camGrid= GridLayout(cols=2)
        camGrid.add_widget(buttons[1])
        camGrid.add_widget(buttons[2])
        calibBox.add_widget(camGrid)
        calibBox.add_widget(buttons[3])

        # add to the widget box
        widgetsGrid.add_widget(calibBox)
        widgetsBox.add_widget(widgetsGrid)

        return widgetsBox



    def update_cam(self,dt,which="Master"):
        if which=="Slave":
            frame = self.captureSlave
        else:
            ret, frame = self.captureMaster.read()

        # convert it to texture
        buf1 = cv.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 

        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # display image from the texture
        if which == "Slave":
            self.img2.texture = texture1
        else:
            self.img1.texture = texture1


    def callback(self, instance):        
        name = instance.text

        def turnCamOff(which="Master"):
            if which=="Slave":
                try:
                    Clock.unschedule(self.camEventSlave)
                    self.captureSlave.release()
                    self.isSlaveCamOn = False
                except:
                    print("error with Slave camera")
            else:
                try:
                    Clock.unschedule(self.camEventMaster)
                    self.captureMaster.release()
                    self.isMasterCamOn = False
                except:
                    print("error with Master camera")

        def run_ffmpeg():
            ffmpg_cmd = [
                self.FFMPEG_BIN,
                '-i', 'tcp://pislave:5000/',
                '-video_size', '1296x972',
                '-pix_fmt', 'bgr24',        # opencv requires bgr24 pixel format
                '-vcodec', 'rawvideo',
                '-an','-sn',                # disable audio processing
                '-f', 'image2pipe',
                '-',                        # output to go to stdout
            ]
            return subprocess.Popen(ffmpg_cmd, stdout = subprocess.PIPE, bufsize=10**8)

        def run_cv_window(process,dt):
            # while True:
                 # read frame-by-frame
            raw_image = process.stdout.read(1296*972*3)
            if raw_image == b'':
                raise RuntimeError("Empty pipe")
            
            # transform the bytes read into a numpy array
            frame =  np.frombuffer(raw_image, dtype='uint8')
            frame = frame.reshape((972,1296,3)) # height, width, channels
            if frame is not None:
                self.captureSlave = frame
                self.update_cam(0,which="Slave")
                
            #     cv.imshow('Video', frame)
            
            if self.isSlaveCamOn == False:
                process.stdout.flush()
                
                cv.destroyAllWindows()
                process.terminate()
                print(process.poll())

        def turnCamOn(which):
            if which== "Slave":
                try:
                    self.isSlaveCamOn = True  
                    ffmpeg_process = run_ffmpeg()
                    self.camEventSlave = Clock.schedule_interval(partial(run_cv_window,ffmpeg_process),1/33.0)

                except:
                    print("Slave cam is not connected")
            else:
                try:                
                    self.captureMaster = cv.VideoCapture(0)
                    self.camEventMaster = Clock.schedule_interval(partial(self.update_cam,which="Master"),1/33.0)
                    self.isMasterCamOn = True  
                except:
                    print("Master cam is not connected")
            
                

        def calibrate():
            try:
                mtx, dist, rvecs, tvecs = calibration()
                calib = {
                    "mtx": mtx,
                    "dist": dist,
                    "rvecs": rvecs,
                    "tvecs": tvecs
                }
                with open('code/raspberry/stereovision/calibration_params.json', 'w') as outfile:
                    json.dump(calib, outfile)
            except:
                print("Error in calibration")

        # names of the buttons
        if name == "Back":
            turnCamOff("Slave")
            turnCamOff("Master")
            self.manager.current = "Home"

        elif name == "Connect":
            print('Connecting slave to master')
        elif name == "Master (L)":
            if self.isMasterCamOn:
                turnCamOff("Master")
            else:
                turnCamOn("Master")     
            print("master cam : L")
        elif name == "Slave (R)":
            if self.isSlaveCamOn:
                turnCamOff("Slave")
            else:
                turnCamOn("Slave")     
            print("slave cam : R")
        elif name == "Capture/Calibrate":            
            print("capturing")
            calibrate()            
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))