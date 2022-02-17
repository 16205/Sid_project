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

class RunScreen(Screen):
    
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)
        
        # _____________Grid of parameters____________
        paramGrid = GridLayout(cols=2)
        self.ids['paramGrid'] = paramGrid

        # RESOLUTION
        resolutionLabel = Label(text="Resolution",size_hint_y=None, height=self.winSize[1]/5)
        resLow = CheckBox(group='res', allow_no_selection=False)
        resMedium = CheckBox(group='res', active=True, allow_no_selection=False)
        resHigh = CheckBox(group='res', allow_no_selection=False)
        resLowLabel = Label(text="Low")
        resMediumLabel = Label(text="Medium")
        resHighLabel = Label(text="High")

        resolutionGrid = GridLayout(cols=3,size_hint_y=None, height=self.winSize[1]/5)
        resolutionGrid.add_widget(resLowLabel)
        resolutionGrid.add_widget(resMediumLabel)
        resolutionGrid.add_widget(resHighLabel)
        resolutionGrid.add_widget(resLow)
        resolutionGrid.add_widget(resMedium)
        resolutionGrid.add_widget(resHigh)

        paramGrid.add_widget(resolutionLabel)
        paramGrid.add_widget(resolutionGrid)


        # SCALE
        scaleLabel = Label(text="Scale",size_hint_y=None, height=self.winSize[1]/5)
        scaleSlider = Slider(min=5, max=20, value=10, step = 5,value_track=True,value_track_color=[1, 1, 0, 1])
        scaleValueLabel = Label(text="10x10x10 cm")

        def OnSliderValueChange(instance,value):
            """
            Do: updates the value of the slider
            """
            scaleValueLabel.text = f"{value}x{value}x{value} cm"
        scaleSlider.bind(value=OnSliderValueChange)

        sliderGrid = GridLayout(cols=1,size_hint_y=None, height=self.winSize[1]/5)
        sliderGrid.add_widget(scaleValueLabel)
        sliderGrid.add_widget(scaleSlider)
        paramGrid.add_widget(scaleLabel)
        paramGrid.add_widget(sliderGrid)

        # _____________Grid of bottom buttons_____________
        bottomGrid = GridLayout(rows=1,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                                spacing=(self.winSize[0]/50,self.winSize[1]/50),
                                size_hint_y=None, height=self.winSize[1]/5)

        namesList = ["Back","Calibrate","Run"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            bottomGrid.add_widget(btn)  
        
        # ____________________________
        pageGrid.add_widget(paramGrid)
        pageGrid.add_widget(bottomGrid)
        self.add_widget(pageGrid)
    
    
    def showCalibration(self):
        """
        Do: activates the cameras to calibrate with a chessboard
        OnCapturePressEvent: capture an image and launch the script to calibrate
        """
        calibImg = Image(source='res/not_found.png')
        self.ids['calibImg'] = calibImg

        anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        self.ids["anchor"] = anchor
        button = Button(text="Capture",font_size=24, background_color=self.BUTTON_COLOR, size_hint =(1,None)) #TODO: adjust height
        button.bind(on_press=self.callback)
        self.ids['captureButton'] = button

        anchor.add_widget(button)
        self.ids[str("paramGrid")].add_widget(calibImg)
        self.ids[str("paramGrid")].add_widget(anchor)
        
    def hideCalibration(self):
        """
        Do: delete the elements to hide the camera
        """
        
        self.ids["paramGrid"].remove_widget(self.ids["calibImg"])
        self.ids["anchor"].remove_widget(self.ids["captureButton"])
        self.ids["paramGrid"].remove_widget(self.ids["anchor"])
    
    def showRunPopup(self):
        """
        Do: popup to show the progression of the scan
        & launches script that scans an object
        """
        # create content and add to the popup
        content = GridLayout(cols=1)

        scanImg = Image(source='res/sid.jpg')
        buttons = GridLayout(cols=4,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                            spacing=(self.winSize[0]/50,self.winSize[1]/50),
                            size_hint_y=None, height=self.winSize[1]/5)
        namesList = ["Close","Cancel","Pause","Resume"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            buttons.add_widget(btn)  

        content.add_widget(scanImg)
        content.add_widget(buttons)

        popup = Popup(title='Run 3D scan',content=content, auto_dismiss=False)
        self.ids['runPopup'] = popup

        # open the popup
        popup.open()


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
        elif name =="Capture":
            print("calibrating")
        elif name =="Close":
            self.ids[str("runPopup")].dismiss()
        elif name =="Cancel":
            print("cancel")
            self.ids[str("runPopup")].dismiss()
        elif name =="Pause":
            print("pause")
        elif name =="Resume":
            print("resume")
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))
