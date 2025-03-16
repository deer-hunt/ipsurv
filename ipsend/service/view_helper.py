import logging

from ipsend.configs import Constant
from ipsend.service.sockets import Socket
from ipsurv import __version__
from ipsurv.util.sys_util import AppException
from ipsurv.util.sys_util import Output, System


class ViewHelper:
    def show_head(self, args):
        if not args.quiet:
            Output.line('Mode: ' + args.mode)
            Output.line('Input: ' + str(args.input) + ' / ' + 'Output: ' + str(args.output))

            if args.mode in Constant.RICH_SOCKET_MODES:
                Output.line('Destination: ' + args.dest)
                Output.line('Port: ' + str(args.port))

            if args.mode == Constant.MODE_SSL:
                ssl_context = args.ssl_context if args.ssl_context is not None else 'auto'
                Output.line('SSL context: ' + ssl_context)

            Output.line('')

    def stopped(self):
        Output.line(' Stopped by user...\n')

    def show_interactive_mode(self, ctrlkey):
        title = 'Line-break to send' if not ctrlkey else 'Ctrl-key to send'

        Output.line('[INTERACTIVE] / ' + title + '\n')

        if ctrlkey:
            if not System.verify_os(True):
                msg = 'Press `Ctrl+D` to send.'
            else:
                msg = 'Press `Ctrl+Z` to send.'
        else:
            msg = 'Input a line break to send.'

        Output.line('Please input send-data. ' + msg + '\n')

    def show_version(self):
        System.exit(Constant.APP_NAME + ' by ' + Constant.PYPI_NAME + ' ' + __version__)

    def get_hex_data(self, data):
        hex_data = ''.join(f'{byte:02x} ' for byte in data)

        return hex_data

    def output_error(self, e):
        msg = ''

        if not Output.is_logging(logging.DEBUG):
            msg = '\n\nSet `--debug` or `--verbose=3` option to output error detail.'

        error = Socket.get_error(e)

        if error:
            Output.warn(error + '\n')
        elif not isinstance(e, AppException):
            Output.warn('An error has occurred.' + msg + '\n')
        else:
            Output.warn(str(e) + msg + '\n')

    def output_closed_error(self):
        Output.line('Connection is closed unexpectedly.')
