from abc import ABC

from ipscap.configs import Constant
from ipscap.util.raw_socket_entity import IPHeader
from ipsurv.util.sys_util import System


class ProtocolService(ABC):
    _instances = {}

    @classmethod
    def register_services(cls, icmp_service, tcp_service, udp_service):
        cls._instances[IPHeader.PROTOCOL_ICMP] = icmp_service
        cls._instances[IPHeader.PROTOCOL_TCP] = tcp_service
        cls._instances[IPHeader.PROTOCOL_UDP] = udp_service

    @classmethod
    def get_service(cls, protocol):
        return cls._instances.get(protocol)

    def show_transfer(self, ip_header, protocol_header, passage_num, now, output):
        if output != Constant.OUTPUT_NONE:
            if output != Constant.OUTPUT_LINE:
                self.show_overview(ip_header, protocol_header, now, passage_num)
                self.show_payload(protocol_header, output)
            else:
                self.show_line(ip_header, protocol_header, now, passage_num)

    def show_overview(self, ip_header, protocol_header, now, passage_num):
        pass

    def show_head(self, ip_header, now, passage_num):
        System.line(self.label('Time:') + self.get_datatime(now) + ' / ' + self.get_timestamp(now) + ', Passage number: ' + str(passage_num))
        System.line(self.label('IP header:') + 'Version: ' + str(ip_header.version) + ', IP header length: ' + str(ip_header.iph_length) + ', Packet length: ' + str(ip_header.packet_length) + ', TTL: ' + str(ip_header.ttl) + ', IP protocol: ' + ip_header.protocol_code + "[{}]".format(str(ip_header.protocol)))

    def show_middle(self, ip_header, protocol_header, show_data_len):
        System.line(self.label('Source:') + self.label('IP: ' + str(ip_header.src_ip), 30) + 'Port: ' + str(protocol_header.src_port))
        System.line(self.label('Destination:') + self.label('IP: ' + str(ip_header.dest_ip), 30) + 'Port: ' + str(protocol_header.dest_port))

        if ip_header.direction == 1:
            direction_msg = 'SEND [ >>> ]'
        elif ip_header.direction == 2:
            direction_msg = 'RECEIVE [ <<< ]'
        else:
            direction_msg = 'UNKNOWN'

        System.line(self.label('Direction:') + direction_msg)

        if show_data_len:
            System.line(self.label('Data length:') + str(protocol_header.payload_length) + ' byte')

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        pass

    def show_payload(self, protocol_header, output):
        if output == Constant.OUTPUT_TEXT:
            data = protocol_header.payload_data.decode('utf-8', errors='ignore')

            if len(protocol_header.get_sanitized_data()) > 0:
                System.line(data + "\n")
        elif output == Constant.OUTPUT_BINARY:
            System.line(protocol_header.payload_data)
            System.line('')
        elif output == Constant.OUTPUT_HEX:
            hex_data = self.get_hex_data(protocol_header.payload_data)
            System.line(hex_data + "\n")

    def get_datatime(self, now):
        return now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-2]

    def get_timestamp(self, now):
        return str(now.timestamp())[:-2]

    def get_hex_data(self, data):
        hex_data = ''.join(f'{byte:02x} ' for byte in data)

        return hex_data

    def label(self, v, n=16):
        return v.ljust(n)


class ICMPProtocolService(ProtocolService):
    def show_overview(self, ip_header, protocol_header, now, passage_num):
        self.show_head(ip_header, now, passage_num)

        System.line(self.label('ICMP header:') + 'ICMP header length: ' + str(protocol_header.icmph_length) + ', Type: ' + str(protocol_header.icmp_type) + ', Code: ' + str(protocol_header.code))

        self.show_middle(ip_header, protocol_header, False)

        System.line(self.label('IP-H data:') + self.get_hex_data(ip_header.header_data))
        System.line(self.label('ICMP-H data:') + self.get_hex_data(protocol_header.header_data))
        System.line('')

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        line = ''

        line += self.get_datatime(now) + split
        line += str(passage_num) + split
        line = line.ljust(30)

        line += str(ip_header.version) + split + str(ip_header.iph_length) + split + str(ip_header.ttl) + split + str(ip_header.packet_length) + split
        line = line.ljust(50)

        line += str(ip_header.protocol_code) + split
        line += str(protocol_header.icmph_length) + split
        line = line.ljust(60)

        line += str(protocol_header.icmp_type) + split + str(protocol_header.code) + split
        line = line.ljust(70)

        line += str(ip_header.src_ip) + split
        line = line.ljust(95)

        line += str(ip_header.dest_ip) + split
        line = line.ljust(120)

        line += ip_header.direction_code + split

        System.line(line)

    def show_payload(self, protocol_header, output):
        pass


