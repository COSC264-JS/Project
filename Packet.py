import sys

class packet():
    magicNum = 0x0000
    
    '''either 0b0 for dataPacket or 0b1 for acknowledgementPacket'''
    packetType = 0b0
    seqNo = None
    
    dataLen = 0
    data = ""
    
    def __init__(self, magicNum, packetType, dataLen, data, seqNo=None):
        self.magicNum = magicNum
        self.packetType = packetType
        self.dataLen = dataLen
        self.data = data
        self.seqNo = seqNo
        
    def __str__(self):
        output_sting = []
        output_sting.append(str(self.magicNum))
        output_sting.append(str(self.packetType))
        output_sting.append(str(self.dataLen))
        output_sting.append(str(self.seqNo))
        
        joiner = ","
        return joiner.join(output_sting)
    
    def setSeqno(self, seqNo):
        self.seqNo = seqNo
    
    
    
def validity_check(magicNum, packetType, dataLen, data):
    
    #typeBinConversion is a vairable that will be converted to 0 or 1 
    #for the smallest packet size
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
        
        
def createPacket(magicNum, packetType, dataLen, data ):
    typeBinConversion = validity_check(magicNum, packetType, dataLen, data)
    
    new_packet = packet(magicNum, typeBinConversion, dataLen, data)
    return new_packet