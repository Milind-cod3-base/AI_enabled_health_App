
from matplotlib.pyplot import title
from plyer import notification  

import time
import tempUser

from timeloop import Timeloop
from datetime import timedelta

# import TaskManager

""" x will be the message from the user interface (UI),
 No need of connecting this from the database, 
 it will directly read from the label which has been selected by the user """

# def pushNotif(task):     
    
#     notification.notify(title = "Alert", message= task)
    
# pause function removed as it might not be important as I can just

# def pauseNotif():
#     pass     #Do I really need pause notification function?
#task = ""


# reading the timer in hours. Picks 2 as default
notifTimer = int(tempUser.readNotificationTimer())
notifTimerSeconds = notifTimer * 60 * 60

# instance given of Timeloop class
tl = Timeloop()

@tl.job(interval= timedelta(seconds= notifTimerSeconds))
# I need a snooze function or repeat notification function which will be sending notification in x number of hours
def repeatNotif():
    
    # reading the temporary stored task
    get_task = tempUser.readMotivation()

    #print(get_task)
    

    notification.notify(title="Alert", message=get_task)
 

def startTimer():
    tl.start(block=True)


    