class TCPProtocolService(ProtocolService):
    def show_overview(self, ip_header, protocol_header, now, passage_num):
        self.show_head(ip_header, now, passage_num)

        System.line(self.label('TCP header:') + 'TCP header length: ' + str(protocol_header.tcph_length) + ', Sequence: ' + str(protocol_header.seq_no) + ', Acknowledgement: ' + str(protocol_header.ack_no) + ', Window: ' + str(protocol_header.window) + ', Flags: ' + str(protocol_header.flag_codes))
        System.line(self.label('TCP options:') + self._get_tcp_options(protocol_header.tcp_options))

        self.show_middle(ip_header, protocol_header, True)

        System.line(self.label('IP-H data:') + self.get_hex_data(ip_header.header_data))
        System.line(self.label('TCP-H data:') + self.get_hex_data(protocol_header.header_data))
        System.line('')

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        line = ''

        line += self.get_datatime(now) + split
        line += str(passage_num) + split
        line = line.ljust(30)

        line += str(ip_header.version) + split + str(ip_header.iph_length) + split + str(ip_header.ttl) + split + str(ip_header.packet_length) + split
        line = line.ljust(50)

        line += str(ip_header.protocol_code) + split
        line += str(protocol_header.tcph_length) + split + str(protocol_header.seq_no) + split + str(protocol_header.ack_no) + split + str(protocol_header.window) + split
        line = line.ljust(90)

        line += str(protocol_header.flag_codes) + split
        line = line.ljust(112)

        line += str(protocol_header.payload_length) + split
        line = line.ljust(120)

        line += str(ip_header.src_ip) + ':' + str(protocol_header.src_port) + split
        line = line.ljust(145)

        line += str(ip_header.dest_ip) + ':' + str(protocol_header.dest_port) + split
        line = line.ljust(170)

        line += ip_header.direction_code + split
        line = line.ljust(185)

        line += self._get_tcp_options(protocol_header.tcp_options, ';')

        System.line(line)

    def _get_tcp_options(self, tcp_options, split=', '):
        value = ''

        if len(tcp_options) > 0:
            for k, v in tcp_options.items():
                if isinstance(v, bool):
                    value += k
                else:
                    value += k + ':' + str(v)

                value += split

            value = value.strip(split)
        else:
            value = '-'

        return value


class UDPProtocolService(ProtocolService):
    def show_overview(self, ip_header, protocol_header, now, passage_num):
        self.show_head(ip_header, now, passage_num)

        System.line(self.label('UDP header:') + 'UDP header length: ' + str(protocol_header.udph_length))

        self.show_middle(ip_header, protocol_header, True)

        System.line(self.label('IP-H data:') + self.get_hex_data(ip_header.header_data))
        System.line(self.label('UDP-H data:') + self.get_hex_data(protocol_header.header_data))
        System.line('')

    def show_line(self, ip_header, protocol_header, now, passage_num, split=', '):
        line = ''

        line += self.get_datatime(now) + split
        line += str(passage_num) + split
        line = line.ljust(30)

        line += str(ip_header.version) + split + str(ip_header.iph_length) + split + str(ip_header.ttl) + split + str(ip_header.packet_length) + split
        line = line.ljust(50)

        line += str(ip_header.protocol_code) + split
        line += str(protocol_header.udph_length) + split
        line = line.ljust(55)

        line += str(protocol_header.payload_length) + split
        line = line.ljust(70)

        line += str(ip_header.src_ip) + ':' + str(protocol_header.src_port) + split
        line = line.ljust(95)

        line += str(ip_header.dest_ip) + ':' + str(protocol_header.dest_port) + split
        line = line.ljust(120)

        line += ip_header.direction_code + split

        System.line(line)
