import cv2
import socket
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_IP = "192.168.1.100" #bu ipnin sabit kalmasi lazim veya bizim bunu alabilmemiz lazim buna bak mutlaka ve sunumda soyle
PORT = 9999

client_socket.connect((HOST_IP, PORT))

data = b"" #byte array yani biz messageyi encode edince byte array oluyor
payload_size = struct.calcsize("Q") #unsigned long long int yani 8 byte yani 8 

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) #4kb buffer -> burasi buffer alis
        if not packet: break # eger empty byte array donerse yani not b"" olursa pythonda bos stringler falsy oldugundan
        #basina not koyarsan true oluyor giriyor, yani peer connectioni kapatmissa veya baglanti socketi kopmussa recv'e bos byte array geliyor ve ife girip icteki whileden cikiyor ya da data bitmisse tam sonuna denk gelmisse yine cikiyor
        data += packet #??????
    packed_message_size = data[:payload_size] # ilk 8 byte data uzunluguydu gonderdigimiz mesajda
    data = data[payload_size:] #ilki inclusive sonuncusu exclusive ?
    message_size = struct.unpack("Q", packed_message_size)[0] # unpack tupple doner so 0. elemanda bizim sizemiz
    while len(data) < message_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:message_size]
    data = data[message_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("receiving video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
client_socket.close()