import logging

from ipscap.configs import Constant
from ipscap.util.raw_socket_entity import IPHeader
from ipsurv import __version__
from ipsurv.util.sys_util import System
from ipsurv.util.sys_util import AppException
from datetime import datetime


class ViewHelper:
    TITLE_WIDTH = 120

    def show_head(self, args):
        System.line('Start capture packets...\n')

        if args.timeout is None:
            System.line('Press `Ctrl + C` to stop.\n')
        else:
            System.line("`--timeout` option is enabled. The capture will stop {} seconds automatically.".format(args.timeout) + "\n")

        if args.has_filters:
            self.show_filter_options(args)

    def show_filter_options(self, args):
        System.line('[FILTERS]')

        if args.protocol != 'TCP,UDP':
            self._show_option(args, 'protocol', 'fixed_protocols', lambda w: [IPHeader.get_protocol_code(v) for v in w])

        self._show_option(args, 'port', 'fixed_ports')

        self._show_option(args, 'ip', 'fixed_ips')

        if args.find:
            self._show_option(args, 'find')
            self._show_option(args, 'find_mode', 'fixed_find_mode')

        self._show_option(args, 'condition')

        self._show_option(args, 'tracking')

        System.line('')

    def _show_option(self, args, name, internal_name=None, fn=None):
        internal_name = internal_name if internal_name else name

        v = getattr(args, internal_name)

        if v:
            if fn:
                v = fn(v)

            System.line((name + ':').ljust(14) + str(v))

    def show_dumpfile_info(self, dumpfile):
        border = self.get_border()

        System.line(border + 'Captured Dump Logs'.center(self.TITLE_WIDTH) + border)
        System.line('Path:'.ljust(8) + dumpfile.get_path())
        System.line('Files:'.ljust(8) + str(dumpfile.get_file_num()))
        System.line('')

    def show_statistics(self, transfers, begin_tm, end_tm, args):
        self._show_stat_top(args.stat_mode)

        self._show_times(begin_tm, end_tm)

        self._show_stat_transfers(transfers, args.stat_group)

    def _show_stat_top(self, stat_mode):
        border = self.get_border()

        System.line(border + 'TRANSFER STATISTICS'.center(self.TITLE_WIDTH) + border)

        if stat_mode == 0:
            System.line('*The statistics is disabled by `--stat_mode` option.')
        elif stat_mode == 1:
            System.line('*The following is the statistics for captured transfers only. If you\'d like see to the statistics for all transfers, set`--stat_mode=2` option.')
        elif stat_mode == 2:
            System.line('*The following is the statistics for all transfers.')

        System.line("\n")

    def _show_times(self, begin_tm, end_tm):
        System.line('Begin time: '.ljust(16) + datetime.fromtimestamp(begin_tm).strftime('%Y-%m-%d %H:%M:%S'))
        System.line('End time: '.ljust(16) + datetime.fromtimestamp(end_tm).strftime('%Y-%m-%d %H:%M:%S'))

        running_sec = round(end_tm - begin_tm, 2)
        System.line('Running time: '.ljust(16) + str(running_sec) + 's')

        System.line("\n")

    def _show_stat_transfers(self, transfers, stat_group):
        if not stat_group:
            self._show_stat_transfer_items(transfers)
        else:
            self._show_stat_transfer_groups(transfers)

        System.line('')

    def _show_stat_transfer_items(self, transfers):
        for key, value in transfers.items():
            (protocol, src_ip, src_port, dest_ip, dest_port) = key

            protocol_code = IPHeader.get_protocol_code(protocol)

            System.line('[' + protocol_code + '] ' + src_ip + ':' + str(src_port) + ' <-> ' + dest_ip + ':' + str(dest_port))

            self._show_subtotal(IPHeader.DIRECTION_SEND, value)
            self._show_subtotal(IPHeader.DIRECTION_RECEIVE, value)

            System.line('')

    def _show_stat_transfer_groups(self, transfers):
        for key, value in transfers.items():
            (protocol, src_ip, dest_ip, port) = key

            protocol_code = IPHeader.get_protocol_code(protocol)

            protocol_ips = '[' + protocol_code + '] ' + src_ip + ' <-> ' + dest_ip
            System.line(protocol_ips.ljust(40) + ' Port: ' + str(port))

            self._show_subtotal(IPHeader.DIRECTION_SEND, value)
            self._show_subtotal(IPHeader.DIRECTION_RECEIVE, value)
            System.line(' GROUPS:'.ljust(12) + str(value['group_count']))

            System.line('')

    def show_stopped(self):
        System.line(' Stopped by user...\n')

    def _show_subtotal(self, direction, subtotals):
        subtotal = subtotals[direction]

        direction_code = IPHeader.get_direction_code(direction)

        line = 'count: ' + str(subtotal['count']) + ', ' + 'unique: ' + str(subtotal['unique']) + ', ' + 'size: ' + str(subtotal['size'])
        System.line((' ' + direction_code + ':').ljust(12) + line)

    def show_version(self):
        System.exit(Constant.APP_NAME + ' by ' + Constant.PYPI_NAME + ' ' + __version__)

    def show_nofilters(self):
        System.exit('Any filters are not specified. Set any filter option or`--force` option.', True)

    def output_debug(self, ip_header, protocol_header):
        if not System.is_logging():
            return

        line = ip_header.src_ip + ':' + str(protocol_header.src_port) + '(' + str(
            ip_header.src_ip_int) + ') -> ' + ip_header.dest_ip + ':' + str(
            protocol_header.dest_port) + '(' + str(ip_header.dest_ip_int) + ')'
        line += ', PACKET_LEN: ' + str(ip_header.total_length) + ', ' + ip_header.protocol_code
        line += ', DATA _LEN: ' + str(protocol_header.payload_length)

        logging.log(logging.INFO, line)

    def output_not_support(self, eth_header):
        if System.is_logging():
            hex_data = self.get_hex_data(eth_header)

            System.output_data('NOT_SUPPORT_PACKET', hex_data, level=logging.DEBUG)

    def get_hex_data(self, data):
        hex_data = ''.join(f'{byte:02x} ' for byte in data)

        return hex_data

    def output_error(self, e):
        msg = ''

        if not System.is_logging(logging.DEBUG):
            msg = '\n\nSet `--debug` or `--verbose=3` option to output error detail.'

        if not isinstance(e, AppException):
            System.warn('An error has occurred.' + msg + '\n')
        else:
            System.warn(str(e) + msg + '\n')

    def get_border(self, length=120):
        return "\n" + '*' * length + "\n"
