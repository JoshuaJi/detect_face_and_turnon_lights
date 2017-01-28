import numpy as np
import cv2
import time
import requests
import json

cap = cv2.VideoCapture(0)
last_status = False
light_status = False
time_on = 0
time_off = 0

print "Initialized"

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # for (x,y,w,h) in faces:
    # 	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    # Display the resulting frame
    
    # cv2.imshow('frame',frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    if len(faces) > 0 and last_status == False:
        time_on = time.time()
        last_status = True
    elif len(faces) > 0 and last_status == True:
        if time.time() - time_on > 1 and light_status == False:
            r = requests.post('http://192.168.2.41:3456/wemo', data = json.dumps({'state':'on'}), headers={'Content-Type': 'application/json'})
            print "lights on"
            time_on = 0
            light_status = True
    elif len(faces) == 0 and last_status == True:
        time_off = time.time()
        last_status = False
    else:
        if time.time() - time_off > 3 and light_status == True:
            r = requests.post('http://192.168.2.41:3456/wemo', data = json.dumps({'state':'off'}), headers={'Content-Type': 'application/json'})
            print "lights off"
            time_off = 0
            light_status = False
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()