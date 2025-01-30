

class Constant:
    PYPI_NAME = 'ipsurv'

    APP_NAME = 'ipsend'

    APP_DESCRIPTION = '`ipsend` is a network transmission tool that supports TCP, SSL, UDP, and Raw sockets, as well as interactive transmission.'
    APP_BOTTOM_DESC = '''command examples:
  ipsend --mode=TCP --dest=google.com --port=80 --interactive=1
  ipsend --dest=google.com --http -I
  ipsend --dest=google.com --port=80 --interactive=2
  ipsend "GET /index.html HTTP/1.1\\n" --dest=google.com --http
  ipsend "GET / HTTP/1.1\\n" --dest=google.com --https
  ipsend --dest=google.com --https -I --output=BASE64
  ipsend --mode=UDP --dest=8.8.8.8 --port=53
  ipsend --mode=TCP --dest=wikipedia.org --http -I --output=BINARY

  ipsend --mode=SSL --dest=google.com --port=443 -I
  ipsend --mode=SSL --dest=google.com --https -I --output=BINARY
  ipsend --mode=SSL --dest=google.com --https -I --ssl_context=TLS1.2

  ipsend '47 45 54 20 2f 69 6e 64 65 78 2e 68 74 6d 6c 20 48 54 54 50 2f 31 2e 31 0a 0a 0a' --mode=TCP --dest=172.217.31.174 --port=80 --input=HEX
  ipsend 'R0VUIC9pbmRleC5odG1sIEhUVFAvMS4xCkhvc3Q6IHd3dy5nb29nbGUuY29tCgo=' --mode=TCP --dest=172.217.31.174 --port=80 --input=BASE64

  ipsend '\\xaa\\x1e\\x00P\\xc9\\x94o"\\x005\\xb6\\x02P\\x18r\\x10y}\\x00\\x00GET / HTTP/1.1\\r\\nAccept: */*\\r\\n\\r\\n' --mode=TCP_HEADER --dest=google.com --input=BINARY
  ipsend '\\xaa\\x1e\\x00P\\xc9\\x94o"\\x005\\xb6\\x02P\\x18r\\x10y}\\x00\\x00GET / HTTP/1.1\\r\\nHost: google.com\\r\\n\\r\\n' --mode=TCP_HEADER --dest=172.217.31.174 --input=binary

documents:
  Documentation site: https://deer-hunt.github.io/ipsurv/
  PyPI: https://pypi.org/project/ipsurv/
  Github: https://github.com/deer-hunt/ipsurv/
'''

    RECV_BUF_SIZE = 65565

    MODE_TCP = 'TCP'
    MODE_UDP = 'UDP'
    MODE_SSL = 'SSL'
    MODE_IP_HEADER = 'IP_HEADER'
    MODE_TCP_HEADER = 'TCP_HEADER'
    MODE_UDP_HEADER = 'UDP_HEADER'
    MODE_ICMP_HEADER = 'ICMP_HEADER'
    MODE_IP_PAYLOAD = 'IP_PAYLOAD'
    MODE_TCP_PAYLOAD = 'TCP_PAYLOAD'
    MODE_UDP_PAYLOAD = 'UDP_PAYLOAD'
    MODE_ICMP_PAYLOAD = 'ICMP_PAYLOAD'

    RICH_SOCKET_MODES = [MODE_TCP, MODE_UDP, MODE_SSL]
    RAW_SOCKET_MODES = [MODE_IP_HEADER, MODE_TCP_HEADER, MODE_UDP_HEADER, MODE_ICMP_HEADER, MODE_TCP_PAYLOAD, MODE_UDP_PAYLOAD, MODE_ICMP_PAYLOAD]
    PAYLOAD_MODES = [MODE_TCP_PAYLOAD, MODE_UDP_PAYLOAD, MODE_ICMP_PAYLOAD]

    INPUT_HEADER = 'HEADER'
    INPUT_TEXT = 'TEXT'
    INPUT_BINARY = 'BINARY'
    INPUT_HEX = 'HEX'
    INPUT_BASE64 = 'BASE64'

    OUTPUT_NONE = 'NONE'
    OUTPUT_TEXT = 'TEXT'
    OUTPUT_BINARY = 'BINARY'
    OUTPUT_HEX = 'HEX'
    OUTPUT_BASE64 = 'BASE64'

    SSL_CONTEXTS = {
        'sslv3': 'PROTOCOL_SSLv3',
        'tls1.0': 'PROTOCOL_TLSv1',
        'tls1.1': 'PROTOCOL_TLSv1_1',
        'tls1.2': 'PROTOCOL_TLSv1_2',
        'tls1.3': 'PROTOCOL_TLSv1_3'
    }

    RICH_SOCKET_OPTIONS = [
        'interactive', 'ssl_context'
    ]

    RAW_SOCKET_OPTIONS = [
        'ip_flags',
        'ip_identification',
        'ip_ttl',
        'ip_protocol',
        'src_ip',
        'src_port',
        'tcp_flags',
        'tcp_seq',
        'tcp_ack',
        'tcp_window',
        'icmp_type',
        'icmp_code',
        'icmp_id',
        'icmp_seq',
    ]

    SSL_OPTIONS = [
        'ssl_context'
    ]

    DUMPFILE_DIR = 'dump_logs'


