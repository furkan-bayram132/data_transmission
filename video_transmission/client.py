import cv2
import socket
import pickle
import struct

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_IP = "192.168.1.104" #bu ipnin sabit kalmasi lazim veya bizim bunu alabilmemiz lazim buna bak mutlaka ve sunumda soyle
PORT = 9999

client_socket.connect((HOST_IP, PORT))

data = b"" #byte array yani biz messageyi encode edince byte array oluyor
payload_size = struct.calcsize("Q") #unsigned long long int yani 8 byte yani 8 

while True:
    #burada en az payload size yani 8 bytelik veri aliyoruz 
    #bir framenin boyutu 900000 falanken neden biz en az bi 8 byte al diyoruz?
    #cunku gonderdigimiz datanin ilk 8 bytesi framenin boyutunu veriyor
    #sonraki operasyonlarimiza devam edebilmemiz icin hali hazirda sahip oldugumuz framenin boyutunu bilmek zorundayiz
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024) #4kb buffer -> burasi buffer alis
        if not packet: break #
        data += packet #??????

    #iste burada gordugumuz gibi yukardan el ettigimiz datadan en az bir 8 byte veri gelmis olmasi lazimdi
    #ki biz bu 8 byteyi alalim ve framenin boyutunu ogrenelim
    packed_message_size = data[:payload_size] 
    #biz yukardan 4096 byte veri almistik yani bir framenin cok kucuk bir bolumu
    data = data[payload_size:] #iste o datanin cok kucuk bir bolumunu sonra uzerine eklemek uzere burada data'ya
    #atamaya basladik
    message_size = struct.unpack("Q", packed_message_size)[0] # unpack tupple doner so 0. elemanda bizim sizemiz
    #data boyu o mesajin sizesinden kucukse yani mesajin tamami daha gelmemisse
    while len(data) < message_size:
        #4kblik veriler halinde aliyoruz datamizi
        data += client_socket.recv(4*1024)
    #ayni frameye ait olan kismi frame_data olarak aliyoruz
    frame_data = data[:message_size]
    #hani paso 4096 byte veri geliyordu ya atiyorum yukardaki looptan gelen son 4096 byte
    #verinin 4090'i o veriye aitti bu demek oluyor ki sondaki 6 byte veri diger frameye ait
    #iste o 6 byteyi data'ya ilettik
    data = data[message_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("receiving video", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
client_socket.close()