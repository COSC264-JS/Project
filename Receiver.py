import socket

from Shared import packet

BUFFER = 1024

socket1 = socket.socket()
host = socket.gethostbyname('localhost')
port = 12345
finished = False
socket1.bind((host, port))

socket1.listen(5)
while not finished:
    connection1, address1 = socket1.accept()
    inString = connection1.recv(BUFFER)
    if len(inString) > 0:
        try:
            inPacket = packet.createPacketFromString(inString)
            print(inPacket.data)
            if inPacket.end == 1:
                finished = True
        except ValueError:
            # this is where the acknowledgement packet is returned
            connection1.send("000")
    connection1.close()

def main_loop():
    while True:


def main():
    main_loop()
