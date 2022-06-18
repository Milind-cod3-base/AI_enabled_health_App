import sqlite3

# importing module to encrypt the database
import encryptDatabase

import tempUser

# this module is to create, commit and close connection with the databse


# adding a new user via Create Account window
def addUser():
    pass


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
