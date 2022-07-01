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


# transitioning from kivy to kivymd
from kivymd.app import MDApp
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.scrollview import ScrollView

# from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd_extensions.akivymd.uix.charts import AKPieChart

import datetime
import matplotlib.pyplot as plt

# importing self made  module
import encryptDatabase
import taskManager
import tempUser
import databaseManager
import permissionSensors
import push_notification
import graphQuery

#importing GRU model
#import aiModel


# giving main window size similiar to a phone screen
Window.size= (320,500)

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

                    # using below code for transition instead of sm.current
                    self.parent.current = "mainW"
                    
                    #self.reset()
                    #sm.current = "mainW"

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
        #self.reset()  # clears everything
        self.parent.current = "create"

    # def reset(self): # resets the username and password section
    #      self.username = ""  
    #      self.password = ""
        

class CreateAccountWindow(Screen):
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    confirm = ObjectProperty(None)

    def login(self):
        #self.reset() # clears all
        self.parent.current = "login"

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
        
                self.parent.current = "login"
            
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
    
    mot1 = ObjectProperty(None)
    mot2 = ObjectProperty(None)
    mot3 = ObjectProperty(None)
    mot4 = ObjectProperty(None)

    def remindMe(self):   # logic to snooze the notifications for 5 minutes  # BUT HOW WILL ONE CAN STOP THE SNOOZE
        if self.mot1.active:
            push_notification.pushNotif("what")
        
        elif self.mot2.active:
            push_notification.pushNotif("why")

        elif self.mot3.active:
            push_notification.pushNotif("when")

        elif self.mot4.active:
            push_notification.pushNotif("we")
            

    def modelOn(self):

        # this will initiate the model which will start taking in the sensors data
        #aiModel.feedAI()
        pass
        

    # this will check out off the model     
    def modelOff(self):
        #accelerometer.disable()
        #gyroscope.disable()
        pass
    
    
    
    # logic to pause notification
    def pauseNotif(self):  
        pass

    def unpauseNotif(self):  # logic to unpause notification
        taskManager.taskNotif("Here must be the selected task from the UI")


    
    def scale(self):
        self.parent.current = "graph"

    def set(self):
        self.parent.current = "settingM"


class SettingMain(Screen):
    
    def notif(self):
        self.parent.current = "settingN"

    def prof(self):
        self.parent.current = "settingP"

    def login(self):

        # when the user will logout, the notification timer
        # will set to 2 hours(default state)
        tempUser.storeNotificationTimer(2)
        
        self.parent.current = "login"

    def back(self):
        self.parent.current= "mainW"

    
    # job of this function will not only to change the screen
    # but also to the refresh the userdata screen with the new
    # logged in user
    def disData(self): 
    
        self.parent.current = "userdata"

    # def refreshData(self):
    #     databaseManager.displayData


# settings window for adding user details
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
        
        w = self.ids["weight"].text
        h = self.ids["heigh"].text

        # j = self.ids["job"].text
        # g = self.ids["gender"].text
        # a = self.ids["age"].text

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

            
                    
        
        popup = Popup(
        title='Saved',
        content=Label(text='Your data has been saved securely'),
        size_hint = (0.5,0.5)
        )

        popup.open()



           
    
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



class Graph(Screen):
    
    def back(self):
        self.parent.current="mainW"


# inherting mdfflatlatlayout and fakerect class
class ProfileCard(MDFloatLayout, FakeRectangularElevationBehavior):
    pass

class UserCard(MDCard):
    pass

# inheriting screenmanager class properties to manage multiple screens
#class WindowManager(ScreenManager): 
#   pass

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
        s_perc= ((graphQuery.dailySitting)/ (datetime.datetime.now() - datetime.timedelta(days=1)))*100
        # percentage time spent walking in a day
        w_perc= ((graphQuery.dailyWalking)/  (datetime.datetime.now() - datetime.timedelta(days=1)))*100
        # percentage time spent running in a day
        r_perc= ((graphQuery.dailyRunning)/  (datetime.datetime.now() - datetime.timedelta(days=1)))*100
        
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
    

        



sm = ScreenManager() # instance of class

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


#kv = Builder.load_file("my.kv")
#sm.current = "login"  # default screen must be login


class MyMainApp(MDApp): # inheriting the properties of App class from kivy library
    
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
        #return sm
        return  Builder.load_file("my.kv") # loading my.kv file    # going to screenmanager
    




if __name__ == "__main__":
    MyMainApp().run()