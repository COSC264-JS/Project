import socket
import time
from Shared import packet


TIME_OUT_TIME = 0.75  # 1 second of waiting for response


class socket_pair():
    """sockets in our case always have a in and an out socket,
    so this is a class that groups them together as 1 for ease when creating pairs"""
    socket_in = None
    socket_out = None
    magicNum = 0x0000

    def __init__(self, in_port, out_port, dest_in_port):
        self.socket_in = in_socket(in_port)
        self.socket_out = out_socket(out_port, dest_in_port)

    def send_packets(self, packets):
        self.socket_out.open_connection()
        for outPacket in packets:
            receivedCorrectly = False
            while not receivedCorrectly:
                self.socket_out.send_packet(outPacket)
                receivedCorrectly = self.check_packet()

    def check_packet(self):
        received_reply = False
        timed_out = False
        timer_start = time.time()
        while not received_reply and and not timed_out:
            current_time = time.time()
            self.socket_in.search()
            if (self.socket_in.packet_in() is not None):
                received_reply = True
            elif ((current_time - timer_start) >= TIME_OUT_TIME):
                timed_out = True
        return received_reply


class out_socket():
    """is a class that defines a socket for transmitting data"""
    host_IP = '192.168.0.1'

    local_port = 0000
    destination_port = 0000

    unique_socket = None

    def __init__(self, local_port, destination_port):
        self.host_IP = socket.gethostname()
        self.local_port = local_port
        self.destination_port = destination_port

    def open_connection(self):
        self.unique_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.unique_socket.connect((self.host_IP, self.destination_port))

    def send_packet(self, outPacket):
        self.unique_socket.send(str(outPacket).encode())

    def close_connection(self):
        self.unique_socket.close()
        self.unique_socket = None


class in_socket():
    """is a class that defines a socket for transmitting data"""
    host_IP = '192.168.0.1'
    connected_to = ''
    local_port = 0000

    unique_socket = None
    connection = None

    local_buffer = 512

    next_sequence_num = 0

    string_in = ''
    packet_in = None

    def __init__(self, local_port):
        self.host_IP = socket.gethostname()
        self.local_port = local_port
        self.unique_socket = socket.socket()
        self.unique_socket.bind((self.host_IP, self.local_port))
        self.unique_socket.listen(1)

    def search(self, magicNum):
        self.packet_in = None
        self.connection, self.connected_to = self.unique_socket.accept()
        self.string_in = self.connection.recv(self.local_buffer).decode()
        packet_found = len(self.string_in) > 0
        if packet_found:
            self.packet_in = packet.createPacketFromString(self.string_in)
            if self.packet_in.magicNum == magicNum and self.packet_in.seqNo == self.next_sequence_num:
                self.next_sequence_num = 1 - self.next_sequence_num()

        self.connection.close()
        self.connected_to = ''
        self.packet_in

    def receive_packets(self):
        packets = []
        end = False
        while not end:
            self.search()
            end = self.packet_in.end
            packets.append(self.packet_in)
        return packets


def create_sockets(in_port, out_port, dest_in_port):
    new_sockets = socket_pair(in_port, out_port, dest_in_port)
    return new_sockets
