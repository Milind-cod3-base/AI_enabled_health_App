

"""this contains a function to temporary take the user name 
and store it into the text file which could over written everytime a user logins into the app."""


def storeName(name):
    with open("tempUser.txt","w") as file:
        file.write(name)

