import sqlite3
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.lang import Builder      # using this no need of having main class same as kivy
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from plyer import accelerometer
from plyer import gyroscope

import datetime

# importing self made encrypting module
import encryptDatabase  

# importing self made task manager module
import taskManager

# importing self made temp User module
import tempUser

# importing module for querying
import databaseManager

#importing GRU model
import aiModel

class LoginWindow(Screen): # login screen class inheriting screen class
    username= ObjectProperty(None)
    password = ObjectProperty(None)

    
    
    
    def loginBtn(self):

        u = self.ids["username"].text     # making instance of username and password text input
        p = self.ids["password"].text

        # storing the entered username into tempUser.txt file.
        tempUser.storeName(u) 
        
        # decrypting the database
        key = encryptDatabase.loadKey() # loading the key 
        encryptDatabase.decrypt("users.db",key)  # decrypting using key

        # connecting to database
        conn = sqlite3.connect('users.db')

        # cursor
        c = conn.cursor()

        c.execute("""SELECT username, password FROM data""")

        items = c.fetchall() # fetching all usernames
        


        count = 0  # a count function to keep track of true and false


        for i in range(len(items)):
            if u == items[i][0]:    # checking if username exists or not

                if p == items[i][1]:      # checking if right password has been entered
                    
                    self.reset()
                    sm.current = "mainW"

                else:
                        popup = Popup(
                        title='Invalid password',
                        content=Label(text='You have entered wrong password.\n\nPlease retry with a correct one'),
                        size_hint = (0.5,0.5)
                        )
            
                        popup.open()
                
                    
                count+=1  # to execute next statement in case username is not found
                break  # to break the loop if the username found

        
        if count == 0:  # if count is still 0 it means there is no existing username

            popup = Popup(
                        title='Invalid Username',
                        content=Label(text='This username does not exist.\n\nPlease Sign Up'),
                        size_hint = (0.5,0.5)
                        )
            
            popup.open()


        # committing 
        conn.commit()

        # closing
        conn.close()
        
        # encrypting the database after closing connection
        encryptDatabase.encrypt("users.db",key)  # encrypting using the key

    
    
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

        # taking user data
        if self.ids["username"].text and self.ids["password"].text and self.ids["confirm"].text is not None:

            u = self.ids["username"].text
            p = self.ids["password"].text
            co = self.ids["confirm"].text

            # if password and confirm password are same then only push to database
            if p==co:  

                # using module to query and store the user data into database
                databaseManager.addUser(u,p)
        
                sm.current = "login"
            
            else:
                popup = Popup(
                            title='Invalid Password', 
                            content=Label(text='Password and Confirm-Password does not match.\n\nPlease try again'), 
                            size_hint = (0.5,0.5)
                            )

                popup.open()
        
        else:
            popup = Popup(
                        title='Invalid Credentials',
                        content=Label(text='One or more fields have been left blank.\n\nPlease fill them before pressing Submit'),
                        size_hint = (0.5,0.5)
                        )
            
            popup.open()
            

    def reset(self):   # resets everything to blank
        u = ""
        p = ""
        co =  ""

class MainWindow(Screen):
    
    def modelOn(self):

        # this will initiate the model which will start taking in the sensors data
        aiModel.feedAI()
        

    # this will check out off the model     
    def modelOff(self):
        accelerometer.disable()
        gyroscope.disable()
    
    
    
    # logic to pause notification
    def pauseNotif(self):  
        pass

    def unpauseNotif(self):  # logic to unpause notification
        taskManager.taskNotif("Here must be the selected task from the UI")


    def remindMe(self):   # logic to snooze the notifications for 5 minutes  # BUT HOW WILL ONE CAN STOP THE SNOOZE
        pass
    
    def scale(self):
        sm.current = "graph"

    def set(self):
        sm.current = "settingM"


class SettingMain(Screen):
    
    def notif(self):
        sm.current = "settingN"

    def prof(self):
        sm.current = "settingP"

    def login(self):
        sm.current = "login"

    def back(self):
        sm.current= "mainW"


class SettingProfile(Screen):
    
    n = ObjectProperty(None)
    a = ObjectProperty(None)
    w = ObjectProperty(None)
    h = ObjectProperty(None)
    j = ObjectProperty(None)
    m = ObjectProperty(None)

    # this function will save the data into the database
    def save(self):

        


        n = self.ids["n"].text
        a = self.ids["age"].text
        w = self.ids["weight"].text
        h = self.ids["heigh"].text
        j = self.ids["job"].text
        g = self.ids["gender"].text
        


        if n and a and w and h and j and g  is not None:
            databaseManager.addProfile(n,a,w,h,j,g)

            
                    
        else:
            popup = Popup(
            title='Invalid Credentials',
            content=Label(text='One or more fields have been left blank.\n\nPlease fill them before pressing Submit'),
            size_hint = (0.5,0.5)
            )

            popup.open()



           
    
    def back(self):
        sm.current = "settingM"
    
    
    


class SettingNotif(Screen):

    def back(self):
        sm.current = "settingM"

class Graph(Screen):
    
    def back(self):
        sm.current="mainW"



# inheriting screenmanager class properties to manage multiple screens
class WindowManager(ScreenManager): 
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
    
    # decrypting database and creating connection
    # checking whether the data table already exists in user.db.
    # If not, then creating a table, closing connection and encrypting database.
    databaseManager.creatingTable()


    # similarly initiating task manager's tasks table
    databaseManager.creatingTableTaskManager()

    # initiating database to store the users movement profile
    databaseManager.createTableStoreProfile()

    def build(self):

        return sm    # going to screenmanager



if __name__ == "__main__":
    MyMainApp().run()