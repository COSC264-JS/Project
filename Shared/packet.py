import sys


class packet():
    magicNum = 0x0000

    # either 0 for dataPacket or 1 for acknowledgementPacket
    packetType = 0
    
    seqNo = None
    
    dataLen = 0
    data = ""

    acknowledgementPacket =

    end = False
    
    def __init__(self, magicNum, packetType, dataLen, data, seqNo, end=0):
        self.magicNum = magicNum
        self.packetType = packetType
        self.dataLen = dataLen
        self.data = data
        self.seqNo = seqNo
        self.end = end
        
    def __str__(self):
        output_sting = []
        output_sting.append(str(self.magicNum))
        output_sting.append(str(self.packetType))
        output_sting.append(str(self.dataLen))
        output_sting.append(str(self.data))
        output_sting.append(str(self.seqNo))
        output_sting.append(str(self.end))
        joiner = '","'
        return joiner.join(output_sting)

    def generateAcknowledgement(self):
        """generates the expected acknowledgement packet"""
    
    def setSeqno(self, seqNo):
        self.seqNo = seqNo

    def getData(self):
        return self.data
    

def validity_check(magicNum, packetType, dataLen, data):
    # ####################
    # #RE-WRITE THIS SAM##
    # ####################
    
    # typeBinConversion is a vairable that will be converted to 0 or 1
    # for the smallest packet size
    typeBinConversion = None
    
    try:
        int(magicNum, 16)
    except ValueError:
        print("your magic number is not a hexadecimal number")
    
    if (packetType != "dataPacket" and packetType != "acknowledgementPacket"): 
        print("invalid packetType: {0}".format(packetType))
    elif (packetType == "dataPacket"):
        typeBinConversion = 0
    else:
        typeBinConversion = 1

    if (dataLen > 512):
        print("incorrect data length")
    elif (sys.getsizeof(data) > dataLen):
        print ("incorrect length of data")
        
    return(typeBinConversion)
        
        
def createPacket(magicNum, packetType, dataLen, data, end=0, seqNo=None):
    typeBinConversion = validity_check(magicNum, packetType, dataLen, data)
    new_packet = packet(magicNum, typeBinConversion, dataLen, data, seqNo)
    return new_packet


def createPacketFromString(stringInput):
    try:
        magicNum, packetType, dataLen, seqNo, data, end = stringInput.split('","')
        new_packet = createPacket(magicNum, packetType, dataLen, data, seqNo, end)
        return new_packet
    except ValueError:
        print("packet is invalid and does not contain the correct amount of fields")
        return ValueError


def createPackets(magicNum, queueOfPackets, data, packetDataLength, packetType):
    """Creates many packets in a queue/ordered list with one peice of data, split up into given packet length"""
    startOfPacketData = 0
    dataLen = len(data)
    
    while (startOfPacketData + packetDataLength < dataLen):
        endOfPacketData = startOfPacketData + packetDataLength
        packet_data = data[startOfPacketData:endOfPacketData]
        queueOfPackets.append(createPacket(magicNum, packetType, dataLen, data))
        startOfPacketData += packetDataLength
    
    endOfPacketData = dataLen
    packet_data = data[startOfPacketData:endOfPacketData]
    queueOfPackets.append(createPacket(magicNum, packetType, dataLen, data, 1))


