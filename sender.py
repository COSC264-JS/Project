from Shared import TCP
from Shared import packet
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


def main():
    # inputs for ports and data
    in_port, out_port = TCP.get_port_pair(PROGRAM_NAME[0].upper())
    dest_in_port = TCP.getValidPort("C", "sin")
    data = get_data()

    socket_pair = TCP.create_sockets(in_port, out_port, dest_in_port, MAGIC_N0)
    socket_pair.socket_out.open_connection()
    packets = []
    packet.createPackets(MAGIC_N0, packets, data, 512, "dataPacket")
    socket_pair.send_packets(packets)
    socket_pair.close_sockets()


main()
