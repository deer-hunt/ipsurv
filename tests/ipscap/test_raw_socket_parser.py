from ipscap.util.raw_socket_entity import IPHeader, ICMPHeader, TCPHeader, UDPHeader
from ipscap.util.raw_socket_parser import IPHeaderParser, ICMPHeaderParser, TCPHeaderParser, UDPHeaderParser
import struct
import socket
import pytest
import re


class TestIPHeaderParser:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    @pytest.fixture
    def ip_header_parser(self):
        eth_ips = [socket.inet_aton("192.168.1.1"), socket.inet_aton("192.168.1.2")]

        return IPHeaderParser(eth_ips)

    def test_get_ip_header(self, ip_header_parser):
        sample_data = b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\xb1\xe6\xc0\xa8\x01\x01\xc0\xa8\x01\x02'
        ip_header = ip_header_parser.get_ip_header(sample_data)

        assert len(ip_header) == 20

    def test_parse(self, ip_header_parser):
        sample_data = b'\x45\x00\x00\x3c\x1c\x46\x40\x00\x40\x06\xb1\xe6\xc0\xa8\x01\x01\xc0\xa8\x01\x02'
        ip_header = ip_header_parser.parse(sample_data)

        assert ip_header.version == 4
        assert ip_header.iph_length == 20
        assert ip_header.packet_length == 60
        assert ip_header.src_ip == '192.168.1.1'
        assert ip_header.dest_ip == '192.168.1.2'
        assert ip_header.direction == 2

    def test_detect_local_ip(self, ip_header_parser):
        sample_ip_header = IPHeader()
        sample_ip_header.src_ip_int = socket.inet_aton('192.168.1.1')
        sample_ip_header.dest_ip_int = socket.inet_aton('8.8.8.8')

        direction = ip_header_parser.detect_local_ip(sample_ip_header)
        assert direction == 1

        sample_ip_header.src_ip_int = socket.inet_aton('8.8.8.8')
        sample_ip_header.dest_ip_int = socket.inet_aton('192.168.1.2')

        direction = ip_header_parser.detect_local_ip(sample_ip_header)
        assert direction == 2

    def test_get_header_parser_icmp(self, ip_header_parser):
        ip_header = IPHeader()
        ip_header.protocol = IPHeader.PROTOCOL_ICMP
        parser = ip_header_parser.get_header_parser(ip_header)
        assert isinstance(parser, ICMPHeaderParser)

    def test_get_header_parser_tcp(self, ip_header_parser):
        ip_header = IPHeader()
        ip_header.protocol = IPHeader.PROTOCOL_TCP
        parser = ip_header_parser.get_header_parser(ip_header)
        assert isinstance(parser, TCPHeaderParser)

    def test_get_header_parser_udp(self, ip_header_parser):
        ip_header = IPHeader()
        ip_header.protocol = IPHeader.PROTOCOL_UDP
        parser = ip_header_parser.get_header_parser(ip_header)
        assert isinstance(parser, UDPHeaderParser)

    def test_get_header_parser_unknown(self, ip_header_parser):
        ip_header = IPHeader()
        ip_header.protocol = 99
        with pytest.raises(Exception, match='Unknown Parser'):
            ip_header_parser.get_header_parser(ip_header)


class TestICMPHeaderParser:
    @pytest.fixture
    def ip_header(self):
        ip_header = IPHeader()

        ip_header.direction = IPHeader.DIRECTION_SEND
        ip_header.protocol = IPHeader.PROTOCOL_TCP
        ip_header.src_ip = '192.168.1.2'
        ip_header.dest_ip = '192.168.1.1'
        ip_header.iph_length = 20

        return ip_header

    def test_create_icmp_header(self):
        parser = ICMPHeaderParser()

        icmp_header = parser.create_icmp_header()

        assert isinstance(icmp_header, ICMPHeader)

    def test_parse(self, ip_header):
        parser = ICMPHeaderParser()

        mtu_data = b'\x45\x00\x00\x54\x00\xb3\x00\x00\x3b\x01\xbe\x3e\xd8\x3a\xdc\x6e\x0a\x00\x02\x0f\x00\x00\xa9\xd6'

        icmp_header = parser.parse(ip_header, mtu_data)

        assert icmp_header.icmph_length == ICMPHeader.DEFAULT_HEADER_LEN
        assert icmp_header.icmp_type == 0
        assert icmp_header.code == 0
        assert icmp_header.checksum == 43478


