from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import sys
import os
import cv2 as cv
sys.path.append(os.getcwd())
from raspberry.laser import *
from raspberry.scan import *

class RunScreen(Screen):
    
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)
        self.isPaused = False
        self.isLaserOn = False
        self.isCamOn = False

        # set values from JSON TODO: create a json to save settings
        self.scale = 10
        self.laserPower = 30
        self.colorSpace = "Saturation"
        self.resolution = "Low"

        self.addWidgets()

    def update_cam(self,dt):
        ret, frame = self.capture.read()
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        b,g,r  = cv.split(frame)        
        h,s,v = cv.split(hsv)

        color = r
        if self.colorSpace == "Saturation":
            color = s
        elif self.colorSpace =="Hue":
            color = h
        else:
            color = r

        buf1 = cv.flip(color, 0)
        buf = buf1.tostring()
        self.image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='luminance')
        self.image_texture.blit_buffer(buf, colorfmt='luminance', bufferfmt='ubyte')
        # display image from the texture
        self.img1.texture = self.image_texture
    

    def addWidgets(self):
        """
        Do : adds widgets to the page 
        """
        widgetHeight = self.winSize[1]/7

        # when a checkbox value changes
        def onCheckboxActiveChange(instance,value):
            if value:
                if instance.group =="col":
                    self.colorSpace = list(instance.ids.values())[0]
                elif instance.group == "res":
                    self.resolution = list(instance.ids.values())[0]
                else:
                    print("Error getting the group")
                
        # Grid containing the parameters
        paramGrid = GridLayout(cols=2)
        self.ids['paramGrid'] = paramGrid

        # Resolution widgets : label and radiobuttons
        resolutionLabel = Label(text="Resolution",size_hint_y=None, height=widgetHeight)   
        resWidget = [Label(text="Low"),Label(text="Medium"),Label(text="High")]   
        resolutionGrid = GridLayout(cols=3,size_hint_y=None, height=widgetHeight)  

        resIndex = 0
        for i in range(6):
            if i < 3:
                resolutionGrid.add_widget(resWidget[i])
                if self.resolution == resWidget[i].text:
                    resIndex = i + 3
            else:
                check = CheckBox(group='res', allow_no_selection=False, ids={i-3:resWidget[i-3].text})
                if resIndex == i:
                    check.active = True
                check.bind(active=onCheckboxActiveChange)
                resolutionGrid.add_widget(check)

        paramGrid.add_widget(resolutionLabel)
        paramGrid.add_widget(resolutionGrid)


        # Scale widgets : label and slider
        scaleLabel = Label(text="Scale",size_hint_y=None, height=widgetHeight)
        scaleSlider = Slider(min=5, max=20, value=self.scale, step = 5,value_track=True,value_track_color=[1, 1, 0, 1])
        scaleValueLabel = Label(text=f"{self.scale}x{self.scale}x{self.scale} cm")
        

        def OnSliderValueChange(instance,value):
            """
            Do: updates the value of the scale
            """
            scaleValueLabel.text = f"{value}x{value}x{value} cm"
            self.scale = value
        
        scaleSlider.bind(value=OnSliderValueChange)

        sliderGrid = GridLayout(cols=1,size_hint_y=None, height=widgetHeight)
        sliderGrid.add_widget(scaleValueLabel)
        sliderGrid.add_widget(scaleSlider)
        paramGrid.add_widget(scaleLabel)
        paramGrid.add_widget(sliderGrid)

        # Laser power widget : label and slider
        laserLabel = Label(text="Laser power",size_hint_y=None, height=widgetHeight)
        laserSlider = Slider(min=0, max=100, value=self.laserPower, step = 1,value_track=True,value_track_color=[1, 1, 0, 1])
        laserValueLabel = Label(text=f"{int(self.laserPower)}%")
        # sets the laser a duty at the start
        #TODO: uncomment
        setDuty(50)

        def OnSliderValueChange(instance,value):
            """
            Do: updates the value of the laser
            """
            laserValueLabel.text = f"{int(value)}%"
            self.laserPower = int(value)
            #TODO: uncomment
            setDuty(int(value))
        
        laserSlider.bind(value=OnSliderValueChange)

        laserGrid = GridLayout(cols=1,size_hint_y=None, height=widgetHeight)
        laserGrid.add_widget(laserValueLabel)
        laserGrid.add_widget(laserSlider)
        paramGrid.add_widget(laserLabel)
        paramGrid.add_widget(laserGrid)

        # Image widget

        self.img1 = Image(source='res/not_found.png')
        paramGrid.add_widget(self.img1)
        # self.capture = cv.VideoCapture(0)
        

        # Radio button color space + turn laser on/off
        laserAndColorGrid = GridLayout(cols=1,padding = (self.winSize[0]/50,self.winSize[1]/50),
                            spacing=(self.winSize[0]/100,self.winSize[1]/100))
        # color space grid for radiobuttons
        colorGrid = GridLayout(cols=3,size_hint_y=None, height=widgetHeight)
        colorWidget = [Label(text="Saturation"),Label(text="Hue"),Label(text="Red")]
        colIndex = 0
        for i in range(6):
            if i < 3:
                colorGrid.add_widget(colorWidget[i])
                if self.colorSpace == colorWidget[i].text:
                    colIndex = i + 3
            else:
                check = CheckBox(group='col', allow_no_selection=False, ids={i-3:colorWidget[i-3].text})
                if i == colIndex:
                    check.active = True
                check.bind(active=onCheckboxActiveChange)
                colorGrid.add_widget(check)

        laserButton = Button(text="Turn laser",font_size=24, background_color=self.BUTTON_COLOR)
        laserButton.bind(on_press=self.callback)
        cameraButton = Button(text="Turn camera",font_size=24, background_color=self.BUTTON_COLOR)
        cameraButton.bind(on_press=self.callback)

        laserAndColorGrid.add_widget(colorGrid)
        laserAndColorGrid.add_widget(laserButton)
        laserAndColorGrid.add_widget(cameraButton)
        paramGrid.add_widget(laserAndColorGrid)

        # Grid layout: buttons in the bottom of the screen
        bottomGrid = GridLayout(rows=1,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                                spacing=(self.winSize[0]/50,self.winSize[1]/50),
                                size_hint_y=None, height=self.winSize[1]/5)
        namesList = ["Back","Save","Run"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            bottomGrid.add_widget(btn)  

        # Whole page layout
        pageGrid = GridLayout(cols=1)
        
        # Adding all the layouts to the page
        pageGrid.add_widget(paramGrid)
        pageGrid.add_widget(bottomGrid)
        self.add_widget(pageGrid)   
    
    def showRunPopup(self):
        """
        Do: popup to show the progression of the scan
        """
        # TODO: import image capture each x photos taken

        # schedule check
        # self.progress = Clock.schedule_interval(self.updateRun,1)

        # create content and add to the popup
        content = GridLayout(cols=1)

        # capture 
        try:
            scanImg = self.image_texture
        except:
            scanImg = Image(source='res/sid.jpg')
        # progress bar
        
        pb = ProgressBar(value=0, max=100,size_hint_y=None, height=self.winSize[1]/15)
        pbLabel = Label(text=f"progress = {pb.value}%",size_hint_y=None, height=self.winSize[1]/15)
        self.ids["progressBar"] = pb
        self.ids["pbLabel"] = pbLabel

        # buttons
        buttons = GridLayout(cols=4,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                            spacing=(self.winSize[0]/50,self.winSize[1]/50),
                            size_hint_y=None, height=self.winSize[1]/5)
        namesList = ["Close","Cancel","Pause","Play"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            buttons.add_widget(btn)  

        # add widgets
        content.add_widget(scanImg)
        content.add_widget(pbLabel)
        content.add_widget(pb)
        content.add_widget(buttons)

        popup = Popup(title='Run 3D scan',content=content, auto_dismiss=False)
        self.ids['runPopup'] = popup

        # open the popup
        popup.open()

    def updateRun(self, dt):
        """
        Do: updates the advancement of the scan
        """
        # TODO: import script to check advancement of pictures by counting the number of files
        if self.ids["progressBar"].value == 100:
            self.progress.cancel()
        elif self.isPaused == False:
            self.ids["progressBar"].value += 5
            self.ids["pbLabel"].text = "progress = "+ str(self.ids["progressBar"].value) + "%"
        

    def callback(self, instance):    
        """
        Do: when a button is pressed, call this function
        Params: instance = which object called the function
        """    
        name = instance.text
        # print(self.resolution,self.scale,self.colorSpace,self.laserPower)

        def turnCamOff():
            try:
                Clock.unschedule(self.camEvent)
                self.capture.release()
                self.isCamOn = False
            except:
                print("no cam event")

        if name == "Back":
            turnCamOff()
            self.manager.current = "Home"
        elif name == "Save":
            print("save current settings in json")
        elif name == "Run":
            # turnCamOff()
            self.showRunPopup()
            # runScan(self.resolution, self.laserPower, self.colorSpace, self.scale)
            print("teste")
        elif name =="Close":
            #TODO: uncomment
            # stopMotor()
            # TODO: save pictures in specific folder
            self.ids[str("runPopup")].dismiss()
            self.progress.cancel()
        elif name =="Cancel":
            # TODO: delete pictures that were just taken
            #TODO: uncomment
            # stopMotor()
            self.progress.cancel()
        elif name =="Pause":
            # TODO: pause the running loop
            self.isPaused = True
        elif name =="Play":
            self.isPaused = False
            turnCamOff()
            runScan(self.resolution, self.laserPower, self.colorSpace, self.scale)
        elif name =="Turn laser":
            if self.isLaserOn == True:
                self.isLaserOn = False
                turnLaserOff() #TODO: uncomment
            else:
                self.isLaserOn = True
                turnLaserOn() #TODO: uncomment
        elif name =="Turn camera":
            if self.isCamOn:
                turnCamOff()
            else:
                self.capture = cv.VideoCapture(0)
                self.camEvent = Clock.schedule_interval(self.update_cam, 1.0 / 33.0)
                self.isCamOn = True       
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))
