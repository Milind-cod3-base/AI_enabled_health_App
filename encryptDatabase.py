""" 
    This module is responsible for creating a new Fernet key,
    loading the created key from the key.key file, 
    decrypt and encrypt the data base using same key.

"""




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


# function to decrypt the databse
def decrypt(filename, key):

    f= Fernet(key)

    with open(filename,"rb") as file:

        # read encrypted data
        encrypted_data = file.read()

    # decrypt data
    decrypted_data = f.decrypt(encrypted_data) 

    # overwrite the original databse
    with open(filename,"wb") as file:
        file.write(decrypted_data)