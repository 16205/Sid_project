from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        winSize = Window.size

        # Grid of bottom buttons
        bottomGrid = GridLayout(rows=1,padding = (winSize[0]/50,winSize[1]/50), spacing=(winSize[0]/50,winSize[1]/50))

        namesList = ["Back","Confirm"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=(0.082,0.629,0.925,1))
            btn.bind(on_press=self.callback)
            bottomGrid.add_widget(btn)  

        
        self.add_widget(bottomGrid)

    def callback(self, instance):        
        name = instance.text

        if name == "Back":
            self.manager.current = "Home"
        elif name == "Confirm":
            print('confirm settings')
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))