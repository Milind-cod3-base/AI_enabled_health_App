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
                            WHERE username=? """,(name,age,weight,height,job, gender, tempUser.readName()))    # validating user by the login username and only updating its details
                            
    conne.commit()
    conne.close()

    
    encryptDatabase.encrypt("users.db",key)  # encrypting using key





    