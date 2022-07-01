# this module is responsible for getting daily, weekly and monthly data access and display it on the graph widget

# import matplotlib  or kivy.matplotlib etc?

import datetime
from datetime import timedelta

# importing databaseManager module
import databaseManager

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


# function to scan and display  daily activity
# def daily():
    
#     # ending of time query
#     upper_limit = datetime.datetime.now()

#     # starting of time query
#     lower_limit = datetime.datetime.now() - timedelta(days= -1)

#     # getting daily range from the db
#     databaseManager.queryGraph(lower_limit, upper_limit)

# returns only sitting values in a day
def dailySitting():
    # ending of time query
     upper_limit = datetime.datetime.now()

     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= -1)

     databaseManager.queryGraph('sitting', lower_limit,  upper_limit)
    

# returns only walking values in a day
def dailyWalking():
    # ending of time query
     upper_limit = datetime.datetime.now()

     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= -1)

     databaseManager.queryGraph('walking', lower_limit, upper_limit)

# returns only running values in a day
def dailyRunning():
    # ending of time query
     upper_limit = datetime.datetime.now()

     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= -1)

     databaseManager.queryGraph('running', lower_limit,  upper_limit)

# # function to scan and display  weekly activity
# def weekly():

#     # ending of time query
#     upper_limit = datetime.datetime.now()

#     # starting of time query
#     lower_limit = datetime.datetime.now() - timedelta(days= -7)

#     # getting weekly range from the db
#     databaseManager.queryGraph(lower_limit, upper_limit)

# returns only sitting values in a week
def weeklySitting():
    # ending of time query
     upper_limit = datetime.datetime.now()

#     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= -7)

     databaseManager.queryGraph('sitting', lower_limit,upper_limit)

# returns only walking values in a week
def weeklyWalking():
    # ending of time query
     upper_limit = datetime.datetime.now()

#     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= -7)

     databaseManager.queryGraph('walking', lower_limit,upper_limit)

# returns only running values in a week
def weeklyRunning():
    # ending of time query
     upper_limit = datetime.datetime.now()

#     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= -7)

     databaseManager.queryGraph('running', lower_limit,upper_limit)



# returns only sitting in a month
def monthlySitting():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = -30)

    # getting monthly range from the db
    databaseManager.queryGraph('sitting',lower_limit, upper_limit)

# returns only walking in a month
def monthlyWalking():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = -30)

    # getting monthly range from the db
    databaseManager.queryGraph('walking',lower_limit, upper_limit)


# returns only sitting in a month
def monthlyRunning():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = -30)

    # getting monthly range from the db
    databaseManager.queryGraph('running',lower_limit, upper_limit)

    
# below function is useful to get the graph displayed on the screen
#  def displayGraph():
#     pass