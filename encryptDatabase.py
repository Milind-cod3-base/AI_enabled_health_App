import imp
from cryptography.fernet import Fernet

# function to write key into .key format file
def writeKey():  
    key =  Fernet.generate_key()
    
    # wb stands for write binary mode
    with open("key.key","wb") as key_file:
        key_file.write(key)
