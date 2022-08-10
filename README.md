# AI enabled Health Application

## What:
    This mobile application tracks and predicts current Human motion
    (sitting, walking, running) using pre-trained GRU Neural Network 
    by having access to both accelerometer and gyrometer of the device.

    If the user stays in a single position for above a certain time (decided by the user)
    a motivation task pops up as a Notification on the device.

    User enters its data into user profile settings, and this data is stored into the
    users.db database using SQL query. 

    Since data privacy is important, users.db file is encrypted using Fernet Encryption.

    Motivation task is customised based on combination of the user data profile 
    and its movement profile. Motivation Task is stored in a different database.

## How:
    Back end is built using Python and Front end is built using Kivy.

    Database management is done using SQLite3

    Encryption is done using Fernet Encryption (symmetric key)

    Python's Plyer library is used to gain access of phone's sensors.

## Platform:
    1. Android
    2. Ios

