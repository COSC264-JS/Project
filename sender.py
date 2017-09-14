from Shared import TCP
from Shared import packet
from Shared import Formatting
import os

MAGIC_N0 = 0x497E


PROGRAM_NAME = os.path.basename(__file__)[0:-3]


def get_data():
    file_found = False
    while not file_found:
        file_name = input("Please input file name you wish to send: \n")
        try:
            with open(file_name, "r") as file:
                data = file.read()
            file_found = True
        except FileNotFoundError:
            print("{} does not exist".format(file_name))
            quit()

    return data


def getValidPort(programName, portName):
    formattedName = "{}{}{}{}".format(programName, Formatting.formats.DARKGRAY, portName, Formatting.formats.END)
    correct = False
    while not correct:
        try:
            port = int(input("Please input port for {} \n".format(formattedName)))
            if 1024 <= port <= 64000:
                correct = True
            else:
                print("{} is not between 1024 and 64000 (inclusive)".format(formattedName))

        except ValueError:
            print("{} is not an integer".format(formattedName))
    return port


def get_port_pair():
    in_port = getValidPort(PROGRAM_NAME[0].upper(), "in")
    out_port = getValidPort(PROGRAM_NAME[0].upper(), "out")
    return (in_port, out_port)


def main():
    # inputs for ports and data
    in_port, out_port = get_port_pair()
    dest_in_port = getValidPort("C", "in")
    data = get_data()
    exitFlag = False

    socket_pair = TCP.create_sockets(in_port, out_port, dest_in_port)
    socket_pair.socket_out.open_connection()
    packets = []
    packet.createPackets(MAGIC_N0, packets, data, 512, "dataPacket")
    socket_pair.send_packets(packets)


main()
