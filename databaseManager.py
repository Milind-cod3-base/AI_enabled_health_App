import sqlite3

from numpy import append
import aiModel

# importing module to encrypt the database
import encryptDatabase

# importing tempUser to get the current logged in user's name
import tempUser

# adding a new user via Create Account window
def addUser(user,password):
    # decrypting the database
    key = encryptDatabase.loadKey() # loading the key 
    encryptDatabase.decrypt("users.db",key)  # decrypting using key
    
    # connecting to database
    conn = sqlite3.connect('users.db')
    
    # create a cursor
    c = conn.cursor()

    
    # add a record
    c.execute("INSERT INTO data(username, password) VALUES (?,?)",(user,password))

    conn.commit()
    conn.close()

    
    encryptDatabase.encrypt("users.db",key)  # encrypting using key
    


# creating a new table if it doesnt exist already
def creatingTable():
    
    # decrypting the database
    key = encryptDatabase.loadKey() # loading the key 
    encryptDatabase.decrypt("users.db",key)  # decrypting using key

    conn = sqlite3.connect('users.db')
    
    c = conn.cursor()

    # Here just creating a table if it doesnt exist from before
    c.execute("""CREATE TABLE if not exists data( 
                username, password, name, age, weight, height, 
                job, gender )"""
                )  
    

    conn.commit()
    conn.close()


    # encrypting database after creating it and closing connection

    encryptDatabase.encrypt("users.db",key)


# checking and/or creating if tasks table doesnt exist in motivationTasks.db file
def creatingTableTaskManager():

    conn = sqlite3.connect('motivationTasks.db')
    
    c = conn.cursor()

    # Here just creating a table if it doesnt exist from before
    c.execute("""
                CREATE TABLE if not exists tasks(
                job, age, gender, movementProfile, 
                task1, task2, task3, task4)
                """
                )  
    

    conn.commit()
    conn.close()


# for storing user profile into the users.db 
def addProfile(name,age,weight,height,job,gender):
    
    # decrypting the database
    key = encryptDatabase.loadKey() # loading the key 
    encryptDatabase.decrypt("users.db",key)  # decrypting using key

    conne = sqlite3.connect('users.db')

    cur = conne.cursor()

    cur.execute("""UPDATE data 
                            SET name=?,
                            age=?, 
                            weight=?, 
                            height=?,
                            job=?,
                            gender=?
                            WHERE username=? """,(name,age,weight,height,job, gender, tempUser.readName()))    
                            # validating user by the login username and only updating its details
                            
    conne.commit()
    conne.close()

    
    encryptDatabase.encrypt("users.db",key)  # encrypting using key


# this function takes in the username and gives out three output, job, age, gender which then could be used
# for the task manager database query, along with one more parameter- movement profile (given by AI)
def taskQuery(username):
    
    # decrypting the database
    key = encryptDatabase.loadKey() # loading the key 
    encryptDatabase.decrypt("users.db",key)  # decrypting using key

    # a function to get the query for task manager, coloumns job, age, gender
    con = sqlite3.connect('users.db')

    cur = con.cursor()
    username = tempUser.readName()
    
    # checks the username and gets the required job, age, gender
    cur.execute("SELECT job, age, gender FROM data WHERE username=?", [username]) 
    

    item = cur.fetchall()

    con.commit()
    con.close()
     
    # encrypting database after creating it and closing connection

    encryptDatabase.encrypt("users.db",key)
    
    # returns a list carry a tuple of data. For ex. [('ceo', '21-30', 'male')]
    return item


# creating a table to store movement data coming from ai and time
def createTableStoreProfile():

    # create and connect a database for storing movement profile
    conn = sqlite3.connect('movementProfile.db')
    
    c = conn.cursor()

    # Here just creating a table if it doesnt exist from before
    c.execute("""
                CREATE TABLE if not exists data(
                time, profile
                )
                """
                )  
    

    conn.commit()
    conn.close()


