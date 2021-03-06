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
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

import tensorflow as tf
import numpy as np
import pandas as pd
import scipy.stats as stats

# transitioning from kivy to kivymd
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd_extensions.akivymd.uix.charts import AKPieChart

import datetime
import matplotlib.pyplot as plt

# importing self made  module
import encryptDatabase
import tempUser
import databaseManager
import permissionSensors
import push_notification
import graphQuery
import aiModel
import offlineAi

from plyer import notification 


# giving main window size similiar to a phone screen
Window.size= (320,500)


# login screen class inheriting screen class
class LoginWindow(Screen): 
    username= ObjectProperty(None)
    password = ObjectProperty(None)

  
    
    # This method checks if the input username 
    # is already present, if it doesn't it will ask to signup
    # if user is present, then check if its password is correct
    def loginBtn(self):
        
        # making instance of username and password text input
        u = self.ids["username"].text     
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

        # fetching all usernames
        items = c.fetchall() 
        

        # a count function to keep track of true and false
        count = 0 

        # loop to parse through the users database
        for i in range(len(items)):
            if u == items[i][0]:    # checking if username exists or not

                if p == items[i][1]:      # checking if right password has been entered
                    
                    # reseting text input fields
                    self.ids["username"].text= ""
                    self.ids["password"].text = ""

                    # using below code for transition instead of sm.current
                    self.parent.current = "mainW"
                    
                    

                else:
                        popup = Popup(
                        title='Invalid password',
                        content=Label(text='You have entered wrong password.\n\nPlease retry with a correct one'),
                        size_hint = (0.5,0.5)
                        )
            
                        popup.open()
                
                # to execute next statement in case username is not found
                count+=1  
                # to break the loop if the username found
                break  

        # if count is still 0 it means there is no existing username
        if count == 0:  

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

    
    # this button transits users to the signup page
    def createBtn(self):
        
        self.parent.current = "create"

    
        
# create account window classs
class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm = ObjectProperty(None)

    # This method transits user to the login window in case he/she
    # already has the ID in the app.
    def login(self):

        # clearing user's credential data before screen transition
        self.ids["username"].text = ""
        self.ids["password"].text = ""
        self.ids["confirm"].text = ""
        self.parent.current = "login"

    # This method checks if all the textfields are filled and the
    # password and confirm password are same. If all is ok, then
    # the user can transit to the login window where he/she can enter
    # credentials again to enter the app.
    def submit(self):

        # taking user data from the front end
        if self.ids["username"].text and self.ids["password"].text and self.ids["confirm"].text is not None:

            u = self.ids["username"].text
            p = self.ids["password"].text
            co = self.ids["confirm"].text

            # if password and confirm password are same then only push to database
            if p==co:  

                # using module to query and store the user data into database
                databaseManager.addUser(u,p)

                # clearing user's credential data before screen transition
                self.ids["username"].text = ""
                self.ids["password"].text = ""
                self.ids["confirm"].text = ""
                
                # tranisitioning to the LoginWIndow
                self.parent.current = "login"
            
            # if the password annd confirm passowrd text field doesnt match, then it gives a pop up
            else:
                popup = Popup(
                            title='Invalid Password', 
                            content=Label(text='Password and Confirm-Password does not match.\n\nPlease try again'), 
                            size_hint = (0.5,0.5)
                            )

                popup.open()
        
        # if fields are not filled, then a pop up will occur
        else:
            popup = Popup(
                        title='Invalid Credentials',
                        content=Label(text='One or more fields have been left blank.\n\nPlease fill them before pressing Submit'),
                        size_hint = (0.5,0.5)
                        )
            
            popup.open()
            

    

