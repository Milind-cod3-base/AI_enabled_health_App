# this module contains the pretrained ai, this module needs to import the permissions for accelerometer and gyro from the phone
# also it needs to import permissons such as tesnorflow etc. 
import databaseManager
from plyer import accelerometer
from plyer import gyroscope
import datetime
import time

import tensorflow as tf
import numpy as np

# setting a global variable and setting it as sitting
GruOutput = "sitting"


# global variable declared to resolve "local variable 'time' referenced
# before assignment"
t = time


# this function starts to feed sensors data into the ai model
def feedAI():
   
    accelerometer.enable()
    gyroscope.enable()

    # Load TFLite model and allocate tensors
    interpreter = tf.lite.Interpreter(model_path="gruM.tflite")
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    while True:
        
        # calling global variable for time 
        global t

        # frequency of 50hz, hence setting a cycle of 0.02 seconds
        t.sleep(0.02)

        t = datetime.datetime.now()

        # gets accelerometers data in tuple format in 3 axes (x,y,z)
        [acc_x, acc_y, acc_z] = accelerometer.acceleration
        
        # gets gyrometers data in tuple format in 3 axes 
        [gyr_x, gyr_y, gyr_z] = gyroscope.rotation

         # input converted into  a single array
        gru_input = [acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z]
        # below function will store AI output into profile database
        # and will also return output
        #gruResponse(time, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z)

       
        #input_shape = input_details[0]['shape']
        
        input_data = gru_input
        #input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
        
        interpreter.set_tensor(input_details[0]['index'], input_data)
        #interpreter.set_tensor(input_details[0]['index'], input_data)

        interpreter.invoke()

        # The function `get_tensor()` returns a copy of the tensor data.
        # Use `tensor()` in order to get a pointer to the tensor.
        output_data = interpreter.get_tensor(output_details[0]['index'])
       

        #This will contain the output response of the gru after calculation, like sitting running walking
        global GruOutput
        GruOutput = output_data

        databaseManager.storeProfile(time, GruOutput)


        # returning the final output
        return GruOutput
            

# this is to set reset the GruOutpu
#feedAI()