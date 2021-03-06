# this module is responsible for getting daily, weekly and monthly data access and display it on the graph widget

# import matplotlib  or kivy.matplotlib etc?

import datetime
from datetime import timedelta

# importing databaseManager module
import databaseManager

#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


# returns only sitting values in a day
def dailySitting():
    # ending of time query
     upper_limit = datetime.datetime.now()

     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= 1)

     return databaseManager.queryGraph('sitting', lower_limit,  upper_limit)
    

# returns only walking values in a day
def dailyWalking():
    # ending of time query
     upper_limit = datetime.datetime.now()

     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= 1)

     return databaseManager.queryGraph('walking', lower_limit, upper_limit)

# returns only running values in a day
def dailyRunning():
    # ending of time query
     upper_limit = datetime.datetime.now()

     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= 1)

     return databaseManager.queryGraph('running', lower_limit,  upper_limit)

# returns only sitting values in a week
def weeklySitting():
    # ending of time query
     upper_limit = datetime.datetime.now()

#     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= 7)

     return databaseManager.queryGraph('sitting', lower_limit,upper_limit)

# returns only walking values in a week
def weeklyWalking():
    # ending of time query
     upper_limit = datetime.datetime.now()

#     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= 7)

     return databaseManager.queryGraph('walking', lower_limit,upper_limit)

# returns only running values in a week
def weeklyRunning():
    # ending of time query
     upper_limit = datetime.datetime.now()

#     # starting of time query
     lower_limit = datetime.datetime.now() - timedelta(days= 7)

     return databaseManager.queryGraph('running', lower_limit,upper_limit)



# returns only sitting in a month
def monthlySitting():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = 30)

    # getting monthly range from the db
    return databaseManager.queryGraph('sitting',lower_limit, upper_limit)

# returns only walking in a month
def monthlyWalking():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = 30)

    # getting monthly range from the db
    return databaseManager.queryGraph('walking',lower_limit, upper_limit)


# returns only sitting in a month
def monthlyRunning():

    # ending of time query
    upper_limit = datetime.datetime.now()

    # starting of time query
    lower_limit = datetime.datetime.now() - timedelta(days = 30)

    # getting monthly range from the db
    return databaseManager.queryGraph('running',lower_limit, upper_limit)

