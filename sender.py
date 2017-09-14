from Shared import TCP
from Shared import packet
from Shared import Formatting
import os

MAGIC_N0 = 0x497E


PROGRAM_NAME = os.path.basename(__file__)[0:-3]


def get_data():
    file_name = input("Please input file name you wish to send: \n")
    with open(file_name, "r") as file:
        data = file.read()

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
    length = input("Please input desired data size per packet: (must be an integer >0 and <513)\n")
    while not check_length(length):
        length = input("Please input desired data size per packet: (must be an integer >0 and <513)\n")
    return int(length)


#def send_data():

def getValidPort(programName, portName):
    formattedName = "{}{}{}{}".format(programName, Formatting.formats.DARKGRAY, portName, Formatting.formats.END)
    correct = False
    while not correct:
        try:
            port = int(input("Please input port for \n".format(formattedName)))
            if 1024 <= in_port <= 64000:
                correct = True
            else:
                print("{} is not between 1024 and 64000 (inclusive)".format(formattedName))

        except ValueError:
            print("{} is not an integer".format(formattedName))
    return port


def get_ports():
    in_port = getValidPort(PROGRAM_NAME[0], "in")
    out_port = getValidPort(PROGRAM_NAME[0], "out")
    return (in_port, out_port)


def main_loop():
    in_port, out_port = get_ports()

    in_socket = TCP.createIn(in_port)
    out_socket = TCP.createOut(out_port)

    out_socket.open_connection()



    packets = []
    data = get_data()
    packet.createPackets(MAGIC_N0, packets, data, 10, "dataPacket")


    for currentPacket in packets:
        print("hi")



def main():
    main_loop()


main()