# This has the main screen and its widgets functions
class MainWindow(Screen):
    
    # a method to set the selected motivation task as the text for the
    # notification in the timer selected by the user (2 hours is default)
    def remindMe(self):   

        # if motivation task 1 check box is active, it should be in the notification
        if self.mot1.active:

            # acquiring task from the label
            tsk1 = self.ids.task1.text

            # storing the temporary task in temporaryMotivationTask.txt file
            tempUser.storeMotivation(tsk1)

            # using this method to read the selected task and notify in given time
            push_notification.repeatNotif()

            # starting the loop of selected notification timer
            push_notification.startTimer()
            
        
        # if motivation task 2 check box is active, it should be in the notification
        elif self.mot2.active:
            # acquiring task from the label
            tsk2 = self.ids.task2.text
            # storing the temporary task in temporaryMotivationTask.txt file
            tempUser.storeMotivation(tsk2)
            # using this method to read the selected task and notify in given time
            push_notification.repeatNotif()
            # starting the loop of selected notification timer
            push_notification.startTimer()
        
        # if motivation task 3 check box is active, it should be in the notification
        elif self.mot3.active:
            # acquiring task from the label
            tsk3 = self.ids.task3.text
            tempUser.storeMotivation(tsk3)
            # using this method to read the selected task and notify in given time
            push_notification.repeatNotif()
            # starting the loop of selected notification timer
            push_notification.startTimer()

        # if motivation task 4 check box is active, it should be in the notification
        elif self.mot4.active:
            # acquiring task from the label
            tsk4 = self.ids.task4.text
            # storing the temporary task in temporaryMotivationTask.txt file
            tempUser.storeMotivation(tsk4)
            # using this method to read the selected task and notify in given time
            push_notification.repeatNotif()
            # starting the loop of selected notification timer
            push_notification.startTimer()
            

    # this will initiate the model which will start taking in the sensors data
    def modelOn(self):


        if platform == "android":
            aiModel.feedAI()
        else:
            offlineAi.Load_Model()
            offlineAi.predict2()

        
        

    # this will check out off the model  and  model wont run
    def modelOff(self):
        accelerometer.disable()
        gyroscope.disable()
        
    
    # taking first task output from getTask fucntion
    # and displaying it on the motivation task label
    def motTask1(self):
        return databaseManager.getTask()[0]


    # taking second task output from getTask fucntion
    # and displaying it on the motivation task label
    def motTask2(self):
        return databaseManager.getTask()[1]


    # taking third task output from getTask fucntion
    # and displaying it on the motivation task label
    def motTask3(self):
        return databaseManager.getTask()[2]


    # taking fourth task output from getTask fucntion
    # and displaying it on the motivation task label
    def motTask4(self):
        return databaseManager.getTask()[3]
    



    
    # logic to pause notificatio
    def pauseNotif(self):  
        pass

    # this will resume the notifications
    def unpauseNotif(self):  # logic to unpause notification
        pass


    # method to take user to graph page
    def scale(self):
        self.parent.current = "graph"

    # method to go to main setting screen
    def set(self):
        self.parent.current = "settingM"


# Main setting screen 
class SettingMain(Screen):
    
    # transition to notification setting
    def notif(self):
        self.parent.current = "settingN"

    # transition to profile setting
    def prof(self):
        self.parent.current = "settingP"

    # logout button which takes the user out of the application
    def login(self):

        # when the user will logout, the notification timer
        # will set to 2 hours(default state)
        tempUser.storeNotificationTimer(2)
        
        self.parent.current = "login"

    # method to transit for mainWindow 
    def back(self):
        self.parent.current= "mainW"

    
    # job of this function will not only to change the screen
    # but also to the refresh the userdata screen with the new
    # logged in user
    def disData(self): 
    
        self.parent.current = "userdata"

    


# settings window for adding user details
class SettingProfile(Screen):
    
    # setting up variables with None object properties
    n = ObjectProperty(None)
    a = ObjectProperty(None)
    w = ObjectProperty(None)
    h = ObjectProperty(None)
    j = ObjectProperty(None)
    m = ObjectProperty(None)

    # this function will save the data into the database
    def save(self):

        

        # taking input from 3 text input fields
        n = self.ids["n"].text
        w = self.ids["weight"].text
        h = self.ids["heigh"].text


        # extracting values from the checkboxes for job
        if self.exec.active:
            j= "executive"
        
        elif self.manage.active:
            j= "manager"

        elif self.programmer.active:
            j= "programmer"

       
        # extracting values from the checkboxes for age
        if self.age1.active:
            a= "21-30"

        elif self.age2.active:
            a = "31-40"

        elif self.age3.active:
            a = "41-50"

        elif self.age4.active:
            a = "51+"

        
        # extracting values from the checkboxes for gender
        if self.male.active:
            g = "male"

        elif self.female.active:
            g = "female"


        
        

        #if n and a and w and h and j and g  is not None:
        databaseManager.addProfile(n,a,w,h,j,g)

            
                    
        # pop for assurance of saved
        popup = Popup(
        title='Saved',
        content=Label(text='Your data has been saved securely'),
        size_hint = (0.5,0.5)
        )

        popup.open()



           
    # Main setting screen transition
    def back(self):
        self.parent.current = "settingM"
    

