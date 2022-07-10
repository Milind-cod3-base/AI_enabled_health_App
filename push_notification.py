
from matplotlib.pyplot import title
from plyer import notification  

import time
import tempUser

from timeloop import Timeloop
from datetime import timedelta


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

    
    

    notification.notify(title="Alert", message=get_task)
 

def startTimer():
    tl.start(block=True)


    