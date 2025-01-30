import logging
import signal
import sys

from ipsend.configs import Config, Constant
from ipsend.core.object_factory import ObjectFactory
from ipsend.core.pipeline import Pipeline
from ipsend.service.packet_generator import PacketGenerator
from ipsend.service.view_helper import ViewHelper


class IpSendCmd:
    def __init__(self, factory):
        self.factory = factory  # type: ObjectFactory
        self.pipeline = self.factory.create_pipeline()  # type: Pipeline
        self.config = self.factory.get_config()  # type: Config

        self.socket = None
        self.data_input = None
        self.data_output = None

        self.dumpfile = None
        self.view_helper = None  # type: ViewHelper

    def run(self):
        try:
            self._pre_initialize()

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

    def _pre_initialize(self):
        self.view_helper = self.factory.create_view_helper()

    def _initialize(self, args):
        self.data_input = self.factory.create_data_input()
        self.data_input.initialize(args.input)

        self.data_output = self.factory.create_data_output()
        self.data_output.initialize(args.output)

        if args.dumpfile:
            self.dumpfile = self.factory.create_dumpfile(self.pipeline)
            self.dumpfile.initialize(Constant.DUMPFILE_DIR)

        self.socket = self._create_socket(args.mode, args.fixed_ssl_context)
        self.socket.initialize(self.data_input, self.data_output, self.dumpfile, args.mode, args.timeout)

        self.pipeline.initialize(self.config)

        signal.signal(signal.SIGINT, self.signal_stop)

    def _create_socket(self, mode, ssl_context):
        socket = None

        if mode in Constant.RICH_SOCKET_MODES:
            socket = self.factory.create_rich_socket(self.pipeline)
            socket.set_ssl_context(ssl_context)
        elif mode in Constant.RAW_SOCKET_MODES:
            socket = self.factory.create_raw_socket(self.pipeline)

        return socket

    def _parse_args(self):
        args_builder = self.factory.create_args_builder(self.config, self.pipeline)

        return args_builder.parse()

    def dispatch(self, args):
        self.view_helper.show_head(args)

        if not args.interactive:
            self._run_instant(args)
        else:
            self._run_interactive(args)

        self._complete()

    def signal_stop(self, sig, frame):
        self.view_helper.show_stopped()

        self._complete()

        sys.exit()

    def _run_instant(self, args):
        data = self._create_send_data(args)

        if args.output_send > 0:
            byte_data = self.data_input.get_data(data)
            self.data_output.output_binary(byte_data)

            if args.output_send == 2:
                return

        self.socket.create(args.dest, args.port)

        self.socket.send(data)

        self.socket.receive()

        self.socket.close()

    def _create_send_data(self, args):
        if args.mode not in Constant.PAYLOAD_MODES:
            data = args.data

            if args.mode in Constant.RICH_SOCKET_MODES:
                if args.auto_lb and args.input == Constant.INPUT_TEXT:
                    data += '\n'
        else:
            packet_generator = PacketGenerator(self.factory, self.data_input)
            data = packet_generator.create_data(args)

        return data

    def _run_interactive(self, args):
        ctrlkey = True if args.interactive == 2 else False

        self.view_helper.show_interactive_mode(ctrlkey)

        socket_thread = self.factory.create_socket_thread(self.socket, self.view_helper)

        self.socket.create(args.dest, args.port)

        socket_thread.start()

        interactive_input = self.factory.create_interactive_input(ctrlkey)

        while True:
            line = interactive_input.get_input()

            if not self.socket.connected():
                self.view_helper.output_closed_error()
                break

            if line is not None:
                self.socket.send(line)

    def _complete(self):
        self.pipeline.complete()
