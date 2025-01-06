import argparse
import logging
import re

from ipscap.configs import Constant
from ipscap.core.pipeline import Pipeline
from ipscap.util.raw_socket_entity import IPHeader
from ipsurv.util.args_util import ArgsHelper
from ipsurv.util.sys_util import System


class ArgsBuilder:
    def __init__(self, config, pipeline):
        self.config = config
        self.pipeline = pipeline  # type: Pipeline

    def parse(self):
        parent_parser, args = self.init_args(self.config.PRE_ARGUMENTS)

        return self.build_args(parent_parser, self.config.APP_ARGUMENTS)

    def init_args(self, arguments):
        parser, args = ArgsHelper.init_parser(arguments)

        if args.debug:
            args.verbose = 3

        ArgsHelper.init_logging(args.verbose, args.log)

        if args.verbose > 0:
            System.warn('Enable verbose mode. Current:' + str(args.verbose) + ' [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]')

            if args.log is not None:
                System.warn('Enable log.(File:' + args.log + ')')

        return parser, args

    def build_args(self, parent_parser, arguments):
        desc = self._create_bottom_desc()

        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, parents=[parent_parser], description=Constant.APP_DESCRIPTION, epilog=desc)

        self.pipeline.init_configure(arguments)

        self._prepare_arguments(parser, arguments)

        args = parser.parse_args()

        self._assign_shorten_option(args)

        if System.is_logging():
            self.logging(args)

        self._configure(parser, args)

        self._notice(args)

        return (args, parser)

    def _create_bottom_desc(self):
        desc = ''

        desc += Constant.APP_BOTTOM_DESC + "\n"

        return desc

    def _assign_shorten_option(self, args):
        if args.web_port:
            args.filter_port = '80,443,53'

        if args.general_port:
            args.filter_port = '21,22,23,25,53,80,110,143,220,443,465,990,993,995,1433,3306'

        if args.exclude_ssh:
            if not args.filter_condition:
                args.filter_condition = ''

            args.filter_condition = 'port!=22;' + args.filter_condition

    def _configure(self, parser, args):
        try:
            args.fixed_filter_protocols = self.fix_filter_protocols(args)
            args.fixed_filter_ips = self._fix_filter_ips(args)
            args.fixed_filter_ports = self._fix_filter_ports(args)
            args.fixed_output = self._fix_output(args)
            args.has_filters = self._has_filters(args)
        except Exception as e:
            logging.log(logging.DEBUG, 'Fix arguments error.', exc_info=True)

            parser.error(e)

    def _prepare_arguments(self, parser, arguments):
        ArgsHelper.add_arguments(parser, arguments, {})

    def _fix_filter_ips(self, args):
        ips = re.split(r'[;, ]+', args.filter_ip)

        ips = list(filter(lambda v: v.strip(), ips))

        ips = ips if len(ips) > 0 else None

        logging.log(logging.INFO, 'Fixed filter_ips:' + str(ips))

        return ips

    def _fix_filter_ports(self, args):
        ports = re.split(r'[;, ]+', args.filter_port)

        ports = list(filter(lambda v: v.strip(), ports))
        ports = list(map(lambda v: int(v), ports))

        ports = ports if len(ports) > 0 else None

        logging.log(logging.INFO, 'Fixed filter_ports:' + str(ports))

        return ports

    def fix_filter_protocols(self, args):
        protocols = []

        tprotocols = re.split(r'[;, ]+', args.filter_protocol)

        for protocol in tprotocols:
            protocol_code = protocol.upper()

            if protocol_code == 'ALL':
                protocols = [IPHeader.PROTOCOL_ICMP, IPHeader.PROTOCOL_TCP, IPHeader.PROTOCOL_UDP]
                break

            protocol = IPHeader.get_protocol(protocol_code)

            if protocol > 0:
                protocols.append(protocol)
            else:
                raise Exception('Unknown protocol (--filter_protocol)')

        logging.log(logging.INFO, 'Fixed filter_protocols:' + str(protocols))

        return protocols

    def _fix_output(self, args):
        output = args.output.upper()

        defines = {
            0: Constant.OUTPUT_NONE,
            1: Constant.OUTPUT_HEADER,
            2: Constant.OUTPUT_TEXT,
            3: Constant.OUTPUT_BINARY,
            4: Constant.OUTPUT_HEX,
            5: Constant.OUTPUT_LINE
        }

        if output.isdigit():
            v = int(output)

            if v in defines:
                output = defines[v]
            else:
                output = None
        else:
            if output not in defines.values():
                output = None

        if output is None:
            raise Exception('Unknown output mode (--output)')

        logging.log(logging.INFO, 'Fixed show:' + output)

        return output

    def _has_filters(self, args):
        if args.find or args.find_hex:
            return True

        if IPHeader.PROTOCOL_TCP not in args.fixed_filter_protocols:
            return True

        if args.fixed_filter_ips:
            return True

        if args.fixed_filter_ports:
            return True

        if args.filter_condition:
            return True

        return False

    def logging(self, args):
        params = vars(args)

        System.output_data('ARGUMENTS', params)

    def _notice(self, args):
        pass
