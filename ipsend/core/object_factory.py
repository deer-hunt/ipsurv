from abc import ABC

from ipsend.configs import Config
from ipsend.core.pipeline import Pipeline
from ipsend.service.args_builder import ArgsBuilder
from ipsend.service.dumpfile import DumpFile
from ipsend.service.sockets import RichSocket, RawSocket, SocketThread
from ipsend.service.view_helper import ViewHelper
from ipsend.util.data_io import DataInput, DataOutput, InteractiveInput
from ipsend.util.raw_socket_entity import IPHeader, ICMPHeader, TCPHeader, UDPHeader
from ipsend.util.raw_socket_generator import IPHeaderGenerator, TCPHeaderGenerator, UDPHeaderGenerator, ICMPHeaderGenerator


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

    def create_data_input(self):
        return DataInput()

    def create_data_output(self):
        return DataOutput()

    def create_interactive_input(self, ctrlkey):
        return InteractiveInput(ctrlkey)

    def create_rich_socket(self, pipeline):
        return RichSocket(pipeline)

    def create_raw_socket(self, pipeline):
        return RawSocket(pipeline)

    def create_socket_thread(self, socket, view_helper):
        return SocketThread(socket, view_helper)

    def create_ip_header_generator(self):
        return (IPHeaderGenerator(), IPHeader())

    def create_tcp_header_generator(self):
        return (TCPHeaderGenerator(), TCPHeader())

    def create_udp_header_generator(self):
        return (UDPHeaderGenerator(), UDPHeader())

    def create_icmp_header_generator(self):
        return (ICMPHeaderGenerator(), ICMPHeader())

    def create_dumpfile(self, pipeline):
        return DumpFile(pipeline)

    def create_view_helper(self):
        return ViewHelper()
