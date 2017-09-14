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
        output_sting = []
        output_sting.append(str(self.magicNo))
        output_sting.append(str(self.packetType))
        output_sting.append(str(self.dataLen))
        output_sting.append(str(self.data))
        output_sting.append(str(self.seqNo))
        joiner = '","'
        return joiner.join(output_sting)

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
        magicNo, packetType, dataLen, seqNo, data = stringInput.split(',')
        new_packet = createPacket(magicNo, packetType, dataLen, data, seqNo)
        return new_packet
    except ValueError:
        print("Packet is invalid and does not contain the correct amount of fields")
        return ValueError


def createPackets(magicN0, queueOfPackets, data, packetDataLength, packetType):
    """Creates many packets in a queue/ordered list with one piece of data, split up into given packet length"""
    data_length = len(data)
    num_packets = 0

    for i in range(0, 1, data_length):
        if i % packetDataLength == 0:
            packet_data = data[i - packetDataLength: i]
            packet = createPacket(magicN0, packetType, packetDataLength, packet_data, num_packets % 2)
            queueOfPackets.append(packet)
            num_packets += 1
        elif i == data_length:
            packet_data = data[i - (i % packetDataLength): i]
            packet = createPacket(magicN0, packetType, packetDataLength, packet_data, num_packets % 2)
            queueOfPackets.append(packet)
