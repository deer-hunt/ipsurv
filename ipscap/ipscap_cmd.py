import sys

import logging
import signal
import threading
from datetime import datetime
from functools import partial

from ipscap.configs import Config, Constant
from ipscap.core.object_factory import ObjectFactory
from ipscap.core.pipeline import Pipeline
from ipscap.service.dumpfile import DumpFile
from ipscap.service.eth_socket import EthSocket
from ipscap.service.packet_filter import PacketFilter
from ipscap.service.protocol_service import ProtocolService
from ipscap.service.transfer_store import TransferStore
from ipscap.service.view_helper import ViewHelper
from ipscap.util.evaluation_parser import EvaluationParser
from ipscap.util.raw_socket_parser import IPHeaderParser
from ipsurv.util.sys_util import System


class IpsCapCmd:
    def __init__(self, factory):
        self.factory = factory  # type: ObjectFactory
        self.pipeline = self.factory.create_pipeline()  # type: Pipeline
        self.config = self.factory.get_config()  # type: Config

        self.capture_thread = None  # type: CaptureThread
        self.transfer_store = None  # type: TransferStore
        self.dumpfile = None  # type: DumpFile
        self.view_helper = None  # type: ViewHelper

    def run(self):
        try:
            args, parser = self._parse_args()

            self._initialize(args)

            self._verify_args(args, parser)

            self.dispatch(args)
        except Exception as e:
            self.view_helper.output_error(e)

            logging.log(logging.ERROR, str(e), exc_info=True)

    def _verify_args(self, args, parser):
        if args.version:
            self.view_helper.show_version()
        elif len(sys.argv) == 1:
            parser.print_help()
            sys.exit()
        elif not args.has_filters and not args.force:
            self.view_helper.show_nofilters()

    def _initialize(self, args):
        self._register_protocol_services()

        ev_parser = EvaluationParser()
        ev_parser.initialize(self.config.CONDITION_RULES)
        parsed_cond = ev_parser.parse(args.condition)

        System.output_data('PARSED_CONDITION', parsed_cond)

        packet_filter = self.factory.create_packet_filter(ev_parser)
        packet_filter.initialize(args)

        self.transfer_store = self.factory.create_transfer_store()

        self.dumpfile = self.factory.create_dumpfile()

        if args.dumpfile:
            self.dumpfile.initialize(Constant.DUMPFILE_DIR)

        self.view_helper = self.factory.create_view_helper()

        signal.signal(signal.SIGINT, partial(self.signal_stop, args=args))

        self.capture_thread = CaptureThread(self.factory, self.pipeline, packet_filter, self.transfer_store, self.dumpfile, self.view_helper, args)

        self.capture_thread.initialize()

        self.pipeline.initialize(self.config)

    def _register_protocol_services(self):
        icmp_service = self.factory.create_icmp_protocol_service()
        tcp_service = self.factory.create_tcp_protocol_service()
        udp_service = self.factory.create_udp_protocol_service()

        ProtocolService.register_services(icmp_service, tcp_service, udp_service)

    def _parse_args(self):
        args_builder = self.factory.create_args_builder(self.config, self.pipeline)

        return args_builder.parse()

    def dispatch(self, args):
        self.view_helper.show_head(args)

        self.capture_thread.start()

        self.capture_thread.join(args.timeout)

        self._complete(args)

    def signal_stop(self, sig, frame, args):
        self.view_helper.show_stopped()

        self._complete(args)

        sys.exit()

    def _complete(self, args):
        transfers = self.transfer_store.totalize(args.stat_group)

        self.pipeline.complete(transfers)

        self.view_helper.show_statistics(transfers, args)

        if args.dumpfile:
            self.view_helper.show_dumpfile_info(self.dumpfile)


class CaptureThread(threading.Thread):
    def __init__(self, factory, pipeline, packet_filter, transfer_store, dumpfile, view_helper, args):
        super().__init__()

        self.daemon = True

        self.factory = factory  # type: ObjectFactory
        self.pipeline = pipeline  # type: Pipeline
        self.packet_filter = packet_filter  # type: PacketFilter
        self.transfer_store = transfer_store  # type: TransferStore
        self.dumpfile = dumpfile  # type: DumpFile
        self.view_helper = view_helper  # type: ViewHelper
        self.args = args

        self.eth_socket = None  # type: EthSocket
        self.ip_header_parser = None  # type: IPHeaderParser

    def initialize(self):
        self.eth_socket = self.factory.create_eth_socket()

        self.eth_socket.create_socket()

        eth_ips = self.eth_socket.get_eth_ips_int()

        self.pipeline.pass_eth_ips(eth_ips)

        logging.log(logging.INFO, 'ETH_IPS: ' + str(eth_ips) + '\n')

        self.ip_header_parser = self.factory.create_ip_header_parser()

        self.ip_header_parser.initialize(eth_ips)

    def run(self):
        self.pipeline.pre_recieve_loop(self.eth_socket, self.ip_header_parser)

        try:
            while True:
                raw_data = self.eth_socket.recvfrom(Constant.RECV_BUF_SIZE)

                eth_header = self.eth_socket.get_eth_header(raw_data)

                self.pipeline.pass_eth_header(raw_data, eth_header)

                if not self.eth_socket.is_enabled_protocol(eth_header):
                    self.view_helper.output_not_support(eth_header)
                    continue

                ip_mtu = self.eth_socket.get_ip_mtu(raw_data)

                (ip_header, protocol_header) = self._parse_ip_mtu(ip_mtu)

                is_capture = self._verify_capture(ip_header, protocol_header)

                self.view_helper.output_debug(is_capture, ip_header, protocol_header)

                passage_num = -1

                if (is_capture and self.args.stat_mode == 1) or self.args.stat_mode == 2:
                    (passage_num) = self.transfer_store.add(ip_header, protocol_header)

                if is_capture:
                    self._process_captured_transfer(ip_header, protocol_header, passage_num)
        except Exception as e:
            self.view_helper.output_error(e)

            logging.log(logging.ERROR, str(e), exc_info=True)

    def _parse_ip_mtu(self, mtu_data):
        ip_header = self.ip_header_parser.parse(mtu_data)

        self.pipeline.pass_ip_header(mtu_data, ip_header)

        header_parser = self.ip_header_parser.get_header_parser(ip_header)

        header_parser = self.pipeline.pass_header_parser(ip_header, header_parser)

        protocol_header = header_parser.parse(ip_header, mtu_data)

        return (ip_header, protocol_header)

    def _verify_capture(self, ip_header, protocol_header):
        is_capture = self.packet_filter.verify_capture(ip_header, protocol_header, self.args)

        return self.pipeline.verify_capture(self.packet_filter, ip_header, protocol_header, is_capture)

    def _process_captured_transfer(self, ip_header, protocol_header, passage_num):
        if self.args.dumpfile:  # Dump logs
            append_header = (self.args.dumpfile == 2)

            if len(protocol_header.get_sanitized_data()) > 0 or append_header:
                self.dumpfile.write(ip_header, protocol_header, append_header)

        self.pipeline.process_captured_transfer(ip_header, protocol_header, passage_num)

        protocol_service = ProtocolService.get_service(ip_header.protocol)

        protocol_service.show_transfer(ip_header, protocol_header, passage_num, datetime.now(), self.args.fixed_output)
