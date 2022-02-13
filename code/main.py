from kivy.app import App
from kivy.uix.screenmanager import *

from HomePageScreen import HomePageScreen 
from RunScreen import  RunScreen
from SendScreen import SendScreen
from StorageScreen import StorageScreen
from SettingsScreen import SettingsScreen


class MainApp(App):
    
    def build(self):
        self.title = "SID 0.1"

        # build the screen manager
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(HomePageScreen(name='Home'))
        sm.add_widget(SettingsScreen(name='Settings'))
        sm.add_widget(RunScreen(name='Run'))
        sm.add_widget(StorageScreen(name='Storage'))
        sm.add_widget(SendScreen(name='Send'))

        return sm

if __name__ == '__main__':
    MainApp().run()