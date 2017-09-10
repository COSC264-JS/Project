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
        check = self.creationCheck(magicNo, packetType, dataLen, data, seqNo)
        if check == "All Good":
            self.magicNo = magicNo
            if (packetType = "dataPacket"):
                self.packetType = 0b0
            elif (packetType = "acknowledgementPacket"):
                self.packetType = 0b1
            self.packetType = packetType
            self.dataLen = dataLen
            self.data = data
            self.seqNo = seqNo
        else:
            raise PacketInputError(check)
        
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
    

    def creationCheck(self, magicNo, packetType, dataLen, data, seqNo):
        output = "  "
        try:
            int(magicNo, 16)
        except:
            output += "magicNo, "
            
        if (packetType != "dataPacket" and packetType != "acknowledgementPacket"): 
            output += "packetType, "
                
        if ((dataLen > 512) or (dataLen != sys.getsizeof(data))):
            output += "dataLen, "
        
        if ((seqNo != 0b0) and (seqNo != 0b1)):
            output += "seqNo, "
        
        if output == "  ":
            output = "All Good"
        else:
            output = "Incorrect" + output[1:-2]
        return output
    
    def validityCheck(self, magicNo, seqNo):
        result = False
        magicNoCheck = (self.magicNo == magicNo)
        seqNoCheck = (self.seqNo == seqNo)
        dataLenCheck = (sys.getsizeof(self.data) == self.dataLen)
        if (magicNoCheck && seqNoCheck && dataLenCheck):
            result = True
        return result
            
        
        
def createPacket(magicNo, packetType, dataLen, data, seqNo=None):
    typeBinConversion = validity_check(magicNo, packetType, dataLen, data)
    new_packet = packet(magicNo, typeBinConversion, dataLen, data, seqNo)
    return new_packet


def createPacketFromString(stringInput):
    try:
        magicNo, packetType, dataLen, seqNo, data = stringInput.split(',')
        new_packet = createPacket(magicNo, packetType, dataLen, data, seqNo)
        return new_packet
    except ValueError:
        print("Packet is invalid and does not contain the correct amount of fields")
        return ValueError


def createPackets(magicNo, queueOfPackets, data, packetDataLength, packetType):
    """Creates many packets in a queue/ordered list with one piece of data, split up into given packet length"""
    startOfPacketData = 0
    dataLen = len(data)
    
    while (startOfPacketData + packetDataLength < dataLen):
        endOfPacketData = startOfPacketData + packetDataLength
        packet_data = data[startOfPacketData:endOfPacketData]
        queueOfPackets.append(createPacket(magicNo, packetType, dataLen, data))
        startOfPacketData += packetDataLength
    
    endOfPacketData = dataLen
    packet_data = data[startOfPacketData:endOfPacketData]
    queueOfPackets.append(createPacket(magicNo, packetType, dataLen, data, 1))


