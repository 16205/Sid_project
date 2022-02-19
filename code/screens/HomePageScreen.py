from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen


class HomePageScreen(Screen):
    def __init__(self, **kwargs):
        super(HomePageScreen, self).__init__(**kwargs)
        winSize = Window.size
        grid = GridLayout(cols=2, padding = (winSize[0]/10,winSize[1]/10), spacing=(winSize[0]/50,winSize[1]/50))

        namesList = ["Run","Settings","Storage"]

        for i in range (len(namesList)):
            btn = Button(text=namesList[i], font_size=24, background_color=(0.082,0.629,0.925,1))
            btn.bind(on_press=self.callback)
            grid.add_widget(btn)  

        
        self.add_widget(grid)

    def callback(self, instance):        
        name = instance.text

        if name == "Run":
            self.manager.current = "Run"
        elif name == "Settings":
            self.manager.current = "Settings"
        elif name == "Storage":
            self.manager.current = "Storage"
        # elif name == "Send":
        #     self.manager.current = "Send"
        else:
            print('The button %s is not in the list of recognized buttons' % (instance))