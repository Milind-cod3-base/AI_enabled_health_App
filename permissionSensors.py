# module responsible for granting sensors and memory access to the app for android
from plyer.facades.accelerometer import Accelerometer

# function to grant access for accelerometer 
def allowAccelero():

    Accelerometer().enable()

def denyAccelero():

    Accelerometer.disable()

# function to grant access for gyrometer
def gyroAccess():
    pass


# function to grant access for memory storage 
def memoryAccess():
    pass

# function to grant access for bluetooth
def bluetooth():
    if platform == 'android':
        from android.permission import Permission

    
   