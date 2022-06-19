# this module is responsible for getting daily, weekly and monthly data access and display it on the graph widget

# import matplotlib  or kivy.matplotlib etc?

import datetime

from datetime import timedelta


# function to scan and display  daily activity
def daily():
    
    # ending of time 
    upper_limit = datetime.datetime.now()
    
    # starting of time
    lower_limit = datetime.datetime.now() - timedelta(days= -1)