class Config:
    PRE_ARGUMENTS = {
        'verbose': {'default': 0, 'type': int, 'help': 'Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]', 'choices': [0, 1, 2, 3]},
        'debug': {'default': False, 'help': '`--debug` is equivalent to `--verbose=3`.', 'action': 'store_true'},
        'log': {'default': None, 'type': str, 'help': 'Verbose log filename.', 'metavar': '{string}'}
    }

    ARGUMENTS = {
        'data': {'default': '', 'type': str, 'help': 'Send-data in INSTANT mode. Not available in INTERACTIVE mode.', 'nargs': '?'},

        'mode': {'default': 'TCP', 'type': str.upper, 'help': 'Transmission mode. Default: TCP', 'choices': ['TCP', 'UDP', 'SSL', 'IP_HEADER', 'TCP_HEADER', 'UDP_HEADER', 'ICMP_HEADER', 'IP_PAYLOAD', 'TCP_PAYLOAD', 'UDP_PAYLOAD', 'ICMP_PAYLOAD']},
        'input': {'default': 'TEXT', 'type': str.upper, 'help': 'Input format. Default: TEXT', 'choices': ['TEXT', 'BINARY', 'HEX', 'BASE64']},
        'output': {'default': 'TEXT', 'type': str.upper, 'help': 'Output format. Default: TEXT', 'choices': ['NONE', 'TEXT', 'BINARY', 'HEX', 'BASE64']},
        'interactive': {'default': 0, 'type': int, 'help': 'Enable INTERACTIVE mode.\n[1: Line-break to send, 2: Ctrl-key to send]', 'metavar': '{int}'},
        'ssl_context': {'default': None, 'type': str.upper, 'help': 'SSL context. [SSLv3, TLS1.0, TLS1.1, TLS1.2, TLS1.3]', 'choices': ['SSLV3', 'TLS1.0', 'TLS1.1', 'TLS1.2', 'TLS1.3']},
        'output_send': {'default': 0, 'type': int, 'help': 'Output Send-data in INSTANT mode. [1: Output & Send, 2: Only output]', 'metavar': '{int}'},
        'auto_lb': {'default': True, 'type': bool, 'help': 'Append Line-break in INSTANT mode and `TEXT` input format.', 'metavar': '{bool}'},

        'dest': {'default': '', 'type': str, 'help': 'Destination IP or Hostname.', 'metavar': '{string}'},
        'port': {'default': 0, 'type': int, 'help': 'Destination port.', 'metavar': '{int}'},
        'timeout': {'default': 30.0, 'type': float, 'help': 'Timeout. Default: 30.0', 'metavar': '{float}'},
        'dumpfile': {'default': False, 'help': 'Dump response data to files. Dir: `./dump_logs/`', 'action': 'store_true'},

        'ip_flags': {'default': 0, 'type': int, 'help': 'IP flags.', 'group': 'header', 'metavar': '{int}'},
        'ip_identification': {'default': 0, 'type': int, 'help': 'IP identification.', 'group': 'header', 'metavar': '{int}'},
        'ip_ttl': {'default': 64, 'type': int, 'help': 'IP TTL.', 'group': 'header', 'metavar': '{int}'},
        'ip_protocol': {'default': 6, 'type': int, 'help': 'IP Protocol number.', 'group': 'header', 'metavar': '{int}'},
        'src_ip': {'default': '', 'type': str, 'help': 'Source IP.', 'group': 'header', 'metavar': '{int}'},
        'src_port': {'default': 0, 'type': int, 'help': 'Source port.', 'group': 'header', 'metavar': '{int}'},
        'dest_ip': {'default': '', 'type': str, 'help': 'Destination IP.', 'group': 'header', 'metavar': '{int}'},
        'dest_port': {'default': 0, 'type': int, 'help': 'Destination port.', 'group': 'header', 'metavar': '{int}'},

        'tcp_flags': {'default': '', 'type': str.upper, 'help': 'TCP flags. ex: FIN,SYN,RST,PSH,ACK', 'group': 'header', 'metavar': '{str}'},
        'tcp_seq': {'default': 0, 'type': int, 'help': 'TCP sequence number.', 'group': 'header', 'metavar': '{int}'},
        'tcp_ack': {'default': 0, 'type': int, 'help': 'TCP acknowledgment number.', 'group': 'header', 'metavar': '{int}'},
        'tcp_window': {'default': 0, 'type': int, 'help': 'TCP window size.', 'group': 'header', 'metavar': '{int}'},

        'icmp_type': {'default': 0, 'type': int, 'help': 'ICMP type.', 'group': 'header', 'metavar': '{int}'},
        'icmp_code': {'default': 0, 'type': int, 'help': 'ICMP code.', 'group': 'header', 'metavar': '{int}'},
        'icmp_id': {'default': 0, 'type': int, 'help': 'ICMP identifier.', 'group': 'header', 'metavar': '{int}'},
        'icmp_seq': {'default': 0, 'type': int, 'help': 'ICMP sequence number.', 'group': 'header', 'metavar': '{int}'},

        'I': {'shorten': True, 'default': False, 'help': '`-I` is equivalent to `--interactive=1`.', 'action': 'store_true', 'group': 'shortcut'},
        'http': {'default': False, 'help': '`--http` is equivalent to `--port=80`.', 'action': 'store_true', 'group': 'shortcut'},
        'https': {'default': False, 'help': '`--https` is equivalent to `--port=443 --mode=SSL`.', 'action': 'store_true', 'group': 'shortcut'},

        'quiet': {'default': False, 'help': 'Hide conditions.', 'action': 'store_true'},
        'version': {'default': False, 'help': 'Show version information.', 'action': 'store_true'}
    }

    ARGUMENTS_GROUP_NAMES = {
        'header': 'Header mode',
        'shortcut': 'Shortcut'
    }
