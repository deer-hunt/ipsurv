import ipaddress
import socket
import struct
from abc import ABC
from collections import OrderedDict

from ipscap.util.raw_socket_entity import IPHeader, ICMPHeader, TCPHeader, UDPHeader


class IPHeaderParser:
    def __init__(self, eth_ips=None):
        self.eth_ips = eth_ips

    def initialize(self, eth_ips):
        self.eth_ips = eth_ips

    def get_ip_header(self, data):
        return data[0:20]

    def parse(self, mtu_data, raws=False):
        ip_header = self.create_ip_header()

        ip_header.header_data = self.get_ip_header(mtu_data)

        iph = struct.unpack('!BBHHHBBH4s4s', ip_header.header_data)

        version_ihl = iph[0]

        ip_header.version = version_ihl >> 4

        ihl = version_ihl & 0xF

        ip_header.iph_length = ihl * 4

        ip_header.tos = iph[1]
        ip_header.total_length = iph[2]
        ip_header.identification = iph[3]

        flags_fragment_offset = iph[4]
        ip_header.flags = (flags_fragment_offset >> 13)
        ip_header.fragment_offset = flags_fragment_offset & 0x1FFF

        ip_header.ttl = iph[5]
        ip_header.protocol = iph[6]
        ip_header.protocol_code = IPHeader.get_protocol_code(ip_header.protocol)

        ip_header.checksum = iph[7]

        ip_header.src_ip = socket.inet_ntoa(iph[8])
        ip_header.src_ip_int = int.from_bytes(iph[8], byteorder='big')

        ip_header.dest_ip = socket.inet_ntoa(iph[9])
        ip_header.dest_ip_int = int.from_bytes(iph[9], byteorder='big')

        ip_header.direction = self.detect_direction(ip_header)
        ip_header.direction_code = IPHeader.get_direction_code(ip_header.direction)

        if raws:
            ip_header.raws = self.parse_bytes(ip_header)

        return ip_header

    def parse_bytes(self, ip_header):
        raws = {}

        hdata = ip_header.header_data

        raws['version_ihl'] = self.get_hex(hdata, 0)
        raws['total_length'] = self.get_hex(hdata, 2, 2)
        raws['identification'] = self.get_hex(hdata, 4, 2)
        raws['flags_fragment_offset'] = self.get_hex(hdata, 6, 2)
        raws['ttl'] = self.get_hex(hdata, 8)
        raws['protocol'] = self.get_hex(hdata, 9)
        raws['checksum'] = self.get_hex(hdata, 10, 2)
        raws['src_ip'] = self.get_hex(hdata, 12, 4)
        raws['dest_ip'] = self.get_hex(hdata, 16, 4)

        return raws

    def get_hex(self, header_data, begin, size=1):
        end = begin + size

        return header_data[begin:end].hex().upper()

    def detect_direction(self, ip_header):
        direction = 0

        if ip_header.src_ip_int in self.eth_ips:
            direction = IPHeader.DIRECTION_SEND
        elif ip_header.dest_ip_int in self.eth_ips:
            direction = IPHeader.DIRECTION_RECEIVE
        else:
            tip = ipaddress.ip_address(ip_header.src_ip)

            if tip.is_private:
                direction = IPHeader.DIRECTION_SEND

            tip = ipaddress.ip_address(ip_header.dest_ip)

            if tip.is_private:
                direction = IPHeader.DIRECTION_RECEIVE

        return direction

    def get_header_parser(self, ip_header):
        if ip_header.protocol == IPHeader.PROTOCOL_ICMP:
            parser = self.create_icmp_header_parser()
        elif ip_header.protocol == IPHeader.PROTOCOL_TCP:
            parser = self.create_tcp_header_parser()
        elif ip_header.protocol == IPHeader.PROTOCOL_UDP:
            parser = self.create_udp_header_parser()
        else:
            raise Exception('Unknown Parser')

        return parser

    def create_ip_header(self):
        return IPHeader()

    def create_icmp_header_parser(self):
        return ICMPHeaderParser()

    def create_tcp_header_parser(self):
        return TCPHeaderParser()

    def create_udp_header_parser(self):
        return UDPHeaderParser()


class HeaderParser(ABC):
    def parse(self, ip_header, data, raws=False):
        pass

    def get_hex(self, header_data, begin, size=1):
        end = begin + size

        return header_data[begin:end].hex()


class ICMPHeaderParser(HeaderParser):
    def create_icmp_header(self):
        return ICMPHeader()

    def parse(self, ip_header, mtu_data, raws=False):
        icmp_header = self.create_icmp_header()

        icmp_header.icmph_length = ICMPHeader.DEFAULT_HEADER_LEN
        icmph_start = ip_header.iph_length
        icmp_header.header_data = mtu_data[icmph_start:icmph_start + ICMPHeader.DEFAULT_HEADER_LEN]

        icmph = struct.unpack('!BBH', icmp_header.header_data)

        icmp_header.icmp_type = icmph[0]
        icmp_header.code = icmph[1]
        icmp_header.checksum = icmph[2]

        if raws:
            icmp_header.raws = self.parse_bytes(icmp_header)

        return icmp_header

    def parse_bytes(self, icmp_header):
        raws = {}

        hdata = icmp_header.header_data

        raws['icmp_type'] = self.get_hex(hdata, 0)
        raws['code'] = self.get_hex(hdata, 1)
        raws['checksum'] = self.get_hex(hdata, 2, 2)

        return raws


