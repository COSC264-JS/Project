import sys
import Packet
import socket

BUFFER = 1024

socket1 = socket.socket()
host  = socket.gethostname()
port = 12345
socket1.bind((host, port))

socket1.listen(5)
while True: 
    connection1, address1 = socket1.accept()
    print(socket1.recv(BUFFER))
    print("got connection from: \n", address1)
    connection1.send("thankyou for connecting")
    connection1.close()