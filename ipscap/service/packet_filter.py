import re

from ipscap.util.raw_socket_entity import IPHeader
from ipscap.configs import Constant
import codecs


class PacketFilter:
    def __init__(self, ev_parser):
        self._find_bytes = None
        self._trackings = []
        self._ev_parser = ev_parser

    def initialize(self, args):
        if args.find:
            self.prepare_find(args)

    def verify_capture(self, ip_header, protocol_header, args):
        is_capture = self.filter_packet(ip_header, protocol_header, args)

        if args.tracking:
            (ip1, ip2, port) = self._get_tacking_key(ip_header, protocol_header)

            if is_capture:
                tracking = (ip_header.src_ip, ip_header.dest_ip, port)

                if tracking not in self._trackings:
                    self._add_transfer(ip1, ip2, port)
            else:
                if self._is_tracking_transfer(ip1, ip2, port):
                    is_capture = True

        return is_capture

    def _get_tacking_key(self, ip_header, protocol_header):
        port = protocol_header.dest_port if protocol_header.dest_port < protocol_header.src_port else protocol_header.src_port

        if ip_header.src_ip > ip_header.dest_ip:
            return (ip_header.dest_ip, ip_header.src_ip, port)

        return (ip_header.src_ip, ip_header.dest_ip, port)

    def _add_transfer(self, ip1, ip2, port):
        tracking = (ip1, ip2, port)

        self._trackings.append(tracking)

    def _is_tracking_transfer(self, ip1, ip2, port):
        is_tracking = False

        for tracking in self._trackings:
            if tracking[0] == ip1 and tracking[1] == ip2 and tracking[2] == port:
                is_tracking = True
                break

        return is_tracking

    def filter_packet(self, ip_header, protocol_header, args):
        if not self.verify_protocol(ip_header, args):
            return False

        if not self.verify_ip(ip_header, args):
            return False

        if not self.verify_port(protocol_header, args):
            return False

        if not self.verify_find(ip_header, protocol_header, args):
            return False

        if not self._ev_parser.is_empty():
            if not self.verify_condition(ip_header, protocol_header):
                return False

        return True

    def verify_protocol(self, ip_header, args):
        if IPHeader.PROTOCOL_TCP in args.fixed_protocols and ip_header.protocol == IPHeader.PROTOCOL_TCP:
            return True

        if IPHeader.PROTOCOL_UDP in args.fixed_protocols and ip_header.protocol == IPHeader.PROTOCOL_UDP:
            return True

        if IPHeader.PROTOCOL_ICMP in args.fixed_protocols and ip_header.protocol == IPHeader.PROTOCOL_ICMP:
            return True

        return False

    def verify_ip(self, ip_header, args):
        if args.fixed_ips is not None:
            for ip in args.fixed_ips:
                if ip_header.src_ip == ip or ip_header.dest_ip == ip:
                    return True

            return False

        return True

    def verify_port(self, protocol_header, args):
        if args.fixed_ports is not None:
            for port in args.fixed_ports:
                if protocol_header.src_port == port or protocol_header.dest_port == port:
                    return True

            return False

        return True

    def prepare_find(self, args):
        find_mode = args.find_mode

        if find_mode == Constant.FIND_REGEX or find_mode == Constant.FIND_MATCH:
            self._find_bytes = args.find.encode('utf-8')
        elif find_mode == Constant.FIND_BINARY:
            self._find_bytes = self.create_bytes_by_binary(args.find)
        elif find_mode == Constant.FIND_HEX:
            self._find_bytes = self.create_bytes_by_hex(args.find)

    def verify_find(self, ip_header, protocol_header, args):
        find_mode = args.find_mode

        if args.find:
            if find_mode == Constant.FIND_REGEX or find_mode == Constant.FIND_MATCH:
                flags = re.IGNORECASE if find_mode == Constant.FIND_REGEX else 0

                if not re.search(self._find_bytes, protocol_header.payload_data, flags):
                    return False
            elif find_mode == Constant.FIND_BINARY:
                transfer_data = ip_header.header_data + protocol_header.header_data + protocol_header.payload_data

                if self._find_bytes not in transfer_data:
                    return False
            elif find_mode == Constant.FIND_HEX:
                transfer_data = ip_header.header_data + protocol_header.header_data + protocol_header.payload_data

                if self._find_bytes not in transfer_data:
                    return False

        return True

    def verify_condition(self, ip_header, protocol_header):
        if self._ev_parser.assigned('port'):
            port = protocol_header.dest_port if protocol_header.dest_port < protocol_header.src_port else protocol_header.src_port

            if not self._ev_parser.evaluate('port', port):
                return False

        if self._ev_parser.assigned('client_port'):
            port = protocol_header.dest_port if protocol_header.dest_port > protocol_header.src_port else protocol_header.src_port

            if not self._ev_parser.evaluate('client_port', port):
                return False

        if self._ev_parser.assigned('src_port'):
            if not self._ev_parser.evaluate('src_port', protocol_header.src_port):
                return False

        if self._ev_parser.assigned('dest_port'):
            if not self._ev_parser.evaluate('dest_port', protocol_header.dest_port):
                return False

        if self._ev_parser.assigned('ttl'):
            if not self._ev_parser.evaluate('ttl', ip_header.ttl):
                return False

        if ip_header.protocol == IPHeader.PROTOCOL_TCP:
            if self._ev_parser.assigned('flags'):
                flags = self._ev_parser.get_value('flags')

                if not (protocol_header.flags & flags):
                    return False

            if self._ev_parser.assigned('seq'):
                if not self._ev_parser.evaluate('seq', protocol_header.seq_no):
                    return False

            if self._ev_parser.assigned('ack'):
                if not self._ev_parser.evaluate('ack', protocol_header.ack_no):
                    return False

            if self._ev_parser.assigned('window'):
                if not self._ev_parser.evaluate('window', protocol_header.window):
                    return False

            if self._ev_parser.assigned('mss'):
                if not self._ev_parser.evaluate('mss', protocol_header.tcp_options.get('mss')):
                    return False

            if self._ev_parser.assigned('wscale'):
                if not self._ev_parser.evaluate('wscale', protocol_header.tcp_options.get('wscale')):
                    return False

            if self._ev_parser.assigned('sack'):
                if not self._ev_parser.evaluate('sack', protocol_header.tcp_options.get('sack')):
                    return False

        return True

    def create_bytes_by_binary(self, data):
        return codecs.decode(data, 'unicode_escape').encode('latin1')

    def create_bytes_by_hex(self, data):
        data = re.sub(r'\s', '', data)

        try:
            if len(data) % 2 != 0:
                raise Exception()

            byte_data = bytes.fromhex(data)
        except Exception:
            raise Exception('Hex data parse error.')

        return byte_data
