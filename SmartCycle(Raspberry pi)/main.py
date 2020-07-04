#-*- coding: utf-8 -*-

# This program must be run every time the computer is turned on.

# 1 : server -(sign)> pi -(image)> server -(how to recycle))> NUGU
# 2 : android -(sign)> server -(sign))> pi -(decoded QRcode)> server -(how to recycle)> android

import time
import numpy as np
from pyzbar import pyzbar
import cv2
import requests
from post import post
import websocket
import sys
import queue
import threading

# declare camera installation class
class VideoCapture:
  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(cv2.CAP_PROP_BUFFERSIZE,3)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)
    #self.cap.set(cv2.CAP_PROP_FPS, )
    self.q = queue.Queue()
     
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # Algorithm what discard all (buffer)images except latest one from camera.
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # 버리기
        except queue.Empty:
          pass
      self.q.put(frame)
      
  def read(self):
    return self.q.get()


# setting - set server ip / port
own_id = "test"
server = "ws://smartcycle.ljhnas.com:8080/" + own_id

# setting - http request
url = 'http://smartcycle.ljhnas.com:80/picture/send' # where to send

websocket.enableTrace(True)

# run camera
capture = VideoCapture(-1) #should be -1 if device is raspberry pi

while True: # repeat this series
    try:
        # socket connection
        ws = websocket.WebSocket()
        ws.connect(server)

    except websocket._exceptions.WebSocketConnectionClosedException:
        print("\n-------------------------------\nserver is closed now.\nretry it after 3 seconds . . .\n-------------------------------\n")
        time.sleep(3)
        continue

    except ConnectionRefusedError:
        print("\n-------------------------------\nserver is closed now.\nretry it after 3 seconds . . .\n-------------------------------\n")
        time.sleep(3)
        continue

    print("\n\n------------------------\nconnected!\n------------------------\n\n")

    while True:

        try:
            a = ws.recv()

        except websocket._exceptions.WebSocketConnectionClosedException:
            print("\n-------------------------------\nserver is closed now.\nretry it after 3 seconds . . .\n-------------------------------\n")
            #retry after 3 secs.
            time.sleep(3)
            break

        except ConnectionRefusedError:
            print("\n-------------------------------\nserver is closed now.\nretry it after 3 seconds . . .\n-------------------------------\n")
            time.sleep(3)
            break

        if a == "1": # capture image and send what I captured to Server
            print("\nimage request has been arrived from server!\n")
            # capture
            frame = capture.read()
            # post it
            post(frame, url, own_id, is_image = True)
            print("\nimage has been sent successfully!\n")
            break

        elif a == "2": # capture QR code and send what I read to Server
            while True: # get image until captured QRcode is decoded successfully
                print("\nQR Code request has been arrived from server!\n")
                ret, frame = capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                decoded = pyzbar.decode(gray)
                if decoded == []:
                    continue
                else: # decode QRcode and post it
                    data = str(decoded[0][0])[2:-1]
                    print("\nQRcode data has been sent successfully!\n")
                    post(data, url, own_id, is_image=False)
                    break

        else:
            print("\n-----------------unexpected signal received!-----------------\n")
            print("signal =", a,"\ntype of signal =", type(a),"\n")

        