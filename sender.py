import socket
from Shared import packet
from Shared import TCP
from Shared import parser
import os

PROGRAM_NAME = os.path.basename(__file__)[0:-3]

def get_data():
    data = raw_input("input data you wish to send: \n")
    return data

def check_length(length):
    try:
        length = int(length)
        if (0 < length <= 512):
            return True
        else:
            print("{} is not between 1 and 512 (inclusive)".format(length))
            return False
    except ValueError:
        print("{} is not an integer\n".format(length))
        return False



def get_data_length():
    length = raw_input("Please input desired data size per packet: (must be an integer >0 and <513)\n")
    while not check_length(length):
        length = raw_input("Please input desired data size per packet: (must be an integer >0 and <513)\n")
    return int(length)


def send_data():
    magicNum = parser.get_magic_num()
    packets = []
    data = get_data()
    packetDataLength = get_data_length()
    packetType = "dataPacket"
    packet.createPackets(magicNum, packets, data, packetDataLength, packetType)

    destinationName = "csin"
    sout = TCP.out_socket(destinationName, PROGRAM_NAME)

    sin = TCP.in_socket(parser.get_socket_port("sin"), parser.get_program_buffer(PROGRAM_NAME))

    sout.open_connection()
    sout.send_packets(packetDataLength, sin)
    sout.close_connection()


def main():
    send_data()


main()