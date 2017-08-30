import sys
import Packet
import socket

#changes per sender if more than one sender
MAGIC_HEX = "0x4497E"
BUFFER = 1024

def sIn():
    """returns a packet that it receives"""

def socketOut(packet):
    """sends a packet"""
    ip = socket.gethostname()
    destination_port = 12345
    sOut = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sOut.connect((ip, destination_port))
    sOut.send(str(packet))
    print(sOut.recv(BUFFER))
    sOut.close()

def createPackets(queueOfPackets, data, packetDataLength):
    '''Creates many packets'''
    startOfPacketData = 0
    dataLength = len(data)
    
    while (startOfPacketData <= dataLength):
        if ((startOfPacketData + packetDataLength) > (dataLength)):
            endOfPacketData = dataLength
        else:
            endOfPacketData = startOfPacketData + packetDataLength
            
        packet_data = data[startOfPacketData:endOfPacketData]
        queueOfPackets.append(createSinglePacket(packet_data, packetDataLength))
        startOfPacketData += packetDataLength
        


def createSinglePacket(packet_data, packetDataLength):
    """creates a packet"""
    return Packet.createPacket(MAGIC_HEX, "dataPacket", packetDataLength, packet_data)
    

def mainLoop(queueOfPackets):
    seqNo = 0
    
    for packet in queueOfPackets:
        packet.setSeqno(seqNo)
        socketOut(packet)
        socketIn = sIn()
        #check if there is no more sockets
        seqNo = 1 - seqNo


def main():
    data = raw_input("Type input: \n")
    packetDataLength = int(raw_input("input data length (max 512): \n"))
    queueOfPackets = []
    createPackets(queueOfPackets, data, packetDataLength)
    mainLoop(queueOfPackets)

main()