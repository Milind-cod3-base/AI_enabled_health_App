import sqlite3
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.lang import Builder      # using this no need of having main class same as kivy
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

class LoginWindow(Screen): # login screen class inheriting screen class
    username= ObjectProperty(None)
    password = ObjectProperty(None)


    def loginBtn(self):
        self.reset()
        sm.current = "mainW"

    def createBtn(self):
        self.reset()  # clears everything
        sm.current = "create"

    def reset(self): # resets the username and password section
        self.username = ""  
        self.password = ""
        

class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm = ObjectProperty(None)

    def login(self):
        self.reset() # clears all
        sm.current = "login"

    def submit(self):
        pass

    def reset(self):   # resets everything to blank
        username = ""
        password = ""
        confirm = ""

class MainWindow(Screen):
    
    def modelOn():
        pass # this will check in the model
    
    def modelOff():
        pass   # this will check out off the model

class SettingMain(Screen):
    pass

class SettingProfile(Screen):
    pass

class SettingNotif(Screen):
    pass

class Graph(Screen):
    pass

class WindowManager(ScreenManager): # inheriting screenmanager class properties to manage multiple screens
    pass


def invalidLogin():
    pass

def invalidForm():
    pass

kv = Builder.load_file("my.kv") # loading my.kv file

sm = WindowManager() # instance of class

# putting screens in widget; standard procedure
screens = [LoginWindow(name="login"),
            CreateAccountWindow(name="create"),
            MainWindow(name="mainW"), 
            SettingMain(name="settingM"), 
            SettingProfile(name="settingP"), 
            SettingNotif(name="settingN"),
            Graph(name="graph")]

for i in screens:
    sm.add_widget(i) 


sm.current = "login"  # default screen must be login


class MyMainApp(App): # inheriting the properties of App class from kivy library
    def build(self):
        return sm    # going to screenmanager



if __name__ == "__main__":
    MyMainApp().run()