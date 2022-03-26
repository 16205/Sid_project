from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)

        # settings grid
        settingsGrid = GridLayout(cols=2,spacing=(self.winSize[0]/50,self.winSize[1]/50),
                                padding = (self.winSize[0]/50,self.winSize[1]/50))
        self.ids['settingsGrid'] = settingsGrid

        connectLabel = Label(text="Connect slave raspberry to Master",size_hint_y=None, height=self.winSize[1]/10)
        camerasLabel = Label(text="Test the cameras",size_hint_y=None, height=self.winSize[1]/5)
        buttonsName = ["Connect", "Master", "Slave"]
        buttons = []
        for i in range (len(buttonsName)):
            btn = Button(text=buttonsName[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            buttons.append(btn)
        
        # button for connection
        buttons[0].size_hint_y = None
        buttons[0].height = self.winSize[1]/8

        # buttons for camera
        camerasGrid = GridLayout(cols=1,size_hint_y=None, height=self.winSize[1]/5,
                                spacing=(self.winSize[0]/100,self.winSize[1]/100))
        camerasGrid.add_widget(buttons[1])
        camerasGrid.add_widget(buttons[2])

        settingsGrid.add_widget(connectLabel)
        settingsGrid.add_widget(buttons[0])
        settingsGrid.add_widget(camerasLabel)
        settingsGrid.add_widget(camerasGrid)


        # Grid of bottom buttons
        bottomGrid = GridLayout(rows=1,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                                spacing=(self.winSize[0]/50,self.winSize[1]/50),
                                size_hint_y=None, height=self.winSize[1]/5)

        namesList = ["Back","Confirm"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            bottomGrid.add_widget(btn)  
        
        # add widgets
        pageGrid.add_widget(settingsGrid)
        pageGrid.add_widget(bottomGrid)
        self.add_widget(pageGrid)

        self.addCalibration()

        """
        TODO: 
            - add radio buton to select 3D object file to convert to (.obj only?)
            - add radio button to select by which means will we send the files
                - usb
                - wifi / scp / SSH => add apearing button to establish ssh connection or stg
        """
    def addCalibration(self):
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

        self.ids[str("settingsGrid")].add_widget(calibImg)
        self.ids[str("settingsGrid")].add_widget(grid)

    def callback(self, instance):        
        name = instance.text

        if name == "Back":
            self.manager.current = "Home"
        elif name == "Confirm":
            print('confirm settings')
        elif name == "Connect":
            print('Connecting')
        elif name == "Master":
            print('configure master camera')
        elif name == "Slave":
            print('configure slave camera')
        elif name =="Capture":
            print("calibrating")
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))