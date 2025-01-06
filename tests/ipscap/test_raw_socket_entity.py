from ipscap.util.raw_socket_entity import IPHeader, ICMPHeader, TCPHeader, UDPHeader
import pytest
import re


class TestIPHeader:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_get_protocol_code(self):
        assert IPHeader.get_protocol_code(IPHeader.PROTOCOL_ICMP) == 'ICMP'
        assert IPHeader.get_protocol_code(IPHeader.PROTOCOL_TCP) == 'TCP'
        assert IPHeader.get_protocol_code(IPHeader.PROTOCOL_UDP) == 'UDP'
        assert IPHeader.get_protocol_code(0) == 'UNKNOWN'

    def test_get_protocol(self):
        assert IPHeader.get_protocol('ICMP') == IPHeader.PROTOCOL_ICMP
        assert IPHeader.get_protocol('TCP') == IPHeader.PROTOCOL_TCP
        assert IPHeader.get_protocol('UDP') == IPHeader.PROTOCOL_UDP

    def test_get_direction_code(self):
        assert IPHeader.get_direction_code(IPHeader.DIRECTION_SEND) == 'SEND'
        assert IPHeader.get_direction_code(IPHeader.DIRECTION_RECEIVE) == 'RECEIVE'


class TestTCPHeader:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_get_protocol_code(self):
        assert TCPHeader.get_flag_codes(TCPHeader.FLAG_FIN) == ['FIN']
        assert TCPHeader.get_flag_codes(TCPHeader.FLAG_ACK) == ['ACK']

        flag_codes = TCPHeader.get_flag_codes(TCPHeader.FLAG_SYN | TCPHeader.FLAG_RST | TCPHeader.FLAG_PSH | TCPHeader.FLAG_URG | TCPHeader.FLAG_ECE | TCPHeader.FLAG_CWR)

        assert 'SYN' in flag_codes
        assert 'PSH' in flag_codes
        assert 'RST' in flag_codes
        assert 'CWR' in flag_codes

    def test_get_flags(self):
        flags = TCPHeader.get_flags(['FIN', 'SYN', 'RST', 'PSH', 'ACK'])

        assert flags & TCPHeader.FLAG_SYN
        assert flags & TCPHeader.FLAG_RST
        assert flags & TCPHeader.FLAG_PSH
        assert flags & TCPHeader.FLAG_FIN
        assert flags & TCPHeader.FLAG_ACK
