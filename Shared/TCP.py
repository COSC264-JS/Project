import socket
import time
from Shared import Formatting
from Shared import packet


TIME_OUT_TIME = 0.75  # 1 second of waiting for response


class socket_pair():
    """sockets in our case always have a in and an out socket,
    so this is a class that groups them together as 1 for ease when creating pairs"""
    socket_in = None
    socket_out = None

    exitFlag = False

    magicNum = 0x0000

    def __init__(self, in_port, out_port, dest_in_port, magicNum):
        self.socket_in = in_socket(in_port)
        self.socket_out = out_socket(out_port, dest_in_port)
        self.magicNum = magicNum

    def send_packets(self, packets):
        self.socket_out.open_connection()
        for packetBuffer in packets:
            receivedCorrectly = False
            while not receivedCorrectly:
                self.socket_out.send_packet(packetBuffer)
                receivedCorrectly = self.check_packet()
            del packetBuffer

    def check_packet(self):
        invalid_reply = False
        valid_reply = False
        timed_out = False
        timer_start = time.time()

        # Keep looking until a valid or invalid reply or time out.
        # Valid replies and invalid replies are not exhaustive as there can be no reply also.
        while not valid_reply and not timed_out and not invalid_reply:
            current_time = time.time()
            self.socket_in.search(self.magicNum)
            if (self.socket_in.rcvd is not None):
                valid_reply = True
            elif (self.socket_in.invalid):
                invalid_reply = True
            elif ((current_time - timer_start) >= TIME_OUT_TIME):
                timed_out = True

        return valid_reply

    def receive_packets(self):
        return self.socket_in.receive_packets(self.magicNum)

    def close_sockets(self):
        self.socket_in.close_socket()
        self.socket_out.close_socket()


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

    def close_socket(self):
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

    next = 0

    string_in = ''
    rcvd = None
    invalid = False

    def __init__(self, local_port):
        self.host_IP = socket.gethostname()
        self.local_port = local_port
        self.unique_socket = socket.socket()
        self.unique_socket.bind((self.host_IP, self.local_port))
        self.unique_socket.listen(1)

    def search(self, magicNum):
        self.rcvd = None
        self.connection, self.connected_to = self.unique_socket.accept()
        self.string_in = (self.connection.recv(self.local_buffer)).decode()
        packet_found = len(self.string_in) > 0
        if packet_found:
            self.rcvd = packet.createPacketFromString(self.string_in)
            if self.rcvd.packetType == "dataPacket":
                if self.rcvd.magicNum == magicNum and self.rcvd.seqNo == self.next:
                    self.next = 1 - self.next()
                else:
                    #invalid data
                    self.rcvd = None
                    self.invalid = True
            elif self.rcvd.packetType == "acknowledgementPacket" and self.rcvd.magicNum == magicNum and self.rcvd.seqNo == self.next:
                if self.rcvd.dataLen != 0:
                    self.rcvd = None
                    self.invalid = True
                else:
                    self.next = 1 - self.next()
            else:
                self.rcvd = None
                self.invalid = True

        self.connection.close()
        self.connected_to = ''

    def receive_packets(self, magicNum):
        packets = []
        end = False
        while not end:
            self.search(magicNum)
            while self.rcvd is not None:
                end = self.rcvd.dataLen == 0
                packets.append(self.rcvd)
        return packets

    def close_socket(self):
        self.unique_socket.close()
        self.unique_socket = None


def create_sockets(in_port, out_port, dest_in_port, magicNum):
    new_sockets = socket_pair(in_port, out_port, dest_in_port, magicNum)
    return new_sockets


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


def get_port_pair(program):
    in_port = getValidPort(program, "in")
    out_port = getValidPort(program, "out")
    return (in_port, out_port)

