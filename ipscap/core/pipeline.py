from abc import ABC

from ipscap.configs import Config, Constant


class Pipeline(ABC):
    """

    """

    def __init__(self):
        self.config = None  # type: Config

    def initialize(self, config):
        """
        :param config:
        :type config: Config
        """

        self.config = config

    def init_configure(self, arguments):
        """
        :param arguments:
        :type arguments: dict
        """
        pass

    def pass_eth_ips(self, eth_ips):
        pass

    def pre_recieve_loop(self, eth_socket, ip_header_parser):
        pass

    def pass_eth_header(self, raw_data, eth_header):
        pass

    def pass_ip_header(self, mtu_data, ip_header):
        pass

    def pass_header_parser(self, ip_header, header_parser):
        return header_parser

    def pass_protocol_header(self, ip_header, protocol_header):
        pass

    def verify_capture(sself, packet_filter, ip_header, protocol_header, is_capture):
        return is_capture

    def process_captured_transfer(self, ip_header, protocol_header, passage_num):
        pass

    def complete(self, transfers):
        pass
