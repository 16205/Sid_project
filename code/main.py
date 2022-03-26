from kivy.app import App
from kivy.uix.screenmanager import *
from kivy.core.window import Window

from screens.HomePageScreen import HomePageScreen 
from screens.RunScreen import  RunScreen
from screens.StorageScreen import StorageScreen
from screens.SettingsScreen import SettingsScreen   


class MainApp(App):
    
    def build(self):
        self.title = "SID alpha version 1.4"
        Window.fullscreen = False
        # build the screen manager
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(HomePageScreen(name='Home'))
        sm.add_widget(SettingsScreen(name='Settings'))      
        sm.add_widget(RunScreen(name='Run'))
        sm.add_widget(StorageScreen(name='Storage'))

        return sm

if __name__ == '__main__':
    MainApp().run()