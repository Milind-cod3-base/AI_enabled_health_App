from cryptography.fernet import Fernet

# function to write key into .key format file
def writeKey():  
    key =  Fernet.generate_key()
    
    # wb stands for write binary mode
    with open("key.key","wb") as key_file:
        key_file.write(key)

# function to loadkey from the .key file
def loadKey():

    # reading file using rb mode or read binary mode
    return open("key.key","rb").read()  


# function to encrypt the data of a file using key
def encrypt(filename, key):
    f = Fernet(key)

    # to open a file
    with open(filename, "rb") as file:

        # to read a file content and store it
        file_data = file.read() 
    
    # encrypting data
    encrypted_data = f.encrypt(file_data)

    # overwriting the new encrypted data into the original file
    with open(filename, "wb") as file:
        file.write(encrypted_data)