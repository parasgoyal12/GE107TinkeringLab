from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import random
import keyboard
from tkinter import *
import os
import _thread
# tk = Tk()
# def toggle_fullscreen(state, event=None):
#     state = not state  # Just toggling the boolean
#     tk.attributes("-fullscreen", state)
#     return "break"

# def end_fullscreen(state, event=None):
#     state = False
#     tk.attributes("-fullscreen", False)
#     return "break"

# def black():
#     tk.configure(background='black')
# topFrame = Frame(tk, background = 'black')
# bottomFrame = Frame(tk, background = 'black')
# topFrame.pack(side = TOP, fill=BOTH, expand = YES)
# bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
# state = False
# tk.bind("<Return>", toggle_fullscreen(state))
# tk.mainloop()

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
                help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
                help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
check=False
while True:
    
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                 (300, 300), (104.0, 177.0, 123.0))
    
    net.setInput(blob)
    detections = net.forward()
    count = 0
    
    for i in range(0, detections.shape[2]):
        
        confidence = detections[0, 0, i, 2]
        if confidence < args["confidence"]:
            continue
        count += 1
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(frame, (startX, startY), (endX, endY),
                      (0, 255, 0), 1)
        cv2.putText(frame, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    if(count > 1):
        if check==False:
            keyboard.press_and_release('win+d')
        check = True
    
    if count<=1 and check==True:
        # print("check")
        keyboard.press_and_release('win+d')
        check = False
         
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    # print("HANS")
cv2.destroyAllWindows()
vs.stop()
