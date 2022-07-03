# this module contains the pretrained ai, this module needs to import the permissions for accelerometer and gyro from the phone
# also it needs to import permissons such as tesnorflow etc. 
import databaseManager
from plyer import accelerometer
from plyer import gyroscope
import datetime
import time




# this function contains the ai, and takes input such from accelerometer and gyro
# def gruResponse( time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z ):
    
#     """Ai goes here"""
   
   
   
   
#     #This will contain the output response of the gru after calculation, like sitting running walking
#     output = "sitting"

#     databaseManager.storeProfile(time, output)


#     # returning the output
#     return output    

# setting a global variable
GruOutput = ""


# global variable declared to resolve "local variable 'time' referenced
# before assignment"
t = time


# this function starts to feed sensors data into the ai model
def feedAI():
    # commenting below as they are already enabled in allow section
    #accelerometer.enable()
    #gyroscope.enable()

    while True:
        
        # calling global variable for time 
        global t

        # frequency of 50hz, hence setting a cycle of 0.02 seconds
        t.sleep(0.02)

        t = datetime.datetime.now()

        # gets accelerometers data in tuple format in 3 axes (x,y,z)
        #acc_x, acc_y, acc_z = accelerometer.acceleration
        
        # gets gyrometers data in tuple format in 3 axes 
        #gyr_x, gyr_y, gyr_z = gyroscope.rotation
        
        # below function will store AI output into profile database
        # and will also return output
        #gruResponse(time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z)


        """Ai goes here"""
   
   
   
    
        #This will contain the output response of the gru after calculation, like sitting running walking
        
        global GruOutput
        GruOutput = "sitting"

        #databaseManager.storeProfile(time, GruOutput)


        # returning the final output
        return GruOutput
            

# this is to set reset the GruOutpu
feedAI()