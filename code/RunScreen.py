from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox


class RunScreen(Screen):
    def __init__(self, **kwargs):
        super(RunScreen, self).__init__(**kwargs)

        winSize = Window.size

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)
        
        # _____________Grid of parameters____________
        paramGrid = GridLayout(cols=2)

        # RESOLUTION
        resolutionLabel = Label(text="Resolution")
        resolutionSlider = Slider(min=100, max=2000, value=1000,value_track=True, value_track_color=[1, 1, 0, 1])
        resolutionValueLabel = Label(text=str(1000))

        def OnSliderValueChange(instance,value):
            resolutionValueLabel.text = str(int(value))
        resolutionSlider.bind(value=OnSliderValueChange)

        sliderGrid = GridLayout(cols=1)
        sliderGrid.add_widget(resolutionValueLabel)
        sliderGrid.add_widget(resolutionSlider)
        paramGrid.add_widget(resolutionLabel)
        paramGrid.add_widget(sliderGrid)

        # DISTANCE
        testBtn = Button(text="test")
        paramGrid.add_widget(testBtn)

        


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

    def callback(self, instance):        
        name = instance.text

        if name == "Back":
            self.manager.current = "Home"
        elif name == "Calibrate":
            print('Calibrate')
        elif name == "Run":
            print('Running')
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))
