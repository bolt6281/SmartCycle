#Caution!
#this code is for linux.
#If you want to run this at window, you should change code to run successfully.
# ex) method of imporing opencv module, appoint camera number, appointing way to set path to save data .. .

'''
[ How to use ]

run this code : sudo python3 ~/SmartCycle.py

save : press 's' key
quit : press 'q' key for a while to save index data successfully.

'''


import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import time
from save_img import save_image_640

path = os.path.dirname(os.path.abspath(__file__))
location = input("where do you want to save?(assign folder)\n./")

location = path + "/" + location

if os.path.isdir(location):
    print ("The directory already exists\n")
else:
    print ("Successfully created the directory!\n")
    os.mkdir(location)
    
if os.path.isfile(location+"/saved_index.txt") == False:
    np.savetxt(location+'/saved_index.txt', [0])
index = int(np.loadtxt(location+"/saved_index.txt"))

# setting
capture = cv2.VideoCapture(-1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

#Capture
while True:
    ret, frame = capture.read()
    cv2.imshow("frame", frame) 
    
    #when press 's' : save frame
    if cv2.waitKey(1) == ord('s'):
        index = save_image_640(frame, index, location)
        
    #when press 'q' : quit
    if cv2.waitKey(1) == ord('q'):
        #save index
        np.savetxt(location+'//saved_index.txt', [index])
        #Close window
        cv2.destroyWindow("frame")
        capture.release()
        break