

from matplotlib.pyplot import title
from plyer import notification  

import time
import tempUser

from timeloop import Timeloop
from datetime import timedelta


# reading the timer in hours from the tempNotificationTimer.txt file. Picks 2 as default.
notifTimer = int(tempUser.readNotificationTimer())

# converting hours into seconds
notifTimerSeconds = notifTimer * 60 * 60

# instance given of Timeloop class
tl = Timeloop()

# attaching tl.job with the repeatNotif function
@tl.job(interval= timedelta(seconds= notifTimerSeconds))
# I need a snooze function or repeat notification function which will be sending notification in x number of hours
def repeatNotif():
    
    # reading the temporary stored task
    get_task = tempUser.readMotivation()

    
    
    # putting the already read task into the message of a notification banner
    notification.notify(title="Alert", message=get_task)
 
# this function prevents to start the loop just after the app boot
# instead, loop only starts when the remind me button is clicked in the UI
def startTimer():
    tl.start(block=True)


    