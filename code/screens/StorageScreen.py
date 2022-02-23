from kivy.uix.label import Label
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
        self.isPopupOpen = False

        # get the files from the os
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))

        # _____________the whole page_____________
        pageGrid = GridLayout(cols=1)

        # folders of the scans
        scanGrid = GridLayout(cols=4, spacing=(self.winSize[0]/20,self.winSize[1]/20),
                                padding = (self.winSize[0]/50,self.winSize[1]/50),size_hint_y = None)
        scanGrid.bind(minimum_height=scanGrid.setter('height'))
        self.ids["scanGrid"] = scanGrid
        
        self.scanFolders = [name for name in os.listdir(f'{cwd}/../scans') if os.path.isdir(os.path.join(f'{cwd}/../scans', name))]
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

        # adjust gridlayout size
        self.on_window_resize(Window,self.winSize[0], self.winSize[1])

    def on_window_resize(self, window, width, height):
        # adjusts folders height and width
        for elem in self.ids["scanGrid"].children:
            elem.height = height /4
            elem.width = width /5

    
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
        self.isPopupOpen = True

    def operationPopup(self,folders,operation,methodToRun):
        # btn callback
        def btnCallBack(instance):
            name = instance.text            
            popup.dismiss()

            if name == "Yes":
                if self.isPopupOpen == False:
                    self.unselectFolders()
                methodToRun(folders)

        # create content and add to the popup
        content = GridLayout(cols=1)

        # text
        text = "will you " + operation +" the following scans :"
        for a in folders:
            text += "\n - " + a
        label = Label(text=text,font_size=20)

        # buttons
        buttons = GridLayout(cols=2,padding = (self.winSize[0]/50,self.winSize[1]/50), 
                            spacing=(self.winSize[0]/50,self.winSize[1]/50),
                            size_hint_y=None, height=self.winSize[1]/5)

        btnYes = Button(text="Yes", font_size=24, background_color=self.BUTTON_COLOR)        
        btnNo = Button(text="No", font_size=24, background_color=self.BUTTON_COLOR)

        btnYes.bind(on_press=btnCallBack)
        btnNo.bind(on_press=btnCallBack)

        buttons.add_widget(btnNo) 
        buttons.add_widget(btnYes)  

        # add widgets
        content.add_widget(label)
        content.add_widget(buttons)

        popup = Popup(title=operation,content=content, auto_dismiss=False, size_hint=(.5,.5))
        self.ids[f'{operation}Popup'] = popup
        # open the popup
        popup.open()
        # self.isPopupOpen = True        
    
    def doWithFolders(self, methodToRun, doBreak= True, operationName=""):
        folders = []
        for scan in self.scanFolders:
            name = f"folder_{scan}"
            if self.ids[name].state == "down":
                folders.append(scan)
                if doBreak:
                    break
        if len(folders) !=0:
            if operationName =="open":
                methodToRun(folders)
            else:
                self.operationPopup(folders,operationName,methodToRun)

    def openFolder(self,folders):
        self.openScanPopup(folders[0])

    def sendFolders(self,folders):
        for folder in folders:
            print(f"sending {folder}")

    def deleteFolders(self,folders):
        if self.isPopupOpen:
            self.closePopup("runPopup")
        for folder in folders:
            self.ids["scanGrid"].remove_widget(self.ids[f"folder_{folder}"])
            print(f"deleting folder {folder}")
    
    def convertFolders(self,folders):
        for folder in folders:
            print(f'Convert {folder} to a .obj file')

    def unselectFolders(self):
        # when quitting the screen or a popup
        for scan in self.scanFolders:
            name = f"folder_{scan}"
            self.ids[name].state = "normal"
    
    def closePopup(self,id):
        self.ids[str(id)].dismiss()
        self.isPopupOpen = False
        self.unselectFolders()

    def callback(self, instance):        

        name = instance.text
        if name == "Back":
            self.unselectFolders()
            self.manager.current = "Home"
        elif name == "Delete":
            if self.isPopupOpen:
                self.doWithFolders(self.deleteFolders,operationName="delete")
            else:
                self.doWithFolders(self.deleteFolders,False,operationName="delete")
        elif name == "Convert":
            if self.isPopupOpen:
                self.doWithFolders(self.convertFolders,operationName="convert")
            else:
                self.doWithFolders(self.convertFolders, False,operationName="convert")
        elif name == "Send":
            if self.isPopupOpen:
                self.doWithFolders(self.sendFolders,operationName="send")
            else:
                self.doWithFolders(self.sendFolders, False,operationName="send")
        elif name == "Open":
            self.doWithFolders(self.openFolder,operationName="open")
        elif name =="Close":
            self.closePopup("runPopup")
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))