import socket

from Shared import packet

#changes per sender if more than one sender
MAGIC_HEX = "0x4497E"
BUFFER = 1024

def sIn():
    """returns a packet that it receives"""


def socketOut(packet):
    """sends a packet"""
    ip = socket.gethostbyname('localhost')
    destination_port = 12345
    sOut = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sOut.connect((ip, destination_port))
    sOut.send(str(packet))
    print(sOut.recv(BUFFER))
    sOut.close()


def mainLoop(queueOfPackets):
    seqNo = 0
    for packet in queueOfPackets:
        packet.setSeqno(seqNo)
        socketOut(packet)
        sIn()
        seqNo = 1 - seqNo


def main():
    data = str(raw_input("Type input: \n"))
    packetDataLength = int(raw_input("input data length (max 512): \n"))
    queueOfPackets = []
    packet.createPackets(MAGIC_HEX, queueOfPackets, data, packetDataLength, "dataPacket")
    print(queueOfPackets)
    mainLoop(queueOfPackets)


main()
