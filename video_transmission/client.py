import cv2
import socket
import pickle
import os
import numpy as np


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

HOST = "192.168.1.104"
PORT = 9999

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

while cap.isOpened():
    ret, frame = cap.read()

    orriented_frame = cv2.flip(frame,1)
    

    success, encoded_frame = cv2.imencode('.jpg', orriented_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    
    frame_as_bytes = pickle.dumps(encoded_frame)

    cv2.imshow("Frame",orriented_frame)

    server.sendto(frame_as_bytes, (HOST, PORT))

    key = cv2.waitKey(1)
    
    if key == ord("q"):
        break

cv2.destroyAllWindows()
cap.release()