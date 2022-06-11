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
        
        # connecting to database
        conn = sqlite3.connect('login.db')

        # cursor
        c = conn.cursor()

        c.execute("""SELECT username, password FROM users""")

        items = c.fetchall() # fetching all usernames

        u = self.ids["username"].text # making instance of username and password text input
        p = self.ids["password"].text

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
        
        # connecting to database
        conn = sqlite3.connect('login.db')
        
        # create a cursor
        c = conn.cursor()
        
        # taking user data
        if self.ids["username"].text and self.ids["password"].text and self.ids["confirm"] .text is not None:

            u = self.ids["username"].text
            p = self.ids["password"].text
            co = self.ids["confirm"].text

            if p==co:  # if password and confirm password are same then only push to database


                # add a record
                c.execute("INSERT INTO users(username, password) VALUES (?,?)",(u,p))
            
                conn.commit()
                conn.close()
        
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
        pass # this will check in the model
    
    def modelOff(self):
        pass   # this will check out off the model
    
    def pauseNotif(self):  # logic to pause notification
        pass

    def unpauseNotif(self):  # logic to unpause notification
        pass

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
    w= ObjectProperty(None)
    h=ObjectProperty(None)
    j=ObjectProperty(None)
    

    # this function will save the data into the database
    def save(self):
        conne = sqlite3.connect('login.db')

        cur = conne.cursor()

        self.n = self.ids["n"].text
        self.a = self.ids["age"].text
        self.w = self.ids["weight"].text
        self.h = self.ids["heigh"].text
        self.j = self.ids["job"].text
        
        if n and a and w and h and j is not None:

            cur.execute("INSERT INTO users(name,age,weight,height,job) VALUES (?,?,?,?,?) WHERE ",(self.n,self.a,self.w,self.h,self.j))   

            conne.commit()
            conne.close()
        
        else:
            popup = Popup(
            title='Invalid Credentials',
            content=Label(text='One or more fields have been left blank.\n\nPlease fill them before pressing Submit'),
            size_hint = (0.5,0.5)
            )

            popup.open()



           
    
    def back(self):
        sm.current = "settingM"
    
    def reset(self):  # clear data
        n = ""
        age= ""
        weight=""
        height=""
        job=""
        
    
    


class SettingNotif(Screen):

    def back(self):
        sm.current = "settingM"

class Graph(Screen):
    
    def back(self):
        sm.current="mainW"



# inheriting screenmanager class properties to manage multiple screens
class WindowManager(ScreenManager): 
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
    
    conn = sqlite3.connect('login.db')
    
    c = conn.cursor()

    # Here just creating a table if it doesnt exist from before
    c.execute("""CREATE TABLE if not exists users( username, password, name, age, weight, height, job )""")  
    

    conn.commit()
    conn.close()


    def build(self):

        return sm    # going to screenmanager



if __name__ == "__main__":
    MyMainApp().run()