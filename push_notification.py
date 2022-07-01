
from plyer import notification  

import time
import tempUser

# import TaskManager

""" x will be the message from the user interface (UI),
 No need of connecting this from the database, 
 it will directly read from the label which has been selected by the user """

def pushNotif(task):     
    
    notification.notify(title = "Alert", message= task)
    
# pause function removed as it might not be important as I can just

# def pauseNotif():
#     pass     #Do I really need pause notification function?



# I need a snooze function or repeat notification function which will be sending notification in x number of hours
def repeatNotif(task):
    
    # reading the timer in hours. Picks 2 as default
    # or else picks the 
    notifTimer = tempUser.readNotificationTimer()

    # as sleep function takes input in seconds, converting hours into seconds
    seconds = notifTimer * 60 * 60
    
   # setting up an idefinite loop of notifications
    while True:
        # this will snooze the notification for required seconds
        time.sleep(seconds)
        
        # after snooze notification again.
        pushNotif(task)


""" One issue might occur: can other functions of app operate properly, while Notification is in sleep mode?
    to counter this issue, i can create a counter with zero which adds to after certain time and call notification function,
    like i can do this inside getTime function"""



# these functions are dummy functions which can be useful for getting the value from the ui and storing it.
# either it can store it into an empty txt file or simple call. lets see.
#def getTask(task):
    #return task

#def getTime(hours):
    #return hours

    