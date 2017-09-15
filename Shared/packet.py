import sys

class Packet():
    magicN0 = 0x0000

    # either 0 for dataPacket or 1 for acknowledgementPacket
    packetType = 0b0
    
    seqNo = None
    
    dataLen = 0
    data = ""

    def __init__(self, magicN0, packetType, dataLen, data, seqNo):
        self.magicNo = magicN0
        self.packetType = packetType
        self.dataLen = dataLen
        self.data = data
        self.seqNo = seqNo

    def __str__(self):
        output_sting = list()
        output_sting.append(str(self.magicNo))
        output_sting.append(str(convertPTB(str(self.packetType))))
        output_sting.append(str(self.seqNo))
        output_sting.append("{:02}".format(self.dataLen))
        output_sting.append(str(self.data))
        return "".join(output_sting)

    def setSeqno(self, seqNo):
        self.seqNo = seqNo

    def getData(self):
        return self.data


def convertBTP(packetType):
    """0b0 is a dataPacket, 0b1 is acknowledgementPacket"""
    if (packetType == 0b0):
        newPacketType = "dataPacket"
    elif (packetType == 0b1):
        newPacketType = "acknowledgementPacket"
    else:
        newPacketType = "corrupt"
    return newPacketType


def convertPTB(packetType):
    """0b0 is a dataPacket, 0b1 is acknowledgementPacket"""
    newPacketType = "corrupt"
    if (packetType == "dataPacket"):
        newPacketType = 0b0
    elif (packetType == "acknowledgementPacket"):
        newPacketType = 0b1
    return newPacketType


def createPacket(magicNo, packetType, dataLen, data, seqNo=None):
    new_packet = Packet(magicNo, packetType, dataLen, data, seqNo)
    return new_packet


def createPacketFromString(stringInput):
    magicNo = hex(int(stringInput[0:5]))
    packetType = stringInput[5]
    # allows for errors to be caught later if packet type has been corrupted
    packetType = convertBTP(packetType)
    seqNo = stringInput[6]
    dataLen = int(stringInput[7:10])
    data = stringInput[10:10 + dataLen]
    new_packet = createPacket(magicNo, packetType, dataLen, data, seqNo)
    return new_packet


def createPackets(magicN0, queueOfPackets, data, maxPacketDataLength, packetType):
    """Creates many packets in a queue/ordered list with one piece of data, split up into given packet length"""
    data_length = len(data)
    number_of_packets = 0
    packet_data = ""

    for i in range(0, data_length, 1):
        packet_data_size = sys.getsizeof(packet_data)
        if packet_data_size < maxPacketDataLength:
            packet_data += str(data)[i]
        else:
            if packet_data_size > maxPacketDataLength:
                i -= 1
                packet_data = str(packet_data)[:-1]
                packet_data_size = sys.getsizeof(packet_data)
            packet = createPacket(magicN0, packetType, packet_data_size, packet_data, number_of_packets % 2)
            queueOfPackets.append(packet)
            number_of_packets += 1
            packet_data = ""

    packet = createPacket(magicN0, packetType, 0, packet_data, number_of_packets % 2)
    queueOfPackets.append(packet)


def appendToFile(inPacket, fileName):
    with open(fileName, "a") as file:
        file.write(inPacket.data)