# settings window to set the notification delay, 2 hours is default
class SettingNotif(Screen):

    # function to save user's notification setting
    def save(self):
        
        # if one hour checkbox is active, 
        # notification timer is set to 1 hour
        if self.oneH.active:
            tempUser.storeNotificationTimer(1)
                
        # if one hour checkbox is active, 
        # notification timer is set to 2 hour
        elif self.twoH.active:
            tempUser.storeNotificationTimer(2)
    
        # if one hour checkbox is active, 
        # notification timer is set to 3 hour
        elif self.threeH.active:
            tempUser.storeNotificationTimer(3)

        # if one hour checkbox is active, 
        # notification timer is set to 4 hour
        elif self.fourH.active:   
            tempUser.storeNotificationTimer(4) 
    
    # takes back to the settings main screen
    def back(self):
        self.parent.current = "settingM"


# class for Graph screen 
class Graph(Screen):
    
    # method for mainwindow transition
    def back(self):
        self.parent.current="mainW"


# inherting mdfflatlatlayout and fakerect class
class ProfileCard(MDFloatLayout, FakeRectangularElevationBehavior):
    pass

# below are the cards just for the sole purpose of existing 
# of cards in kivyMD ui.
class UserCard(MDCard):
    pass

class MovementAnalysisCard(ProfileCard):
    pass

class MotivationTaskCard(ProfileCard):
    pass

class SettingsCard(ProfileCard):
    pass


# class for screen for displaying daily user activity
class DailyGraph(Screen):

    # This function starts when the user enters the screen
    def on_enter(self):
        """ As AkPieChart takes values only in percentage
        We must convert time into percentage which will be later
        displayed in the form of pie chart with three labels"""

        # percentage time spent sitting in a day
        # s_perc= ((graphQuery.dailySitting)/ (datetime.datetime.now() - datetime.timedelta(days=1)))*100
        # # # percentage time spent walking in a day
        # w_perc= ((graphQuery.dailyWalking)/  (datetime.datetime.now() - datetime.timedelta(days=1)))*100
        # # # percentage time spent running in a day
        # r_perc= ((graphQuery.dailyRunning)/  (datetime.datetime.now() - datetime.timedelta(days=1)))*100
        s_perc = 20
        w_perc = 30
        r_perc = 50
        # putting above variables along with labels in a dictionary inside a list
        items = [{"Sitting": s_perc, "Walking":w_perc, "Running": r_perc}]
        self.piechart = AKPieChart(
            items=items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(300,300)
        )
        self.ids.chart_box.add_widget(self.piechart)
        
    # This function removes the chart when the user leaves the screen  
    def remove_chart(self):
         self.ids.chart_box.remove_widget(self.piechart)
    

# class for screen for displaying weekly user activity 
class WeeklyGraph(Screen):

    # This function starts when the user enters the screen
    def on_enter(self):

        """ As AkPieChart takes values only in percentage
        We must convert time into percentage which will be later
        displayed in the form of pie chart with three labels"""
        
        # percentage time spent sitting in a week
        s_perc= ((graphQuery.weeklySitting)/ (datetime.datetime.now() - datetime.timedelta(days=7)))*100
        # percentage time spent walking in a week
        w_perc= ((graphQuery.weeklyWalking)/  (datetime.datetime.now() - datetime.timedelta(days=7)))*100
        # percentage time spent running in a week
        r_perc= ((graphQuery.weeklyRunning)/  (datetime.datetime.now() - datetime.timedelta(days=7)))*100

        # putting above variables along with labels in a dictionary inside a list
        items = [{"Sitting": s_perc, "Walking":w_perc, "Running": r_perc}]
        self.piechart = AKPieChart(
            items=items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(300,300)
        )
        self.ids.chart_box.add_widget(self.piechart)
        
    # This function removes the chart when the user leaves the screen  
    def remove_chart(self):
         self.ids.chart_box.remove_widget(self.piechart)



