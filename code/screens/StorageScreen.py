from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

import os

class StorageScreen(Screen):
    def __init__(self, **kwargs):
        super(StorageScreen, self).__init__(**kwargs)

        self.winSize = Window.size
        self.BUTTON_COLOR = (0.082,0.629,0.925,1)
        Window.bind(on_resize=self.on_window_resize)

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)

        # folders of the scans
        scanGrid = GridLayout(cols=5, spacing=(self.winSize[0]/20,self.winSize[1]/20),
                                padding = (self.winSize[0]/50,self.winSize[1]/50),size_hint_y = None)
        scanGrid.bind(minimum_height=scanGrid.setter('height'))
        self.ids["scanGrid"] = scanGrid
        
        self.scanFolders = [name for name in os.listdir('./scans') if os.path.isdir(os.path.join('./scans', name))]
        for i in range (len(self.scanFolders)):
            toggle = ToggleButton(text=self.scanFolders[i], font_size=24, background_normal="res/folder.png",
                        background_down="res/folder_open.png",size_hint = (None, None))
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

        # scroll view
        root = ScrollView(size=scanGrid.size, do_scroll_y=True )

        # add widgets to the screen
        root.add_widget(scanGrid)
        pageGrid.add_widget(root)      
        pageGrid.add_widget(bottomGrid)
        self.add_widget(pageGrid)

    def on_window_resize(self, window, width, height):
        # adjusts folders height and width
        for elem in self.ids["scanGrid"].children:
            elem.height = height /3
            elem.width = width /4

    
    def openScanPopup(self,scanName):
        # create content and add to the popup
        content = GridLayout(cols=1)

        # images 
        scanImg = Image(source='scans/'+scanName+'/sid.jpg')

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
    
    def doWithFolders(self, methodToRun, doBreak= True):
        for scan in self.scanFolders:
                name = f"folder_{scan}"
                if self.ids[name].state == "down":
                    methodToRun(scan)
                    if doBreak:
                        break

    def sendFolders(self,folders):
        self.manager.current = "Send"
        #TODO: modify

    def deleteFolders(self,folders):
        print("deleting")
        #TODO: faire ce truc
    def callback(self, instance):        
        name = instance.text

        if name == "Back":
            self.manager.current = "Home"
        elif name == "Delete":
            self.doWithFolders(self.deleteFolders,False)
        elif name == "Convert":
            print('Convert to .obj 3D or printable 3D file')
        elif name == "Send":
            # TODO: gérer cette couille
            pass
            # self.doWithFolders(self.sendFolders)
            # self.manager.current = "Send"
        elif name == "Open":
            self.doWithFolders(self.openScanPopup)
        elif name =="Close":
            self.ids[str("runPopup")].dismiss()
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))