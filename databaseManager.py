import sqlite3


# importing module to encrypt the database
import encryptDatabase

# importing tempUser to get the current logged in user's name
import tempUser

# this module is to create, commit and close connection with the databse


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

    for i in item:
        print(i)

    con.commit()
    con.close()
     
    # encrypting database after creating it and closing connection

    encryptDatabase.encrypt("users.db",key)


# this will get the classified movemnt profile from the output and store it into the db file
def storeProfile(time, profile):


    pass
    