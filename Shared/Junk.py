from Shared import packet
import codecs

file_name = "/home/jamie/Documents/Code/COSC264/Try 3/Project/Shared/testdata.txt"
with open(file_name, "r") as file:
    data = file.read()

packets = []

packet.createPackets(0x497E, packets, data, 512, "dataPacket")

for new_packet in packets:
    print(str(new_packet))
