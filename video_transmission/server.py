import cv2
import numpy as np
import pickle
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = "192.168.1.104"
PORT = 9999

server.bind((HOST, PORT))

while True:
    x = server.recvfrom(1000000)
    clientip = x[1][0]
    
    data = pickle.loads(x[0])
    
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)

    cv2.imshow("Frame",frame)

    key = cv2.waitKey(1)

    if(key == ord("q")):
        break

