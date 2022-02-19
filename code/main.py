from kivy.app import App
from kivy.uix.screenmanager import *

from screens.HomePageScreen import HomePageScreen 
from screens.RunScreen import  RunScreen
from screens.SendScreen import SendScreen
from screens.StorageScreen import StorageScreen
from screens.SettingsScreen import SettingsScreen   


class MainApp(App):
    
    def build(self):
        self.title = "SID alpha version 1.0"

        # build the screen manager
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(HomePageScreen(name='Home'))
        sm.add_widget(SettingsScreen(name='Settings'))      
        sm.add_widget(RunScreen(name='Run'))
        sm.add_widget(StorageScreen(name='Storage'))
        # sm.add_widget(SendScreen(name='Send'))

        return sm

if __name__ == '__main__':
    MainApp().run()