# this will get the classified movemnt profile from the output and store it into the db file
def storeProfile(time, profile):

    # create and connect a database for storing movement profile
    conn = sqlite3.connect('movementProfile.db')
    
    c = conn.cursor()

    # Here just creating a table if it doesnt exist from before
    c.execute("""
                INSERT INTO data(time, profile) VALUES (?,?)
                """, (time, profile)

                )  
    

    conn.commit()


    conn.commit()
    conn.close()



# this function is responsible to take upper and lower limit of time 
# and give an ordered output between the range which could be called in
# graphQuery module
def queryGraph(profile, lowerLimit, upperLimit):
    
    conn = sqlite3.connect('movementProfile.db')

    c = conn.cursor()

    # getting time column between certain time_stamp range of a certain profile
    c.execute("SELECT time FROM data WHERE profile=? AND time BETWEEN ? AND ?", (profile, lowerLimit, upperLimit))


    # items will give a list which contains timestamp and profile in the form of tuples
    items = c.fetchall()
    
    c.commit()
    c.close()

    # returning here because it will end the function and connection to db can close before this
    return items



# a function to get the 4 tasks from the task manager based on the user's job, age, gender, profile
def getTask():

    # storing job, age and gender to the variables of the current user and its profile
    job, age, gender = taskQuery(tempUser.readName)[0]
    
    # this is the dummy variables, only for testing purposes
    #job, age, gender = "executive", "21-30","male"
    
    # putting this in a while loop so it keeps refreshing:
    while True:

        # for now profile is set as dummy
        # later on it will be connected with the output of the AI
       

        # here a we need to constantly check the movement profile of user and given answer accordingly
        # taking output from aimodel module using Gruoutput global variable
        profile = aiModel.GruOutput

        # dummy profile to run the app on Windows machine
        #profile = "sitting"
        
        
        # making a connection with task manager database and getting 4 tasks which will be
        # later displayed in the main screen in checkboxes
        conn = sqlite3.connect('motivationTasks.db')
        cur = conn.cursor()

        # returning four tasks based on the combination of job, age, gender, profile
        # motivationTasks.db has the tasks for every combination of user data
        cur.execute(""" SELECT task1, task2, task3, task4 FROM tasks
                        WHERE job=? AND age=? 
                        AND gender=? AND movementProfile=? """,(job, age, gender,profile))

        item = cur.fetchall()

        conn.commit()
        conn.close()
        
        # returning the 4 tasks in tuple format 
        return item[0]

# CAUTION: clear table function, it will delete the mentioned table, use with caution
def deleteTable(db):

    conn = sqlite3.connect(db)
    
    # create a cursor
    c = conn.cursor()

    
    # add a record
    c.execute("DROP TABLE data")

    conn.commit()
    conn.close()


# declaring global empty variables
userName = 'empty'
userAge = 'empty'
userWeight = 'empty'
userHeight = 'empty'
userPosition = 'empty'
userGender = 'empty'

# a function to display the userdata in the user data screen
def displayData():
    key = encryptDatabase.loadKey() # loading the key 
    encryptDatabase.decrypt("users.db",key)  # decrypting using key

    conne = sqlite3.connect('users.db')

    cur = conne.cursor()

    cur.execute("""  SELECT name, 
                            age, 
                            weight, 
                            height,
                            job,
                            gender
                            FROM data
                            WHERE username=? """,[tempUser.readName()])    
                            # validating user by the login username and only updating its details
                            
    
    items = cur.fetchall()

    
    
    global userName
    global userAge
    global userWeight
    global userHeight
    global userPosition
    global userGender

    userName = items[0][0]
    userAge = items[0][1]
    userWeight = items[0][2]
    userHeight = items[0][3]
    userPosition = items[0][4]
    userGender = items[0][5]
    
    
    
    conne.commit()
    conne.close()

    
    encryptDatabase.encrypt("users.db",key)  # encrypting using key
    

# calling this function here to use the global variable
displayData()



