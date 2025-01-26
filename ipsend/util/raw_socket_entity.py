import re
from abc import ABC


class Header(ABC):
    def __init__(self):
        self.checksum = 0
        self.payload_length = 0
        self.payload_data = b''


class IPHeader(Header):
    PROTOCOL_ICMP = 1
    PROTOCOL_TCP = 6
    PROTOCOL_UDP = 17

    DIRECTION_SEND = 1
    DIRECTION_RECEIVE = 2

    def __init__(self):
        super().__init__()

        self.version = 4
        self.iph_length = 0
        self.tos = 0
        self.total_length = 0
        self.identification = 0
        self.flags = 0
        self.fragment_offset = 0
        self.ttl = 0
        self.protocol = 0
        self.protocol_code = None
        self.src_ip = None
        self.src_ip_int = None
        self.dest_ip = None
        self.dest_ip_int = None


class ProtocolHeader(ABC):
    def __init__(self):
        self.src_port = 0
        self.dest_port = 0

    def get_sanitized_data(self):
        return re.sub(rb'^\x00+$', b'', self.payload_data)


class ICMPHeader(Header, ProtocolHeader):
    DEFAULT_HEADER_LEN = 4

    def __init__(self):
        super().__init__()

        self.src_port = -1
        self.dest_port = -1

        self.icmp_type = 0
        self.code = 0


class TCPHeader(Header, ProtocolHeader):
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
        super().__init__()

        self.seq_no = 0
        self.ack_no = 0
        self.tcph_length = 0
        self.flags = 0
        self.flag_codes = []
        self.window = 0
        self.urgent_pointer = 0
        self.tcp_options = 0


class UDPHeader(Header, ProtocolHeader):
    DEFAULT_HEADER_LEN = 8

    def __init__(self):
        super().__init__()

        self.udph_length = 0
