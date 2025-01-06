from abc import ABC

from ipscap.configs import Config
from ipscap.core.pipeline import Pipeline
from ipscap.service.args_builder import ArgsBuilder
from ipscap.service.dumpfile import DumpFile
from ipscap.service.eth_socket import EthSocket
from ipscap.service.packet_filter import PacketFilter
from ipscap.service.protocol_service import ICMPProtocolService
from ipscap.service.protocol_service import TCPProtocolService
from ipscap.service.protocol_service import UDPProtocolService
from ipscap.service.transfer_store import TransferStore
from ipscap.service.view_helper import ViewHelper
from ipscap.util.raw_socket_parser import IPHeaderParser


class ObjectFactory(ABC):
    """

    """

    def get_config(self):
        """
        :rtype: Config
        """
        return Config

    def create_pipeline(self):
        """
        :rtype: Pipeline
        """
        return Pipeline()

    def create_args_builder(self, config, pipeline):
        """
        :param config:
        :type config: Config
        :param pipeline:
        :type pipeline: Pipeline
        :rtype: ArgsBuilder
        """
        return ArgsBuilder(config, pipeline)

    def create_eth_socket(self):
        return EthSocket()

    def create_ip_header_parser(self):
        return IPHeaderParser()

    def create_packet_filter(self, evaluation_parser):
        return PacketFilter(evaluation_parser)

    def create_transfer_store(self):
        return TransferStore()

    def create_dumpfile(self):
        return DumpFile()

    def create_view_helper(self):
        return ViewHelper()

    def create_icmp_protocol_service(self):
        return ICMPProtocolService()

    def create_tcp_protocol_service(self):
        return TCPProtocolService()

    def create_udp_protocol_service(self):
        return UDPProtocolService()
