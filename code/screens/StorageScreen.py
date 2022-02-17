from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.popup import Popup

import os

class StorageScreen(Screen):
    def __init__(self, **kwargs):
        super(StorageScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)

        # folders of the scans
        scanGrid = GridLayout(cols=5, spacing=(self.winSize[0]/20,self.winSize[1]/20),
                                padding = (self.winSize[0]/50,self.winSize[1]/50))
        
        self.scanFolders = [name for name in os.listdir('./scans') if os.path.isdir(os.path.join('./scans', name))]
        for i in range (len(self.scanFolders)):
            toggle = ToggleButton(text=self.scanFolders[i], font_size=24, background_normal="res/folder.png",
                        background_down="res/folder_open.png",size_hint_y=None, height=self.winSize[1]/4)
            name = f"folder_{self.scanFolders[i]}"
            self.ids[name] = toggle
            scanGrid.add_widget(toggle)  

        # Grid of bottom buttons
        bottomGrid = GridLayout(rows=1,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                                spacing=(self.winSize[0]/50,self.winSize[1]/50),
                                size_hint_y=None, height=self.winSize[1]/5)

        namesList = ["Back","Delete","Convert","Open","Send"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            bottomGrid.add_widget(btn)  

        # add widgets to the screen
        pageGrid.add_widget(scanGrid)
        pageGrid.add_widget(bottomGrid)
        self.add_widget(pageGrid)
    
    def openScanPopup(self,scanName):
        # create content and add to the popup
        content = GridLayout(cols=1)

        # images 
        scanImg = Image(source='res/sid.jpg')

        # buttons
        buttons = GridLayout(cols=4,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                            spacing=(self.winSize[0]/50,self.winSize[1]/50),
                            size_hint_y=None, height=self.winSize[1]/5)
        namesList = ["Close","Delete","Convert","Send"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=self.BUTTON_COLOR)
            btn.bind(on_press=self.callback)
            buttons.add_widget(btn)  

        # add widgets
        content.add_widget(scanImg)
        content.add_widget(buttons)

        popup = Popup(title=scanName,content=content, auto_dismiss=False)
        self.ids['runPopup'] = popup

        # open the popup
        popup.open()

    def callback(self, instance):        
        name = instance.text

        if name == "Back":
            self.manager.current = "Home"
        elif name == "Delete":
            print('Delete selected elements')
        elif name == "Convert":
            print('Convert to .obj 3D or printable 3D file')
        elif name == "Send":
            self.manager.current = "Send"
        elif name == "Open":
            for scan in self.scanFolders:
                name = f"folder_{scan}"
                if self.ids[name].state == "down":
                    self.openScanPopup(scan)
                    break
        elif name =="Close":
            self.ids[str("runPopup")].dismiss()
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))