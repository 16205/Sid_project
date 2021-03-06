from kivy.app import App
from kivy.uix.screenmanager import *
from kivy.core.window import Window

from screens.HomePageScreen import HomePageScreen 
from screens.RunScreen import  RunScreen
from screens.StorageScreen import StorageScreen
from screens.SettingsScreen import SettingsScreen

import raspberry.GPIO_setup as stp

class MainApp(App):
    
    def build(self):
        self.title = "SID alpha version 1.4"
        
        # Setup GPIO
        stp.gpioSetup()
        
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