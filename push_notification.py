
from plyer import notification  

import time

# import TaskManager

def pushNotif(x):     # x will be the message from Task Manager
    
    notification.notify(title = "Alert", message= x)
    

def pauseNotif():
    pass     #Do I really need pause notification function? 


    
    
