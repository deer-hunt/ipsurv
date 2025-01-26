from ipsend.configs import Constant
from ipsend.util.data_io import DataInput
from ipsend.util.raw_socket_entity import TCPHeader
import re


class PacketGenerator:
    def __init__(self, factory, data_input):
        self.factory = factory
        self.data_input = data_input

    def create_data(self, args):
        byte_data = None

        data = self.data_input.get_data(args.data)

        if args.mode == Constant.MODE_ICMP_PAYLOAD:
            generator, entity = self.factory.create_ip_header_generator()
            byte_data = self._create_ip_header_data(generator, entity, args, data)
        elif args.mode == Constant.MODE_TCP_PAYLOAD:
            generator, entity = self.factory.create_tcp_header_generator()
            byte_data = self._create_tcp_header_data(generator, entity, args, data)
        elif args.mode == Constant.MODE_UDP_PAYLOAD:
            generator, entity = self.factory.create_udp_header_generator()
            byte_data = self._create_udp_header_data(generator, entity, args, data)
        elif args.mode == Constant.MODE_ICMP_PAYLOAD:
            generator, entity = self.factory.create_icmp_header_generator()
            byte_data = self._create_icmp_header_data(generator, entity, args, data)
        else:
            raise Exception('Unknown mode.')

        self.data_input.initialize(DataInput.INPUT_RAW)

        return byte_data

    def _create_ip_header_data(self, generator, entity, args, data):
        entity.version = 4
        entity.iph_length = 0
        entity.tos = 0
        entity.total_length = 0
        entity.identification = args.ip_identification
        entity.flags = args.ip_flags
        entity.fragment_offset = 0
        entity.ttl = args.ip_ttl
        entity.protocol = args.ip_protocol
        entity.src_ip = args.src_ip
        entity.src_ip_int = None
        entity.dest_ip = args.dest_ip
        entity.dest_ip_int = None
        entity.payload_data = data

        return generator.generate(entity, args.src_ip, args.dest_ip)

    def _create_tcp_header_data(self, generator, entity, args, data):
        entity.src_port = args.src_port
        entity.dest_port = args.dest_port

        entity.seq_no = args.tcp_seq
        entity.ack_no = args.tcp_ack

        entity.flags = TCPHeader.get_flags(re.split(r'[;,\s]+', args.tcp_flags))
        entity.window = args.tcp_window
        entity.tcp_options = 0
        entity.payload_data = data

        return generator.generate(entity, args.src_ip, args.dest_ip)

    def _create_udp_header_data(self, generator, entity, args, data):
        entity.src_port = args.src_port
        entity.dest_port = args.dest_port
        entity.payload_data = data

        return generator.generate(entity, args.src_ip, args.dest_ip)

    def _create_icmp_header_data(self, generator, entity, args, data):
        entity.type = args.icmp_type
        entity.code = args.icmp_code
        entity.identifier = args.icmp_id
        entity.sequence = args.icmp_seq
        entity.payload_data = data

        return generator.generate(entity, args.src_ip, args.dest_ip)
