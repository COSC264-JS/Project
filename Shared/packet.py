import sys


class PacketInputError(Exception):
    def __init__(self, message):
        self.message = message


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
        output_sting.append(str(self.packetType))
        output_sting.append(str(self.seqNo))
        output_sting.append("{:02}".format(self.dataLen))
        output_sting.append(str(self.data))
        return "".join(output_sting)

    def generateAcknowledgement(self):
        """generates the expected acknowledgement packet"""
    
    def setSeqno(self, seqNo):
        self.seqNo = seqNo

    def getData(self):
        return self.data


def convertPacketType(packetType):
    if (packetType == "dataPacket"):
        newPacketType = 0b0
    elif (packetType == "acknowledgementPacket"):
        newPacketType = 0b1
    return newPacketType


def createPacket(magicNo, packetType, dataLen, data, seqNo=None):
    converted = convertPacketType(packetType)
    new_packet = Packet(magicNo, converted, dataLen, data, seqNo)
    return new_packet


def createPacketFromString(stringInput):
    try:
        magicNo = stringInput[0:6]
        packetType = stringInput[6]
        seqNo = stringInput[7]
        dataLen = int(stringInput[8:11])
        data = stringInput[11:11 + dataLen]
        new_packet = createPacket(magicNo, packetType, dataLen, data, seqNo)
        return new_packet
    except ValueError:
        print("Packet is invalid and does not contain the correct amount of fields")
        return ValueError


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
