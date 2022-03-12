from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import sys
import os
sys.path.append(os.getcwd())
from raspberry.laser import *
# from raspberry.stepper import *
from raspberry.scan import *

class RunScreen(Screen):
    
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)
        self.isPaused = False
        self.isLaserOn = False

        self.addWidgets()
        
    def addWidgets(self):
        """
        Do : adds widgets to the page 
        """
        widgetHeight = self.winSize[1]/7
                
        # Grid containing the parameters
        paramGrid = GridLayout(cols=2)
        self.ids['paramGrid'] = paramGrid

        # Resolution widgets : label and radiobuttons
        resolutionLabel = Label(text="Resolution",size_hint_y=None, height=widgetHeight)        

        resWidget = []
        resWidget.append(Label(text="Low"))
        resWidget.append(Label(text="Medium"))
        resWidget.append(Label(text="High"))
        resWidget.append(CheckBox(group='res', allow_no_selection=False))
        resWidget.append(CheckBox(group='res', active=True, allow_no_selection=False))
        resWidget.append(CheckBox(group='res', allow_no_selection=False))

        resolutionGrid = GridLayout(cols=3,size_hint_y=None, height=widgetHeight)
        for item in resWidget:
            resolutionGrid.add_widget(item)

        paramGrid.add_widget(resolutionLabel)
        paramGrid.add_widget(resolutionGrid)


        # Scale widgets : label and slider
        scaleLabel = Label(text="Scale",size_hint_y=None, height=widgetHeight)
        scaleSlider = Slider(min=5, max=20, value=10, step = 5,value_track=True,value_track_color=[1, 1, 0, 1])
        scaleValueLabel = Label(text="10x10x10 cm")

        def OnSliderValueChange(instance,value):
            """
            Do: updates the value of the scale
            """
            scaleValueLabel.text = f"{value}x{value}x{value} cm"
        
        scaleSlider.bind(value=OnSliderValueChange)

        sliderGrid = GridLayout(cols=1,size_hint_y=None, height=widgetHeight)
        sliderGrid.add_widget(scaleValueLabel)
        sliderGrid.add_widget(scaleSlider)
        paramGrid.add_widget(scaleLabel)
        paramGrid.add_widget(sliderGrid)

        # Laser power widget : label and slider
        laserLabel = Label(text="Laser power",size_hint_y=None, height=widgetHeight)
        laserSlider = Slider(min=0, max=100, value=50, step = 10,value_track=True,value_track_color=[1, 1, 0, 1])
        laserValueLabel = Label(text="50%")
        # sets the laser a duty at the start
        setDuty(50)

        def OnSliderValueChange(instance,value):
            """
            Do: updates the value of the laser
            """
            laserValueLabel.text = f"{int(value)}%"
            setDuty(int(value))
        
        laserSlider.bind(value=OnSliderValueChange)

        laserGrid = GridLayout(cols=1,size_hint_y=None, height=widgetHeight)
        laserGrid.add_widget(laserValueLabel)
        laserGrid.add_widget(laserSlider)
        paramGrid.add_widget(laserLabel)
        paramGrid.add_widget(laserGrid)


        # Grid layout: buttons in the bottom of the screen
        bottomGrid = GridLayout(rows=1,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                                spacing=(self.winSize[0]/50,self.winSize[1]/50),
                                size_hint_y=None, height=self.winSize[1]/5)
        namesList = ["Back","Calibrate","Run"]

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

    def showCalibration(self):
        """
        Do: activates the cameras to calibrate with a chessboard
        """
        # TODO: import camera image
        calibImg = Image(source='res/not_found.png')
        self.ids['calibImg'] = calibImg

        # anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        # self.ids["anchor"] = anchor
        grid = GridLayout(cols=1,padding = (self.winSize[0]/50,self.winSize[1]/50),
                            spacing=(self.winSize[0]/100,self.winSize[1]/100))

        button = Button(text="Capture",font_size=24, background_color=self.BUTTON_COLOR, size_hint =(1,None))
        button.bind(on_press=self.callback)
        self.ids['captureButton'] = button
        grid.add_widget(button)

        laserButton = Button(text="Turn laser",font_size=24, background_color=self.BUTTON_COLOR, size_hint =(1,None))
        laserButton.bind(on_press=self.callback)
        grid.add_widget(laserButton)

        self.ids[str("paramGrid")].add_widget(calibImg)
        self.ids[str("paramGrid")].add_widget(grid)
        
    def hideCalibration(self):
        """
        Do: delete the elements to hide the camera calibration widgets
        """
        try:
            self.ids["paramGrid"].remove_widget(self.ids["calibImg"])
            self.ids["anchor"].remove_widget(self.ids["captureButton"])
            self.ids["paramGrid"].remove_widget(self.ids["anchor"])
        except:
            pass
    
    def showRunPopup(self):
        """
        Do: popup to show the progression of the scan
        """
        # TODO: import image capture each x photos taken

        # schedule check
        self.progress = Clock.schedule_interval(self.updateRun,1)

        # create content and add to the popup
        content = GridLayout(cols=1)

        # capture 
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
        namesList = ["Close","Cancel","Pause","Resume"]

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
        

        if name == "Back":
            self.hideCalibration()
            self.manager.current = "Home"
        elif name == "Calibrate":
            if any(isinstance(c, AnchorLayout) for c in list(self.ids["paramGrid"].children)):
                self.hideCalibration()
            else:
                self.showCalibration()
        elif name == "Run":
            self.showRunPopup()
            
            turnLaserOn()
            runScan("testeee","test")
            # TODO: call script to scan the whole
        elif name =="Capture":
            # TODO: call script to calibrate and save settings
            print("calibrating")
        elif name =="Close":
            turnLaserOff()
            # stopMotor()
            # TODO: save pictures in specific folder
            self.ids[str("runPopup")].dismiss()
            self.progress.cancel()
        elif name =="Cancel":
            # TODO: delete pictures that were just taken
            turnLaserOff()
            # stopMotor()
            self.progress.cancel()
        elif name =="Pause":
            # TODO: pause the running loop
            self.isPaused = True
        elif name =="Resume":
            # TODO: resume the progress
            self.isPaused = False
        elif name =="Turn laser":
            if self.isLaserOn == True:
                self.isLaserOn = False
                turnLaserOff()
            else:
                self.isLaserOn = True
                turnLaserOn()
                
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))
