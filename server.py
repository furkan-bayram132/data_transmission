import socket

host = socket.gethostbyname(socket.gethostname())
#sadece bu computerdan baglanmak istiyorsak local host kullanabiliyoruz anladigim kadariyla 
#local hostu arastir 
#ama eger bir lan olusturmak istiyorsam veya diger bilgisayalarin bana internetten baglanabilemesini
#istiyorsam local host yerine local ip addressi kullanmam gerekiyor
#ipv4 nedir
HOST = "192.168.1.104" #local ip address
PORT = 9999

#bu socket sadece baglanti isteklerini acceptlemek icin 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))

#tam anlamadim
server.listen(5)

while True:
    #baglandigimiz cihazlarla konusabilmek icin her baglantiya bir socket atiyoruz
    #iste bu socketler araciligiyla her cihazla ayri ayri konusuyoruz
    print("buraya girdi")
    communication_socket, address = server.accept()
    print(f"connected to {address}")
    #1024 byte ne anlama geliyor
    message = communication_socket.recv(1024).decode("utf-8")
    print(f"message from client : {message}")
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    communication_socket.send("hello from server".encode("utf-8"))
    #communication_socket.close()
    print(f"connection with {address} ended")









































"""
#socket turu olarak interneti kullaniyoruz (1.parametre)
#2.parametre ise tcp protokolunu kullaniyoruz
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#we want to bind the server to a specific address now 
#0.0.0.0 otomatik olarak bu bilgisayari server olarak dusunup bu bilgisayarin ip adresini alır ve
#9999 numarali porta baglar
server.bind(("0.0.0.0", 9999))

#ayni anda porta 5 tane baglanti kabul edilebilir
server.listen(5)

while True:
    #addr is the address of the client that is connected to the server
    #client direkt client instancesi boylece o client ile communicate edebiliriz
    client,addr = server.accept()
    #we are gonna receive a 1024 bytes messsage, decode it and then print it 
    print(client.recv(1024).decode())
    #clienteye bir mesaj gonderecez mesaji sifreleyip yani encode edip gondermemiz gererkiyor? neden
    client.send("hello from server".encode())
    """