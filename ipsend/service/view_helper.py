import logging

from ipsend.configs import Constant
from ipsend.service.sockets import Socket
from ipsurv import __version__
from ipsurv.util.sys_util import AppException
from ipsurv.util.sys_util import System


class ViewHelper:
    def show_head(self, args):
        pass

    def show_stopped(self):
        System.line(' Stopped by user...\n')

    def show_interactive_mode(self, ctrlkey):
        title = 'Line-break to send' if not ctrlkey else 'Ctrl-key to send'

        System.line('[INTERACTIVE] / ' + title + '\n')

        if ctrlkey:
            if not System.verify_os(True):
                msg = 'Press `Ctrl+D` to send.'
            else:
                msg = 'Press `Ctrl+Z` to send.'
        else:
            msg = 'Input a line break to send.'

        System.line('Please input send-data. ' + msg + '\n')

    def show_version(self):
        System.exit(Constant.APP_NAME + ' by ' + Constant.PYPI_NAME + ' ' + __version__)

    def get_hex_data(self, data):
        hex_data = ''.join(f'{byte:02x} ' for byte in data)

        return hex_data

    def output_error(self, e):
        msg = ''

        if not System.is_logging(logging.DEBUG):
            msg = '\n\nSet `--debug` or `--verbose=3` option to output error detail.'

        error = Socket.get_error(e)

        if error:
            System.warn(error + '\n')
        elif not isinstance(e, AppException):
            System.warn('An error has occurred.' + msg + '\n')
        else:
            System.warn(str(e) + msg + '\n')
