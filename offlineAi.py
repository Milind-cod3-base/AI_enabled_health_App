# improt library

import tensorflow as tf
import numpy as np
import pandas as pd
import scipy.stats as stats

# installing library
# pip install pandas

#import scipy

# python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
# python3 -m pip install tensorflow


# storing data in to dataframe

df1 = pd.read_csv("running.csv")
df2 = pd.read_csv("sitting.csv")
df3 = pd.read_csv("walking.csv")

# creating shape

segments1 = []
labels1 = []

for i in range(0, len(df1) - 600, 600):

    x = df1['Ax'].values[i: i + 600]
    y = df1['Ay'].values[i: i + 600]
    z = df1['Az'].values[i: i + 600]
    a = df1['Gx'].values[i: i + 600]
    b = df1['Gy'].values[i: i + 600]
    c = df1['Gz'].values[i: i + 600]

    label1 = stats.mode(df1['Activity'][i: i + 600])[0][0]

    segments1.append([x, y, z, a, b, c])

    labels1.append(label1)

# reshape the segments which is(list of arrays) to a list

reshaped_segments1 = np.asarray(
    segments1, dtype=np.float32).reshape(-1, 600, 6)

labels1 = np.asarray(pd.get_dummies(labels1), dtype=np.float32)

rs1 = reshaped_segments1[:280]

# dividing according to requirement

fd1 = np.split(rs1, 14, axis=0)


fd1 = np.array(fd1)

# creating shape

segments2 = []
labels2 = []

for i in range(0, len(df2) - 600, 600):

    x = df2['Ax'].values[i: i + 600]
    y = df2['Ay'].values[i: i + 600]
    z = df2['Az'].values[i: i + 600]
    a = df2['Gx'].values[i: i + 600]
    b = df2['Gy'].values[i: i + 600]
    c = df2['Gz'].values[i: i + 600]

    label2 = stats.mode(df2['Activity'][i: i + 600])[0][0]

    segments2.append([x, y, z, a, b, c])

    labels2.append(label2)

# reshape the segments which is(list of arrays) to a list

reshaped_segments2 = np.asarray(
    segments2, dtype=np.float32).reshape(-1, 600, 6)

labels2 = np.asarray(pd.get_dummies(labels2), dtype=np.float32)

rs2 = reshaped_segments2[:280]

# dividing according to requirement

fd2 = np.split(rs2, 14, axis=0)

fd2 = np.array(fd2)

# creating shape

segments3 = []
labels3 = []

for i in range(0, len(df3) - 600, 600):

    x = df3['Ax'].values[i: i + 600]
    y = df3['Ay'].values[i: i + 600]
    z = df3['Az'].values[i: i + 600]
    a = df3['Gx'].values[i: i + 600]
    b = df3['Gy'].values[i: i + 600]
    c = df3['Gz'].values[i: i + 600]

    label3 = stats.mode(df3['Activity'][i: i + 600])[0][0]

    segments3.append([x, y, z, a, b, c])

    labels3.append(label3)

# reshape the segments which is(list of arrays) to a list

reshaped_segments3 = np.asarray(
    segments3, dtype=np.float32).reshape(-1, 600, 6)

labels3 = np.asarray(pd.get_dummies(labels3), dtype=np.float32)

rs3 = reshaped_segments3[:280]

# dividing according to requirement

fd3 = np.split(rs3, 14, axis=0)

fd3 = np.array(fd3)

# input_shape = ''
# output_shape = ''
# interpreter = ''

# loading model


def Load_Model():
    global input_shape
    global output_shape
    global interpreter
    interpreter = tf.lite.Interpreter(model_path="gruMilind.tflite")
    interpreter.allocate_tensors()
    input_shape = interpreter.get_input_details()
    output_shape = interpreter.get_output_details()

# function to giving input shape


def predict(x):
    interpreter.set_tensor(input_shape[0]['index'], x)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_shape[0]['index'])
    Predicted_class = output_data
    return Predicted_class


# file to predict

def predict2():
    y = []
    for i in range(0, 14):
        x = fd2[i]
        y = predict(x)
        for i in range(0, 19):
            r = y[i]
            a = "running"
            b = "sitting"
            c = "walking"

            if r[0] > r[1]:
                if r[0] > r[2]:
                    #print(a)
                    return a
                else:
                    # print(c)
                    return c
            else:
                if r[1] > r[2]:
                    # print(b)
                    return b
                else:
                    # print(c)
                    return c



def predict3():
    y = []
    for i in range(0, 14):
        x = fd3[i]
        y = predict(x)
        for i in range(0, 19):
            r = y[i]
            a = "running"
            b = "sitting"
            c = "walking"

            if r[0] > r[1]:
                if r[0] > r[2]:
                    x = a
                else:
                    x = c
            else:
                if r[1] > r[2]:
                    x = b
                else:
                    x = c
            return x
    
# calling function


#Load_Model()

# predict function to predict activity

#predict2()
