import argparse
import logging
import ssl
import sys

from ipsend.configs import Constant
from ipsend.core.pipeline import Pipeline
from ipsurv.util.args_util import ArgsHelper
from ipsurv.util.sys_util import System


class ArgsBuilder:
    def __init__(self, config, pipeline):
        self.config = config
        self.pipeline = pipeline  # type: Pipeline

    def parse(self):
        parent_parser, args = self.init_args(self.config.PRE_ARGUMENTS)

        return self.build_args(parent_parser, self.config.ARGUMENTS)

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

        self._validate_options(parser, args, arguments)

        self._notice(args)

        return (args, parser)

    def _create_bottom_desc(self):
        desc = ''

        desc += Constant.APP_BOTTOM_DESC + "\n"

        return desc

    def _assign_shorten_option(self, args):
        if args.http:
            args.port = 80

        if args.https:
            args.port = 443
            args.mode = Constant.MODE_SSL

        if args.I:
            args.interactive = 1

    def _configure(self, parser, args):
        try:
            args.fixed_ssl_context = self._fix_ssl_context(args)
            self._fix_dest(args)
        except Exception as e:
            logging.log(logging.DEBUG, 'Fix arguments error.', exc_info=True)

            parser.error(e)

    def _fix_ssl_context(self, args):
        if not args.ssl_context:
            ssl_context = None
        else:
            k = args.ssl_context.lower()

            if k in Constant.SSL_CONTEXTS:
                ssl_context = getattr(ssl, Constant.SSL_CONTEXTS[k], None)

                if ssl_context is None:
                    raise Exception('Not support SSL context.')
            else:
                raise Exception('Unknown SSL context.')

        return ssl_context

    def _fix_dest(self, args):
        if args.mode in Constant.RAW_SOCKET_MODES or args.mode in Constant.PAYLOAD_MODES:
            if not args.dest_ip and args.dest:
                args.dest_ip = args.dest

            if not args.dest_port and args.port:
                args.dest_port = args.port

    def _validate_options(self, parser, args, arguments):
        _, rawargs = ArgsHelper.init_parser(arguments, raw=True)

        if args.version or len(sys.argv) == 1:
            return

        mode = args.mode

        if mode in Constant.RICH_SOCKET_MODES:
            self._validate_options_by_mode(mode, parser, rawargs, Constant.RAW_SOCKET_OPTIONS)

            if not args.dest:
                parser.error('`--dest` is required in `{}` mode.'.format(mode))

            if args.port <= 0:
                parser.error('`--port` is required in `{}` mode.'.format(mode))
        elif mode in Constant.RAW_SOCKET_MODES or mode in Constant.PAYLOAD_MODES:
            self._validate_options_by_mode(mode, parser, rawargs, Constant.RICH_SOCKET_OPTIONS)

        if mode != Constant.MODE_SSL:
            self._validate_options_by_mode(mode, parser, rawargs, Constant.SSL_OPTIONS)

        if args.interactive:
            if args.data:
                parser.error('`data` can not be specified with `--interactive` option.')

            if args.output_send:
                parser.error('`output_send` can not be specified specified with `--interactive` option.')

    def _validate_options_by_mode(self, mode, parser, args, non_options):
        non_supports = []

        for key in non_options:
            if getattr(args, key):
                non_supports.append(key)

        if len(non_supports) > 0:
            msg = ', '.join(['`--' + key + '`' for key in non_supports])
            msg += ' option is not supported in `{}` mode.'.format(mode)
            parser.error(msg)

    def _prepare_arguments(self, parser, arguments):
        ArgsHelper.add_arguments(parser, arguments, {}, group_names=self.config.ARGUMENTS_GROUP_NAMES)

    def logging(self, args):
        params = vars(args)

        System.output_data('ARGUMENTS', params)

    def _notice(self, args):
        pass
