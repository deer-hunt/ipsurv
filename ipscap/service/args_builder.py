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
            args.port = '80,443,53'

        if args.general_port:
            args.port = '21,22,23,25,53,80,110,143,220,443,465,990,993,995,1433,3306'

        if args.exclude_ssh:
            if not args.condition:
                args.condition = ''

            args.condition = 'port!=22;' + args.condition

    def _configure(self, parser, args):
        try:
            args.fixed_find_mode = self._fix_find_mode(args)
            args.fixed_protocols = self.fix_protocols(args)
            args.fixed_ips = self._fix_ips(args)
            args.fixed_ports = self._fix_ports(args)
            args.fixed_output = self._fix_output(args)
            args.has_filters = self._has_filters(args)
        except Exception as e:
            logging.log(logging.DEBUG, 'Fix arguments error.', exc_info=True)

            parser.error(e)

    def _prepare_arguments(self, parser, arguments):
        ArgsHelper.add_arguments(parser, arguments, {})

    def _fix_find_mode(self, args):
        find_mode = args.find_mode.upper()

        defines = {
            1: Constant.FIND_REGEX,
            2: Constant.FIND_MATCH,
            3: Constant.FIND_BINARY,
            4: Constant.FIND_HEX,
        }

        if find_mode.isdigit():
            v = int(find_mode)

            if v in defines:
                find_mode = defines[v]
            else:
                find_mode = None
        else:
            if find_mode not in defines.values():
                find_mode = None

        if find_mode is None:
            raise Exception('Unknown output mode (--find_mode)')

        logging.log(logging.INFO, 'Fixed find_mode:' + find_mode)

        return find_mode

    def _fix_ips(self, args):
        ips = re.split(r'[;, ]+', args.ip)

        ips = list(filter(lambda v: v.strip(), ips))

        ips = ips if len(ips) > 0 else None

        logging.log(logging.INFO, 'Fixed ips:' + str(ips))

        return ips

    def _fix_ports(self, args):
        ports = re.split(r'[;, ]+', args.port)

        ports = list(filter(lambda v: v.strip(), ports))
        ports = list(map(lambda v: int(v), ports))

        ports = ports if len(ports) > 0 else None

        logging.log(logging.INFO, 'Fixed ports:' + str(ports))

        return ports

    def fix_protocols(self, args):
        protocols = []

        tprotocols = re.split(r'[;, ]+', args.protocol)

        for protocol in tprotocols:
            protocol_code = protocol.upper()

            if protocol_code == 'ALL':
                protocols = [IPHeader.PROTOCOL_ICMP, IPHeader.PROTOCOL_TCP, IPHeader.PROTOCOL_UDP]
                break

            protocol = IPHeader.get_protocol(protocol_code)

            if protocol > 0:
                protocols.append(protocol)
            else:
                raise Exception('Unknown protocol (--protocol)')

        logging.log(logging.INFO, 'Fixed protocols:' + str(protocols))

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
        if IPHeader.PROTOCOL_TCP not in args.fixed_protocols:
            return True

        if args.find:
            return True

        if args.fixed_ips:
            return True

        if args.fixed_ports:
            return True

        if args.condition:
            return True

        return False

    def logging(self, args):
        params = vars(args)

        System.output_data('ARGUMENTS', params)

    def _notice(self, args):
        pass
