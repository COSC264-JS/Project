from Shared import TCP
from Shared import packet
import os

MAGIC_N0 = 0x497E

PROGRAM_NAME = os.path.basename(__file__)[0:-3]


def write_data(packets):
    for new_packet in packets:
        file_name = input("Please input file name you wish to send: \n")
        if not os.path.exists(file_path):
            with open(file_name, "w") as file:
                file.write(new_packet.data)
        else:
            print("{} already exists - NOT overwriting, aborting program")
            quit()

def main():
    in_port, out_port = TCP.get_port_pair(PROGRAM_NAME[0].upper())
    dest_in_port = TCP.getValidPort("C", "rin")
    socket_pair = TCP.create_sockets(in_port, out_port, dest_in_port, MAGIC_N0)
    packets = socket_pair.receive_packets()
    write_data(packets)
    socket_pair.close_sockets()


main()
