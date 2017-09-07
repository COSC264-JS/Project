import socket
import packet
import parser
import time


class out_socket():
    host_IP = '192.168.0.1'
    destination_port = 0000

    unique_socket = None

    local_buffer = 512

    # not sure how to get destination_buffer
    destination_buffer = 512

    def __init__(self, socket_name, local_name):
        self.host_IP = socket.gethostname()

        self.destination_port = int(parser.get_socket_port(socket_name))
        self.local_buffer = parser.get_program_buffer(local_name)

    def open_connection(self):
        self.unique_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.unique_socket.connect((self.host_IP, self.destination_port))

    def send_packet(self, outPacket):
        self.unique_socket.send(str(outPacket))

    def receive_acknowledgement(self, outPacket):
        """will return true if the packet have been received correctly"""
        expected = outPacket.generateAcknowledgement()
        received = self.unique_socket.recv(self.local_buffer)
        if str(expected) == str(received):
            return True
        return False

    def send_packets(self, packets, in_socket):
        self.open_connection()
        for outPacket in packets:
            receivedCorrectly = False
            while not receivedCorrectly:
                self.send_packet(outPacket)
                receivedCorrectly = check_packet(in_socket.receive_packet())

    def close_connection(self):
        self.unique_socket.close()
        self.unique_socket = None


class in_socket():
    host_IP = '192.168.0.1'
    connected_to = ''
    local_port = 0000

    acknowledgementPacket = packet.createPacket(parser.get_magic_num(), "acknowledgementPacket", 16, None)
    unique_socket = None
    connection = None

    local_buffer = 512

    # not sure how to get sender_buffer
    sender_buffer = 512

    next_sequence_num = 0

    string_in = ''
    packet_in = None


    def __init__(self, local_port, local_buffer):
        self.host_IP = socket.gethostname()
        self.local_port = local_port
        self.local_buffer = local_buffer
        self.unique_socket = socket.socket()
        self.unique_socket.bind((self.host_IP, self.local_port))
        self.unique_socket.listen(1)

    def search(self):
        self.connection, self.connected_to = self.unique_socket.accept()
        self.string_in = self.connection.recv(self.local_buffer)
        packet_found = len(self.string_in) > 0
        if packet_found:
            self.packet_in = packet.createPacketFromString(self.string_in)
            if self.packet_in.magicNum == parser.get_magic_num() and self.packet_in.seqNo == self.next_sequence_num:
                self.next_sequence_num = 1 - self.next_sequence_num()



        self.connection.close()
        self.connected_to = ''
        return(self.packet_in.data)

    def receive_packets(self):
        packets = []
        end = False
        while not end:
            self.search()
            end = self.packet_in.end
            packets.append(self.packet_in)
        return packets

def check_packet(packet):

