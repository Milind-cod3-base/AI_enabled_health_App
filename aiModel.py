# this module contains the pretrained ai, this module needs to import the permissions for accelerometer and gyro from the phone
# also it needs to import permissons such as tesnorflow etc. 
import databaseManager
from plyer import accelerometer
from plyer import gyroscope
import datetime

# this function contains the ai, and takes input such from accelerometer and gyro
def gruResponse( time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z ):
    
    #This will contain the output response of the gru after calculation, like sitting standing walking
    output = "sitting"

    databaseManager.storeProfile(time, output)


    # below code might not be needed, could be revived later when needed
    #return output    




# this function starts to feed sensors data into the ai model
def feedAI():
    accelerometer.enable()
    gyroscope.enable()

    while True:

        time = datetime.datetime.now()

        # gets accelerometers data in tuple format in 3 axes (x,y,z)
        acc_x, acc_y, acc_z = accelerometer.acceleration
        
        # gets gyrometers data in tuple format in 3 axes 
        gyr_x, gyr_y, gyr_z = gyroscope.rotation
        
        gruResponse(time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z)