# AI_enabled_health_App
This branch contains a stable built of the app only to run on the windows.
The permissions of the sensors are disabled and in databaaseManager file -> getTask function -> profile is removed from 
Gruoutput to sitting as a dummy variable “sitting”.

And in aiModel.py -> feedAI -> accelerometer.acceleration and gyroscope.rotation is disabled as widnows Machine doesnt come with movement sensors.

Also, in feedAI function -> databasemanger.Storeprofile has been disabled. 
