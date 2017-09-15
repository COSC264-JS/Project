from Shared import TCP
import os

MAGIC_N0 = 0x497E

PROGRAM_NAME = os.path.basename(__file__)[0:-3]

def getValidFile():
    file_path = input("please input the destination file: \n")
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("")
        return file_path
    print("File already exists... exiting")
    quit()


def main():
    in_port, out_port = TCP.get_port_pair(PROGRAM_NAME[0].upper())
    dest_in_port = TCP.getValidPort("C", "rin")
    file_name = getValidFile()

    socket_pair = TCP.create_sockets(in_port, out_port, dest_in_port, MAGIC_N0)
    socket_pair.receive_packets(file_name)
    socket_pair.close_sockets()


main()
