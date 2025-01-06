import re

from ipscap.util.raw_socket_entity import IPHeader


class PacketFilter:
    def __init__(self, ev_parser):
        self.trackings = []
        self.ev_parser = ev_parser

    def verify_capture(self, ip_header, protocol_header, args):
        is_capture = self.filter_packet(ip_header, protocol_header, args)

        if args.tracking:
            port = protocol_header.dest_port if protocol_header.dest_port < protocol_header.src_port else protocol_header.src_port

            if is_capture:
                tracking = (ip_header.src_ip, ip_header.dest_ip, port)

                if tracking not in self.trackings:
                    self.trackings.append(tracking)
            else:
                if len(self.trackings) > 0:
                    if self._is_tracking_transfer(ip_header, port):
                        is_capture = True

        return is_capture

    def _is_tracking_transfer(self, ip_header, port):
        is_tracking = False

        for tracking in self.trackings:
            if tracking[0] == ip_header.src_ip and tracking[1] == ip_header.dest_ip:
                if tracking[2] == port:
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

        if not self.ev_parser.is_empty():
            if not self.verify_condition(ip_header, protocol_header):
                return False

        return True

    def verify_protocol(self, ip_header, args):
        if IPHeader.PROTOCOL_TCP in args.fixed_filter_protocols and ip_header.protocol == IPHeader.PROTOCOL_TCP:
            return True

        if IPHeader.PROTOCOL_UDP in args.fixed_filter_protocols and ip_header.protocol == IPHeader.PROTOCOL_UDP:
            return True

        if IPHeader.PROTOCOL_ICMP in args.fixed_filter_protocols and ip_header.protocol == IPHeader.PROTOCOL_ICMP:
            return True

        return False

    def verify_ip(self, ip_header, args):
        if args.fixed_filter_ips is not None:
            for ip in args.fixed_filter_ips:
                if ip_header.src_ip == ip or ip_header.dest_ip == ip:
                    return True

            return False

        return True

    def verify_port(self, protocol_header, args):
        if args.fixed_filter_ports is not None:
            for port in args.fixed_filter_ports:
                if protocol_header.src_port == port or protocol_header.dest_port == port:
                    return True

            return False

        return True

    def verify_find(self, ip_header, protocol_header, args):
        if args.find:
            if not args.find_case_sensitive:
                flags = re.IGNORECASE
            else:
                flags = 0

            if not re.search(args.find.encode('utf-8'), protocol_header.payload_data, flags):
                return False

        if args.find_hex:
            search_byte = self.create_byte_by_hex(args.find_hex)

            transfer_data = ip_header.header_data + protocol_header.header_data + protocol_header.payload_data

            if search_byte not in transfer_data:
                return False

        return True

    def verify_condition(self, ip_header, protocol_header):
        if self.ev_parser.assigned('port'):
            port = protocol_header.dest_port if protocol_header.dest_port < protocol_header.src_port else protocol_header.src_port

            if not self.ev_parser.evaluate('port', port):
                return False

        if self.ev_parser.assigned('client_port'):
            port = protocol_header.dest_port if protocol_header.dest_port > protocol_header.src_port else protocol_header.src_port

            if not self.ev_parser.evaluate('client_port', port):
                return False

        if self.ev_parser.assigned('src_port'):
            if not self.ev_parser.evaluate('src_port', protocol_header.src_port):
                return False

        if self.ev_parser.assigned('dest_port'):
            if not self.ev_parser.evaluate('dest_port', protocol_header.dest_port):
                return False

        if self.ev_parser.assigned('ttl'):
            if not self.ev_parser.evaluate('ttl', ip_header.ttl):
                return False

        if ip_header.protocol == IPHeader.PROTOCOL_TCP:
            if self.ev_parser.assigned('flags'):
                flags = self.ev_parser.get_value('flags')

                if not (protocol_header.flags & flags):
                    return False

            if self.ev_parser.assigned('seq'):
                if not self.ev_parser.evaluate('seq', protocol_header.seq_no):
                    return False

            if self.ev_parser.assigned('ack'):
                if not self.ev_parser.evaluate('ack', protocol_header.ack_no):
                    return False

            if self.ev_parser.assigned('window'):
                if not self.ev_parser.evaluate('window', protocol_header.window):
                    return False

            if self.ev_parser.assigned('mss'):
                if not self.ev_parser.evaluate('mss', protocol_header.tcp_options.get('mss')):
                    return False

            if self.ev_parser.assigned('wscale'):
                if not self.ev_parser.evaluate('wscale', protocol_header.tcp_options.get('wscale')):
                    return False

            if self.ev_parser.assigned('sack'):
                if not self.ev_parser.evaluate('sack', protocol_header.tcp_options.get('sack')):
                    return False

        return True

    def create_byte_by_hex(self, data):
        data = re.sub(r'\s', '', data)

        try:
            if len(data) % 2 != 0:
                raise Exception()

            byte_data = bytes.fromhex(data)
        except Exception:
            raise Exception('Hex data parse error.')

        return byte_data
