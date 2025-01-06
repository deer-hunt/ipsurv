import re
from abc import ABC


class IPHeader:
    PROTOCOL_ICMP = 1
    PROTOCOL_TCP = 6
    PROTOCOL_UDP = 17

    DIRECTION_SEND = 1
    DIRECTION_RECEIVE = 2

    @classmethod
    def get_protocol_code(cls, protocol):
        if protocol == IPHeader.PROTOCOL_ICMP:
            code = 'ICMP'
        elif protocol == IPHeader.PROTOCOL_TCP:
            code = 'TCP'
        elif protocol == IPHeader.PROTOCOL_UDP:
            code = 'UDP'
        else:
            code = 'UNKNOWN'

        return code

    @classmethod
    def get_protocol(cls, code):
        protocol = 0

        if code == 'ICMP':
            protocol = IPHeader.PROTOCOL_ICMP
        elif code == 'TCP':
            protocol = IPHeader.PROTOCOL_TCP
        elif code == 'UDP':
            protocol = IPHeader.PROTOCOL_UDP

        return protocol

    @classmethod
    def get_direction_code(cls, direction):
        if direction == IPHeader.DIRECTION_SEND:
            code = 'SEND'
        elif direction == IPHeader.DIRECTION_RECEIVE:
            code = 'RECEIVE'
        else:
            code = 'UNKNOWN'

        return code

    def __init__(self):
        self.header_data = b''

        self.version = 4
        self.iph_length = 0
        self.flags = 0
        self.ttl = 0
        self.packet_length = 0
        self.protocol = 0
        self.protocol_code = None
        self.src_ip = None
        self.src_ip_int = None
        self.dest_ip = None
        self.dest_ip_int = None

        self.direction = 0
        self.direction_code = None


class ProtocolHeader(ABC):
    def __init__(self):
        self.header_data = b''

        self.src_port = 0
        self.dest_port = 0

        self.payload_length = 0
        self.payload_data = b''

    def get_sanitized_data(self):
        return re.sub(rb'^\x00+$', b'', self.payload_data)


class ICMPHeader(ProtocolHeader):
    DEFAULT_HEADER_LEN = 4

    def __init__(self):
        super().__init__()

        self.src_port = -1
        self.dest_port = -1

        self.icmp_type = 0
        self.code = 0
        self.checksum = 0


class TCPHeader(ProtocolHeader):
    DEFAULT_HEADER_LEN = 20

    FLAG_FIN = 1
    FLAG_SYN = 2
    FLAG_RST = 4
    FLAG_PSH = 8
    FLAG_ACK = 16
    FLAG_URG = 32
    FLAG_ECE = 64
    FLAG_CWR = 128

    @classmethod
    def get_flag_codes(cls, flags):
        flag_codes = []

        if flags & TCPHeader.FLAG_FIN:
            flag_codes.append('FIN')

        if flags & TCPHeader.FLAG_SYN:
            flag_codes.append('SYN')

        if flags & TCPHeader.FLAG_RST:
            flag_codes.append('RST')

        if flags & TCPHeader.FLAG_PSH:
            flag_codes.append('PSH')

        if flags & TCPHeader.FLAG_ACK:
            flag_codes.append('ACK')

        if flags & TCPHeader.FLAG_URG:
            flag_codes.append('URG')

        if flags & TCPHeader.FLAG_ECE:
            flag_codes.append('ECE')

        if flags & TCPHeader.FLAG_CWR:
            flag_codes.append('CWR')

        return flag_codes

    @classmethod
    def get_flags(cls, codes):
        flags = 0

        if 'FIN' in codes:
            flags |= TCPHeader.FLAG_FIN

        if 'SYN' in codes:
            flags |= TCPHeader.FLAG_SYN

        if 'RST' in codes:
            flags |= TCPHeader.FLAG_RST

        if 'PSH' in codes:
            flags |= TCPHeader.FLAG_PSH

        if 'ACK' in codes:
            flags |= TCPHeader.FLAG_ACK

        if 'URG' in codes:
            flags |= TCPHeader.FLAG_URG

        if 'ECE' in codes:
            flags |= TCPHeader.FLAG_ECE

        if 'CWR' in codes:
            flags |= TCPHeader.FLAG_CWR

        return flags

    def __init__(self):
        self.src_port = 0
        self.dest_port = 0
        self.seq_no = 0
        self.ack_no = 0
        self.tcph_length = 0
        self.flags = 0
        self.flag_codes = []
        self.window = 0
        self.checksum = 0
        self.tcp_options = None


class UDPHeader(ProtocolHeader):
    DEFAULT_HEADER_LEN = 8

    def __init__(self):
        self.src_port = 0
        self.dest_port = 0
        self.udph_length = 0
        self.checksum = 0