# class for screen for displaying monthly user activity
class MonthlyGraph(Screen):
    
    # This function starts when the user enters the screen
    def on_enter(self):
        
        """ As AkPieChart takes values only in percentage
        We must convert time into percentage which will be later
        displayed in the form of pie chart with three labels"""

        # percentage time spent sitting in a monthly
        s_perc= ((graphQuery.monthlySitting)/ (datetime.datetime.now() - datetime.timedelta(days=30)))*100
        # percentage time spent walking in a monthly
        w_perc= ((graphQuery.monthlyWalking)/  (datetime.datetime.now() - datetime.timedelta(days=30)))*100
        # percentage time spent running in a monthly
        r_perc= ((graphQuery.monthlyRunning)/  (datetime.datetime.now() - datetime.timedelta(days=30)))*100

        # putting above variables along with labels in a dictionary inside a list
        items = [{"Sitting": s_perc, "Walking":w_perc, "Running": r_perc}]
        self.piechart = AKPieChart(
            items=items,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=[None, None],
            size=(300,300)
        )
        self.ids.chart_box.add_widget(self.piechart)
        
    # This function removes the chart when the user leaves the screen  
    def remove_chart(self):
         self.ids.chart_box.remove_widget(self.piechart)


# setting new classes here for new windows
class ProfileScroller(ScrollView):
    pass 


# classes reperesenting systemPermission
class SystemPermission(Screen):

    def allowAccelerometer(self):
        permissionSensors.allowAccelero

    def allowGyrometer(self):
        permissionSensors.allowGyro

    def allowStorage(self):
        permissionSensors.memoryAccess

   
# classes user data class 
class UserData(Screen):
    
    
    if databaseManager.userGender != None :
    
        # using stringProperty to get the text into the label
        n = StringProperty(databaseManager.userName)  
        age = StringProperty(databaseManager.userAge)
        gender = StringProperty(databaseManager.userGender)
        weight = StringProperty(databaseManager.userWeight)
        
        # name of the below variables have been changed as height and position are
        # prexisting variables in the kivy file.
        hei= StringProperty(databaseManager.userHeight)
        po = StringProperty(databaseManager.userPosition)
    
    else:
        n = StringProperty("empty")
        age = StringProperty("empty")
        gender = StringProperty("empty")
        weight = StringProperty("empty")
        hei= StringProperty("empty")
        po = StringProperty("empty")
    

        


# instance of class
sm = ScreenManager() 

# putting screens in widget; standard procedure
screens = [LoginWindow(name="login"),
            CreateAccountWindow(name="create"),
            MainWindow(name="mainW"), 
            SettingMain(name="settingM"), 
            SettingProfile(name="settingP"), 
            SettingNotif(name="settingN"),
            Graph(name="graph"),
            DailyGraph(name="dailygraph"),
            WeeklyGraph(name="weeklygraph"),
            MonthlyGraph(name = "monthlygraph"),
            SystemPermission(name= "systempermission"),
            UserData(name = "userdata")]

for i in screens:
    sm.add_widget(i) 


# inheriting the properties of App class from kivy library
class MyMainApp(MDApp): 
    
    # decrypting database and creating connection
    # checking whether the data table already exists in user.db.
    # If not, then creating a table, closing connection and encrypting database.
    databaseManager.creatingTable()


    # similarly initiating task manager's tasks table
    databaseManager.creatingTableTaskManager()

    # initiating database to store the users movement profile
    databaseManager.createTableStoreProfile()

  

    def build(self):
        self.theme_cls.theme_style = "Light"
        # loading my.kv file    # going to screenmanager
        return  Builder.load_file("my.kv") 
    



# if its the main file, execute the following code
if __name__ == "__main__":
    MyMainApp().run()