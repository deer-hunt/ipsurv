import socket
import struct
from abc import ABC

from ipscap.util.raw_socket_entity import TCPHeader, UDPHeader


class IPHeaderGenerator:
    def __init__(self):
        pass

    def generate(self, ip_header):
        version_ihl = (ip_header.version << 4) + ip_header.iph_length

        flags_fragment_offset = (ip_header.flags << 13) + ip_header.fragment_offset

        src_ip = socket.inet_aton(ip_header.src_ip)
        dest_ip = socket.inet_aton(ip_header.dest_ip)

        payload_length = len(ip_header.payload_data)

        ip_header.total_length = (ip_header.iph_length * 4) + payload_length

        header = [
            version_ihl,
            ip_header.tos,
            ip_header.total_length,
            ip_header.identification,
            flags_fragment_offset,
            ip_header.ttl,
            ip_header.protocol,
            0,
            src_ip,
            dest_ip
        ]

        byte_data = struct.pack('!BBHHHBBH4s4s', *header)

        checksum = self.calculate_checksum(byte_data)

        header[7] = checksum
        ip_header_data = struct.pack('!BBHHHBBH4s4s', *header)

        byte_data = ip_header_data + ip_header.payload_data

        return byte_data

    def calculate_checksum(self, header):
        if len(header) % 2 == 1:
            header += b'\x00'

        checksum = 0
        for i in range(0, len(header), 2):
            part = (header[i] << 8) + header[i + 1]
            checksum += part
            checksum = (checksum & 0xffff) + (checksum >> 16)

        checksum = ~checksum & 0xffff

        return checksum


class HeaderGenerator(ABC):
    def generate(self, protocol_header, src_ip=None, dest_ip=None):
        pass

    def create_pseudo_header(self, src_ip, dest_ip, protocol, total_length):
        src_ip = socket.inet_aton(src_ip)
        dest_ip = socket.inet_aton(dest_ip)
        reserved = 0

        pseudo_header = struct.pack('!4s4sBBH', src_ip, dest_ip, reserved, protocol, total_length)

        return pseudo_header

    def calculate_checksum(self, data):
        if len(data) % 2 == 1:
            data += b'\x00'

        checksum = 0
        for i in range(0, len(data), 2):
            part = (data[i] << 8) + data[i + 1]
            checksum += part
            checksum = (checksum & 0xffff) + (checksum >> 16)

        checksum = ~checksum & 0xffff
        return checksum


class ICMPHeaderGenerator(HeaderGenerator):
    def generate(self, icmp_header, src_ip=None, dest_ip=None):
        header = [
            icmp_header.type,
            icmp_header.code,
            0,
            icmp_header.identifier,
            icmp_header.sequence
        ]

        byte_data = struct.pack('!BBHHH', *header)

        checksum = self.calculate_checksum(byte_data + icmp_header.payload_data)

        header[2] = checksum
        icmp_header_data = struct.pack('!BBHHH', *header)

        byte_data = icmp_header_data + icmp_header.payload_data

        return byte_data


class TCPHeaderGenerator(HeaderGenerator):
    def generate(self, tcp_header, src_ip=None, dest_ip=None):
        if tcp_header.tcph_length <= 0:
            tcp_header.tcph_length = TCPHeader.DEFAULT_HEADER_LEN

        data_offset = tcp_header.tcph_length // 4
        offset_flags = (data_offset << 12) + (tcp_header.flags & 0x1FF)

        header = [
            tcp_header.src_port,
            tcp_header.dest_port,
            tcp_header.seq_no,
            tcp_header.ack_no,
            offset_flags,
            tcp_header.window,
            0,
            tcp_header.urgent_pointer
        ]

        byte_data = struct.pack('!HHLLHHHH', *header)

        total_length = len(byte_data) + len(tcp_header.payload_data)

        pseudo_header = self.create_pseudo_header(src_ip, dest_ip, socket.IPPROTO_TCP, total_length)

        checksum = self.calculate_checksum(pseudo_header + byte_data + tcp_header.payload_data)

        header[6] = checksum
        tcp_header_data = struct.pack('!HHLLHHHH', *header)

        byte_data = tcp_header_data + tcp_header.payload_data

        return byte_data


class UDPHeaderGenerator(HeaderGenerator):
    def create_udp_header(self):
        return UDPHeader()

    def generate(self, udp_header, src_ip=None, dest_ip=None):
        if udp_header.udph_length <= 0:
            udp_header.udph_length = UDPHeader.DEFAULT_HEADER_LEN + len(udp_header.payload_data)

        header = [
            udp_header.src_port,
            udp_header.dest_port,
            udp_header.udph_length,
            0
        ]

        byte_data = struct.pack('!HHHH', *header)

        pseudo_header = self.create_pseudo_header(src_ip, dest_ip, socket.IPPROTO_UDP, udp_header.udph_length)

        checksum = self.calculate_checksum(pseudo_header + byte_data + udp_header.payload_data)

        header[3] = checksum
        udp_header_data = struct.pack('!HHHH', *header)

        byte_data = udp_header_data + udp_header.payload_data

        return byte_data
