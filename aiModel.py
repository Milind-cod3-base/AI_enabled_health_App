# this module contains the pretrained ai, this module needs to import the permissions for accelerometer and gyro from the phone
# also it needs to import permissons such as tesnorflow etc. 
import databaseManager

# this function contains the ai, and takes input such from accelerometer and gyro
def gruResponse( time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z ):
    
    #This will contain the output response of the gru after calculation, like sitting standing walking
    output = "sitting"

    databaseManager.storeProfile(time, output)


    # below code might not be needed, could be revived later when needed
    #return output    