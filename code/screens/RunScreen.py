from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image

class RunScreen(Screen):
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)

        winSize = Window.size

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)
        
        # _____________Grid of parameters____________
        paramGrid = GridLayout(cols=2)
        self.ids['paramGrid'] = paramGrid

        # RESOLUTION
        resolutionLabel = Label(text="Resolution")
        resLow = CheckBox(group='res', allow_no_selection=False)
        resMedium = CheckBox(group='res', active=True, allow_no_selection=False)
        resHigh = CheckBox(group='res', allow_no_selection=False)
        resLowLabel = Label(text="Low")
        resMediumLabel = Label(text="Medium")
        resHighLabel = Label(text="High")

        resolutionGrid = GridLayout(cols=3)
        resolutionGrid.add_widget(resLowLabel)
        resolutionGrid.add_widget(resMediumLabel)
        resolutionGrid.add_widget(resHighLabel)
        resolutionGrid.add_widget(resLow)
        resolutionGrid.add_widget(resMedium)
        resolutionGrid.add_widget(resHigh)

        paramGrid.add_widget(resolutionLabel)
        paramGrid.add_widget(resolutionGrid)


        # SCALE
        scaleLabel = Label(text="Scale")
        scaleSlider = Slider(min=5, max=20, value=10, step = 5,value_track=True,value_track_color=[1, 1, 0, 1])
        scaleValueLabel = Label(text="10x10x10 cm")

        def OnSliderValueChange(instance,value):
            # scaleValueLabel.text = str(int(value))
            scaleValueLabel.text = f"{value}x{value}x{value} cm"
        scaleSlider.bind(value=OnSliderValueChange)

        sliderGrid = GridLayout(cols=1)
        sliderGrid.add_widget(scaleValueLabel)
        sliderGrid.add_widget(scaleSlider)
        paramGrid.add_widget(scaleLabel)
        paramGrid.add_widget(sliderGrid)
      


        # _____________Grid of bottom buttons_____________
        bottomGrid = GridLayout(rows=1,padding = (winSize[0]/50,winSize[1]/50), spacing=(winSize[0]/50,winSize[1]/50),size_hint_y=None, height=winSize[1]/5)

        namesList = ["Back","Calibrate","Run"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=(0.082,0.629,0.925,1))
            btn.bind(on_press=self.callback)
            bottomGrid.add_widget(btn)  
        
        # ____________________________
        pageGrid.add_widget(paramGrid)
        pageGrid.add_widget(bottomGrid)
        self.add_widget(pageGrid)
    
    
    def show_calibration(self):
        winSize = Window.size
        calibImg = Image(source='res/not_found.png',size_hint_y=None, height=winSize[1]/2)
        button = Button(text="Capture",font_size=24, background_color=(0.082,0.629,0.925,1), size_hint =(.2,None)) #TODO: adjust height
        button.bind(on_press=self.callback)
        self.ids['captureButton'] = button

        self.ids[str("paramGrid")].add_widget(calibImg)
        self.ids[str("paramGrid")].add_widget(button)
        


    def callback(self, instance):        
        name = instance.text

        if name == "Back":
            self.manager.current = "Home"
        elif name == "Calibrate":   
            if str("captureButton") not in self.ids:
                self.show_calibration()                
        elif name == "Run":
            print('Running')
        elif name =="Capture":
            print("calibrating")
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))
