import pytest
import sys

if sys.platform.startswith('win'):
    pytest.mark.skip('Skipping Windows')

from ipscap.util.raw_socket_entity import IPHeader, TCPHeader
from ipscap.service.packet_filter import PacketFilter
from ipscap.util.evaluation_parser import EvaluationParser
from ipscap.configs import Config


class TestPacketFilter:
    @pytest.fixture
    def packet_filter(self):
        ev_parser = EvaluationParser({})

        packet_filter = PacketFilter(ev_parser)

        return packet_filter

    @pytest.fixture
    def ip_header(self, mocker):
        ip_header = mocker.Mock(spec=IPHeader)
        ip_header.direction = IPHeader.DIRECTION_SEND
        ip_header.protocol = IPHeader.PROTOCOL_TCP
        ip_header.src_ip = '192.168.1.2'
        ip_header.dest_ip = '192.168.1.1'
        ip_header.ttl = 64

        return ip_header

    @pytest.fixture
    def protocol_header(self, mocker):
        protocol_header = mocker.Mock(spec=TCPHeader)
        protocol_header.src_port = 12345
        protocol_header.dest_port = 80
        protocol_header.payload_length = 10
        protocol_header.payload_data = b'data data '

        protocol_header.seq_no = 999
        protocol_header.ack_no = 999
        protocol_header.tcph_length = 20
        protocol_header.flags = 31
        protocol_header.window = 10
        protocol_header.tcp_options = {'mss': 1000, 'wscale': 7, 'sack': True}

        return protocol_header

    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.fixed_protocols = [IPHeader.PROTOCOL_TCP]
        args.fixed_ips = ['192.168.1.1', '192.168.1.2']
        args.fixed_ports = [80, 12345]
        args.tracking = True
        args.find = None
        args.find_case_sensitive = False
        args.find_hex = None
        return args

    def test_verify_capture(self, packet_filter, ip_header, protocol_header, args):
        is_capture = packet_filter.verify_capture(ip_header, protocol_header, args)
        assert is_capture is True

    def test_is_tracking_transfer(self, packet_filter, ip_header):
        packet_filter.trackings.append((ip_header.src_ip, ip_header.dest_ip, 80))
        assert packet_filter._is_tracking_transfer(ip_header, 80) is True

    def test_filter_packet(self, packet_filter, ip_header, protocol_header, args):
        assert packet_filter.filter_packet(ip_header, protocol_header, args) is True

    def test_verify_protocol(self, packet_filter, ip_header, args):
        assert packet_filter.verify_protocol(ip_header, args) is True

    def test_verify_ip(self, packet_filter, ip_header, args):
        assert packet_filter.verify_ip(ip_header, args) is True

    def test_verify_port(self, packet_filter, protocol_header, args):
        assert packet_filter.verify_port(protocol_header, args) is True

    def test_verify_find(self, packet_filter, ip_header, protocol_header, args):
        args.find = 'data'
        assert packet_filter.verify_find(ip_header, protocol_header, args) is True

    def test_verify_condition(self, packet_filter, ip_header, protocol_header):
        ev_parser = EvaluationParser({})
        ev_parser.initialize(Config.CONDITION_RULES)
        ev_parser.parse('port>0;client_port>0;src_port>0;dest_port>0;ttl>0;flags=PSH;seq>0;ack>0;window>=0;mss>=0;wscale>0;sack>0;')

        packet_filter = PacketFilter(ev_parser)

        assert packet_filter.verify_condition(ip_header, protocol_header) is True

    def test_create_byte_by_hex(self, packet_filter):
        hex_data = "48656c6c6f20776f726c64"
        byte_data = packet_filter.create_byte_by_hex(hex_data)
        assert byte_data == b'Hello world'