class TestTCPHeaderParser:
    @pytest.fixture
    def ip_header(self):
        ip_header = IPHeader()

        ip_header.direction = IPHeader.DIRECTION_SEND
        ip_header.protocol = IPHeader.PROTOCOL_TCP
        ip_header.src_ip = '192.168.1.2'
        ip_header.dest_ip = '192.168.1.1'
        ip_header.iph_length = 20

        return ip_header

    def test_create_tcp_header(self):
        parser = TCPHeaderParser()
        tcp_header = parser.create_tcp_header()
        assert isinstance(tcp_header, TCPHeader)

    def test_parse(self, ip_header):
        parser = TCPHeaderParser()
        mtu_data = b'\x45\x00\x00\x3c\x59\x38\x40\x00\x40\x06\x67\x48\x0a\x00\x02\x0f\x62\x89\x0b\xa4\xc6\x82\x00\x50\xfd\x4c\x26\xe3\x00\x00\x00\x00\xa0\x02\x72\x10\x7a\x6a\x00\x00\x02\x04\x05\xb4\x04\x02\x08\x0a\x1a\xa1\x7f\xdb\x00\x00\x00\x00\x01\x03\x03\x07'
        tcp_header = parser.parse(ip_header, mtu_data)

        assert tcp_header.src_port == 50818
        assert tcp_header.dest_port == 80
        assert tcp_header.seq_no == 4249626339
        assert tcp_header.ack_no == 0
        assert tcp_header.tcph_length == 40
        assert tcp_header.flags == 2
        assert tcp_header.window == 29200
        assert tcp_header.checksum > 0

    def test_parse_tcp_options(self):
        parser = TCPHeaderParser()
        options_data = b'\x02\x04\x05\xb4\x04\x02\x08\x0a\x1a\xa1\x7f\xdb\x00\x00\x00\x00\x01\x03\x03\x07'
        tcp_options = parser.parse_tcp_options(options_data)
        print(tcp_options)
        assert tcp_options['mss'] == 1460
        assert tcp_options['wscale'] == 7
        assert tcp_options['timestamp'] > 0
        assert 'sack' in tcp_options


class TestUDPHeaderParser:
    @pytest.fixture
    def ip_header(self):
        ip_header = IPHeader()

        ip_header.direction = IPHeader.DIRECTION_SEND
        ip_header.protocol = IPHeader.PROTOCOL_TCP
        ip_header.src_ip = '192.168.1.2'
        ip_header.dest_ip = '192.168.1.1'
        ip_header.iph_length = 20

        return ip_header

    def test_create_udp_header(self):
        parser = UDPHeaderParser()
        udp_header = parser.create_udp_header()
        assert isinstance(udp_header, UDPHeader)

    def test_parse(self, ip_header):
        parser = UDPHeaderParser()
        mtu_data = b'\x45\x00\x00\x37\x15\xf9\x40\x00\x40\x11\x08\x9f\x0a\x00\x02\x0f\x08\x08\x08\x08\xc3\x6d\x00\x35\x00\x23\x1c\x53'
        udp_header = parser.parse(ip_header, mtu_data)

        assert udp_header.src_port == 50029
        assert udp_header.dest_port == 53
        assert udp_header.udp_length == 35
        assert udp_header.checksum > 0

        payload_start = ip_header.iph_length + 8
        udp_header.payload_data = mtu_data[payload_start:]
        assert udp_header.payload_length == len(udp_header.payload_data)
