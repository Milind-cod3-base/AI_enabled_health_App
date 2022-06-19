
from plyer import notification  

import time

# import TaskManager

""" x will be the message from the user interface (UI),
 No need of connecting this from the database, 
 it will directly read from the label which has been selected by the user """

def pushNotif(x):     
    
    notification.notify(title = "Alert", message= x)
    

def pauseNotif():
    pass     #Do I really need pause notification function? 


    
    
