

"""this contains a function to temporary take the user name 
and store it into the text file which could over written everytime a user logins into the app."""


# function to store the temporary name into the text file tempUser.txt
def storeName(name):
    with open("tempUsername.txt","w") as file:
        file.write(name)


# function to read the name of temporary user from the file tempUser.txt
def readName():
    with open("tempUsername.txt","r") as file:
        return file.read()


""" It also stores the notification timer setting given by the user
and also resets the screens at the time of logout to 2 hours so that it stays
default"""

def storeNotificationTimer(hours):
    with open("tempUsername.txt","w") as file:
        file.write(hours)

def readNotificationTimer(hours):
    with open("tempUsername.txt","r") as file:
        return file.read()