class TCPHeaderParser(HeaderParser):
    def create_tcp_header(self):
        return TCPHeader()

    def parse(self, ip_header, mtu_data, raws=False):
        tcp_header = self.create_tcp_header()

        tcph_start = ip_header.iph_length
        tcph_data = mtu_data[tcph_start:tcph_start + TCPHeader.DEFAULT_HEADER_LEN]

        tcph = struct.unpack('!HHLLHHHH', tcph_data)

        tcp_header.src_port = tcph[0]
        tcp_header.dest_port = tcph[1]
        tcp_header.seq_no = tcph[2]
        tcp_header.ack_no = tcph[3]

        offset_flags = tcph[4]

        tcp_header.tcph_length = (offset_flags >> 12) * 4
        tcp_header.flags = offset_flags & 0x1FF

        tcp_header.flag_codes = TCPHeader.get_flag_codes(tcp_header.flags)

        tcp_header.window = tcph[5]
        tcp_header.checksum = tcph[6]
        tcp_header.urgent_pointer = tcph[7]

        payload_start = ip_header.iph_length + tcp_header.tcph_length

        tcp_header.header_data = mtu_data[tcph_start:payload_start]

        options_data = tcp_header.header_data[TCPHeader.DEFAULT_HEADER_LEN:]
        tcp_header.tcp_options = self.parse_tcp_options(options_data)

        tcp_header.payload_data = mtu_data[payload_start:]
        tcp_header.payload_length = len(tcp_header.payload_data)

        if raws:
            tcp_header.raws = self.parse_bytes(tcp_header)

        return tcp_header

    def parse_tcp_options(self, data):
        pos = 0
        tcp_options = OrderedDict()

        while pos < len(data):
            kind = data[pos]

            if kind == 0:  # End of Option List
                break

            elif kind == 1:  # NOP
                tcp_options['nop'] = True
                pos += 1

            elif kind == 2:  # MSS
                tcp_options['mss'] = struct.unpack('!H', data[pos + 2:pos + 4])[0]
                pos += 4

            elif kind == 3:  # WScale
                tcp_options['wscale'] = struct.unpack('!B', data[pos + 2:pos + 3])[0]
                pos += 3

            elif kind == 4:  # SACK
                tcp_options['sack'] = True
                pos += 2

            elif kind == 8:  # Timestamp
                tsval, tsecr = struct.unpack('!II', data[pos + 2:pos + 10])
                tcp_options['timestamp'] = tsval
                pos += 10

            else:
                if pos + 1 >= len(data):
                    break

                length = data[pos + 1]

                if length < 2:
                    break

                pos += length

        return tcp_options

    def parse_bytes(self, tcp_header):
        raws = {}

        hdata = tcp_header.header_data

        raws['src_port'] = self.get_hex(hdata, 0, 2)
        raws['dest_port'] = self.get_hex(hdata, 2, 2)
        raws['seq_no'] = self.get_hex(hdata, 4, 4)
        raws['ack_no'] = self.get_hex(hdata, 8, 4)
        raws['flags'] = self.get_hex(hdata, 12, 2)
        raws['window'] = self.get_hex(hdata, 14, 2)
        raws['checksum'] = self.get_hex(hdata, 16, 2)
        raws['urgent_pointer'] = self.get_hex(hdata, 18, 2)

        return raws


class UDPHeaderParser(HeaderParser):
    def create_udp_header(self):
        return UDPHeader()

    def parse(self, ip_header, mtu_data, raws=False):
        udp_header = self.create_udp_header()

        udp_header.udph_length = UDPHeader.DEFAULT_HEADER_LEN
        udph_start = ip_header.iph_length
        udph_data = mtu_data[udph_start:udph_start + UDPHeader.DEFAULT_HEADER_LEN]

        udph = struct.unpack('!HHHH', udph_data)

        udp_header.src_port = udph[0]
        udp_header.dest_port = udph[1]
        udp_header.udp_length = udph[2]
        udp_header.checksum = udph[3]

        payload_start = ip_header.iph_length + 8

        udp_header.header_data = udph_data

        udp_header.payload_data = mtu_data[payload_start:udph_start + udp_header.udp_length]
        udp_header.payload_length = len(udp_header.payload_data)

        if raws:
            udp_header.raws = self.parse_bytes(udp_header)

        return udp_header

    def parse_bytes(self, udp_header):
        raws = {}

        hdata = udp_header.header_data

        raws['src_port'] = self.get_hex(hdata, 0, 2)
        raws['dest_port'] = self.get_hex(hdata, 2, 2)
        raws['udph_length'] = self.get_hex(hdata, 4, 2)
        raws['checksum'] = self.get_hex(hdata, 6, 2)

        return raws
