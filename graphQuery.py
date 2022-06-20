# this module is responsible for getting daily, weekly and monthly data access and display it on the graph widget

# import matplotlib  or kivy.matplotlib etc?

import datetime
from datetime import timedelta

# importing databaseManager module
import databaseManager


# function to scan and display  daily activity
def daily():
    
    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days= -1)

    # getting daily range from the db
    databaseManager.queryGraph(lower_limit, upper_limit)



# function to scan and display  weekly activity
def weekly():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days= -7)



# function to scan and display  monthly activity
def monthly():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = -30)