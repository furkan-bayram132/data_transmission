import cv2
import struct
import pickle
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_IP = socket.gethostbyname(socket.gethostname())
PORT = 9999
server_socket.bind((HOST_IP, PORT))

server_socket.listen()
print("listenin for incoming connections")

while True:
    #bunun blocklamasi gerekiyor cunku asagidaki islemleri client_sockete bagliymis gibi yapiyoruz
    #gerci hata donmez if client_socket dedigimizden
    #ama zaten amacimiz bir cliente baglanmaksa ona baglanmadan bir seyler yapmak zaten mantiksiz
    #yapcaksan beklemeye girmeden yap client baglaninca bir seyler yapmak serverin isi
    client_socket, address = server_socket.accept()
    print("got connection from ", address)
    
    #asagida q'ya basarsak client_socketi kapatiyoruz iste o zaman daha buraya girmicek
    if client_socket:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            #once imencode ile jpgye cevirmem lazim sonra pickle dumps
            #son parametreyi incele
            frame = cv2.flip(frame,1)
            result,jpgframe = cv2.imencode(".jpg",frame,[int(cv2.IMWRITE_JPEG_QUALITY), 90])
            pickledframe = pickle.dumps(jpgframe)
            #L 4 byte integer icin, Q 8 byte integer icin
            message = struct.pack("Q", len(pickledframe)) + pickledframe 
            print("len message : " + str(len(message)))
            #tcp burada verinin tamami gidene kadar threadi blockladigi icin video akisi cok yavas oluyor
            #udp gibi yollayip bloklamayan bir protokol lazim ya da burada veriyi sendall yerine kucuk kucuk 
            #gonderebilmek lazim
            try:
                client_socket.sendall(message)
            except: #buraya giriyorsa client baglantisini koparmistir
                cap.release()
                cv2.destroyAllWindows()
                break

            cv2.imshow("transmitting video", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("d"):
                cap.release()
                cv2.destroyAllWindows()
                client_socket.close()
                break
