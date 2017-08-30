import sys

class packet():
    magicNum = 0x0000
    
    '''either 0b0 for dataPacket or 0b1 for acknowledgementPacket'''
    packetType = 0b0
    seqno = 0
    
    dataLen = 0
    data = ""
    
    def __init__(self, magicNum, packetType, seqno, dataLen, data):
        self.magicNum = magicNum
        self.packetType = packetType
        self.seqno = seqno
        self.dataLen = dataLen
        self.data = data
        
    
def validity_check(magicNum, packetType, seqno, dataLen, data):
    
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
        typeBinConversion = 0b0
    else:
        typeBinConversion = 0b1
    
    if (seqno != 0 and seqno != 1):
        print("incorrect seqno")

    if (dataLen > 512):
        print("incorrect data length")
    elif (sys.getsizeof(data) > dataLen):
        print ("incorrect length of data")
        
    return(typeBinConversion)
        
        
def create_packet(magicNum, packetType, seqno, dataLen, data):
    typeBinConversion = validity_check(magicNum, packetType, seqno, dataLen, data)
    
    new_packet = packet(magicNum, typeBinConversion, seqno, dataLen, data)
    return new_packet