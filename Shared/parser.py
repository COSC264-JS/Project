from xml.dom import minidom


class InvalidSocketError(Exception):
    """when a socket name does not exist"""


class InvalidProgramError(Exception):
    """when a socket name does not exist"""


XML_LOCATION = 'Shared/program_information.xml'



def get_magic_num():
    document = minidom.parse(XML_LOCATION)
    return ((document.getElementsByTagName('data'))[0].attributes['magicNum'].value)


def get_socket_port(socket_name):
    document = minidom.parse(XML_LOCATION)
    sockets = (document.getElementsByTagName('socket'))
    for socket in sockets:
        if socket.attributes['name'].value == socket_name:
            return socket.attributes['port'].value
    raise InvalidSocketError


def get_program_buffer(program_name):
    document = minidom.parse(XML_LOCATION)
    programs = (document.getElementsByTagName('prog'))
    for program in programs:
        if program.attributes['name'].value == program_name:
            return program.attributes['buffer'].value
    raise InvalidProgramError
