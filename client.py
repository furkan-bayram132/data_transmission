import socket

HOST = "192.168.1.104"
PORT = 9999

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((HOST, PORT))

for i in range(0,5):
    socket.send("hello from client".encode("utf-8"))

message = socket.recv(1024).decode("utf-8")

message2 = socket.recv(1024).decode("utf-8")
print(message)
print(message2 + " sdfhdusıagfysodaı")




























"""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1",9999))

#client'i bir servera bagladik yukarida .send diyince direkt o servera gonderecek mesajini yani
#serverdaki diger kisiler de gorebilecek mi?

for i in range(0,5): 
 print(client.recv(1024))
 """