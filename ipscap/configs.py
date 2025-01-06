from ipscap.util.raw_socket_entity import TCPHeader


class Constant:
    PYPI_NAME = 'ipsurv'

    APP_NAME = 'ipscap'

    APP_DESCRIPTION = '`ipscap` captures "ICMP, TCP, UDP" packets. It supports filtering by various conditions, dumping file, displaying statistics.'
    APP_BOTTOM_DESC = '''command examples:
  ipscap --filter_port="80;53" --find="GET"
  ipscap --filter_port="80" --find="3\\d1"
  ipscap --find_hex="00 99 f0 e0 78 4e 23 70 a1"
  ipscap --find="HTTP" --tracking
  ipscap --filter_condition="port!=22"
  ipscap --filter_condition="port=80,443,53,-1" --filter_protocol=TCP,UDP,ICMP
  ipscap --filter_condition="src_port>=80;src_port<=500;flags=SYN,PSH"
  ipscap --filter_condition="ttl>=120"
  ipscap --output=HEADER
  ipscap --output=BYTE --filter_port="80,443"
  ipscap --output=LINE --filter_port="80,443"
  ipscap --stat_mode=2 --filter_protocol=TCP,UDP --output=NONE
  ipscap --filter_port=80,443 --stat_group=1
  ipscap --filter_port=80 --dumpfile=1
  ipscap --exclude_ssh
  ipscap --force


documents:
  Documentation site: https://deer-hunt.github.io/ipsurv/
  PyPI: https://pypi.org/project/ipsurv/
  Github: https://github.com/deer-hunt/ipsurv/
'''

    RECV_BUF_SIZE = 65565

    OUTPUT_NONE = 'NONE'
    OUTPUT_HEADER = 'HEADER'
    OUTPUT_TEXT = 'TEXT'
    OUTPUT_BINARY = 'BINARY'
    OUTPUT_HEX = 'HEX'
    OUTPUT_LINE = 'LINE'

    DUMPFILE_DIR = 'dump_logs'


class Config:
    PRE_ARGUMENTS = {
        'verbose': {'default': 0, 'type': int, 'help': 'Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]', 'choices': [0, 1, 2, 3]},
        'debug': {'default': False, 'help': '`--debug` is equivalent to `--verbose=3`.', 'action': 'store_true'},
        'log': {'default': None, 'type': str, 'help': 'Verbose log filename.', 'metavar': '{string}'}
    }

    APP_ARGUMENTS = {
        'find': {'default': '', 'help': 'Find character string by regex and ignoring case. ex: "3\\d1", "HTTP"', 'metavar': '{string}'},
        'find_case_sensitive': {'default': False, 'action': 'store_true', 'help': 'Find with case sensitivity.'},
        'find_hex': {'default': '', 'help': 'Find HEX data. ex: "00 99 f0 e0 78 4e 23 70 a1"', 'metavar': '{string}'},
        'filter_port': {'default': '', 'type': str, 'help': 'Filter port. It is source port or destination port. ex: =80, =53,80', 'metavar': '{int}'},
        'filter_protocol': {'default': 'TCP,UDP', 'type': str, 'help': 'Filter Protocol. Default: "TCP,UDP"', 'metavar': '[ICMP, TCP, UDP]'},
        'filter_ip': {'default': '', 'type': str, 'help': 'Filter IP. ex: =192.168.1.10, =192.168.1.10,192.168.1.20', 'metavar': '{string}'},
        'filter_condition': {'default': '', 'help': 'Filter by detail condition. ex: "src_port=80;dest_port<=30000;ttl=64;flags=SYN,PSH"', 'metavar': '{string}'},
        'tracking': {'default': False, 'action': 'store_true', 'help': 'Tracking transfers that have been matched by filters.'},
        'stat_mode': {'default': 1, 'type': int, 'help': 'Statistics mode.\n0: None, 1: Captured transfers, 2: All transfers', 'choices': [0, 1, 2]},
        'stat_group': {'default': 0, 'type': int, 'help': 'Group the transfer in statistics.\n0: None, 1: Grouping by IPs and service port, 2: Grouping by IPs', 'choices': [0, 1, 2]},
        'output': {'default': 'TEXT', 'help': 'Output mode about header and data. [Mode] or [0 - 5]\nNONE: \nHEADER: header only, TEXT: text data\nBINARY: binary data, HEX: hex data\nLINE: single line', 'metavar': '[NONE, HEADER, TEXT, BINARY, HEX, LINE]'},
        'dumpfile': {'default': 0, 'type': int, 'help': 'Dump data to files. Dir: `./dump_logs/`\n0: Off, 1: Dump data, 2: Dump headers and data', 'choices': [0, 1, 2]},
        'timeout': {'default': None, 'type': float, 'help': 'Stop automatically after the specified number of seconds.', 'metavar': '{float}'},

        'exclude_ssh': {'default': False, 'help': '`--exclude_ssh` is equivalent to `--filter_condition="port!=22"`.', 'action': 'store_true'},
        'web_port': {'default': False, 'help': '`--web_port` is equivalent to `--filter_port=80,443,53`.', 'action': 'store_true'},
        'general_port': {'default': False, 'help': '`--general_port` is equivalent to `--filter_port=21,22,23,25,53,80,110,143,220,443,465,990,993,995,1433,3306`.', 'action': 'store_true'},

        'force': {'default': False, 'help': 'Run force if any filter options aren\'t specified.', 'action': 'store_true'},
        'version': {'default': False, 'help': 'Show version information.', 'action': 'store_true'}
    }

    CONDITION_RULES = {
        'port': {'type': int},
        'client_port': {'type': int},
        'src_port': {'type': int},
        'dest_port': {'type': int},
        'ttl': {'type': int},
        'flags': {'type': lambda v: v.upper(), 'list': True, 'types': lambda codes: TCPHeader.get_flags(codes), 'single': True},
        'seq': {'type': int},
        'ack': {'type': int},
        'window': {'type': int},
        'mss': {'type': int},
        'wscale': {'type': int},
        'sack': {'type': int}
    }
