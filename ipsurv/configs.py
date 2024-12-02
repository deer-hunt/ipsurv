from distutils.util import strtobool


class Constant:
    APP_NAME = 'ipsurv'

    APP_DESCRIPTION = '"IpSurv" is a command-line program for surveying IP addresses, host information, and more. Also "IpSurv" is extensible program by Python.'
    APP_BOTTOM_DESC = '''command example:
  ipsurv 192.168.1.100
  ipsurv 192.168.1.100 192.168.1.101
  ipsurv google.com wikipedia.org
  cat list.txt|ipsurv
  cat list.txt|ipsurv --format="hostname"
  cat list.txt|ipsurv --json=2
  cat /var/log/httpd/access_log|ipsurv --add_ip --no_original
  ipsurv self

documents:
  https://github.com/deer-hunt/ipsurv/
  There are several documents, including "Command arguments reference", "Command examples", and more.
'''

    ENV_ARGS_VAR = 'IPSURV_ARGS'
    ENV_CONF_VAR = 'IPSURV_CONF'

    MODE_SURVEY_IPS = 1
    MODE_SURVEY_SELF = 2

    STR_LOWER = 1
    STR_PASCAL = 2
    STR_UPPER = 3

    DELIMITER_DEFAULT = ','

    STATUS_EXIST = 'EXIST'
    STATUS_EMPTY = 'EMPTY'
    STATUS_RESOLVE_FAIL = 'RESOLVE_FAIL'
    STATUS_ILLEGAL_FORMAT = 'ILLEGAL_FORMAT'

    IP_TYPE_PRIVATE = 1
    IP_TYPE_PUBLIC = 2


class Config:
    PRE_ARGUMENTS = {
        'verbose': {'default': 0, 'type': int, 'help': 'Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]', 'choices': [0, 1, 2, 3]},
        'log': {'default': None, 'type': str, 'help': 'Verbose log filename.'},
        'disable_env': {'default': False, 'help': 'Disable to load env variable for args. Env name: `IPSURV_ARGS`.', 'action': 'store_true'}
    }

    APP_ARGUMENTS = {
        'resolve': {'default': True, 'type': strtobool, 'help': 'Resolve the name to IP if target value is domain or hostname automatically.'},
        'identify_int': {'default': False, 'help': 'Identify IP\'s int value.', 'action': 'store_true'},
        'autodetect': {'default': False, 'type': strtobool, 'help': 'Autodetect an IP or hostname that is included in the line. [Experimental]'},
        'begin': {'default': -1, 'type': int, 'help': 'Beginning from sequence number.'},
        'end': {'default': -1, 'type': int, 'help': 'Ending to sequence number.'},

        'collect': {'default': 'rdap;dnstxt;dnsreverse;ipinfo', 'type': str, 'help': 'Data collectors. See reference manual in detail. ex: rdap;dnstxt;dnsreverse;ipinfo'},
        'all_collect': {'default': False, 'help': 'All data collectors.', 'action': 'store_true'},
        'timeout': {'default': '8.0', 'type': str, 'help': 'Timeout seconds. Specify single value - ex: 1,3.2. Or specify values of each connection types. "dns,http,reactivity" - "3;5.1;6"'},

        'group': {'default': None, 'type': None, 'help': 'Grouping rule. ex: network, 24, 255.255.255.0'},
        'skip_duplicate': {'default': 0, 'type': int, 'help': 'Skip duplicate group. *2: It also skip checking server reactivity[icmp, tcp, udp].', 'choices': [0, 1, 2]},
        'range': {'default': '', 'type': str, 'help': 'Check whether IP is in IP/subnet ranges.  The value is CIDR notation. ex: "1.0.0.1/8;192.168.1.1/24"'},

        'format': {'default': 'default', 'type': None, 'help': 'Output format. Specify `Profile` or `Parameter`. See reference manual in detail. ex: simple, default, detail, heavy, geo, hostname etc.', 'action': 'StrAction'},
        'no_original': {'default': False, 'help': 'Cancel outputting the original line automatically.', 'action': 'store_true'},
        'sequence': {'default': False, 'help': 'Append sequence number.', 'action': 'store_true'},
        'add_ip': {'default': False, 'help': 'Append "ip" to the output format. For example, use when the target is a hostname, etc.', 'action': 'store_true'},
        'ident': {'default': False, 'help': 'Append identifier. Default identifier is ip.', 'action': 'store_true'},
        'enclose': {'default': None, 'type': str, 'help': 'Character of enclose in result line. If you specify "json" option, this option is disabled. ex: \'"\', "\'"'},
        'delimiter': {'default': None, 'type': str, 'help': 'Delimiter-char in result line.', 'action': 'StrAction'},
        'alt_delimiter': {'default': ';', 'type': str, 'help': 'Alternative delimiter character. If you specify "enclose" or "json" option, this option is disabled.', 'action': 'StrAction'},
        'headers': {'default': 0, 'type': int, 'help': 'Show headers. 1: LowerCase, 2: PascalCase, 3: UpperCase', 'choices': [0, 1, 2, 3]},
        'json': {'default': 0, 'type': int, 'help': 'Output JSON data. *2: Output formatted JSON.', 'choices': [0, 1, 2]},
        'json_list': {'default': False, 'help': 'Output JSON list. It makes it easier to parse JSON.', 'action': 'store_true'},
        'exhaustive': {'default': False, 'help': 'Output exhaustive internal values in JSON. Use with "json" option.', 'action': 'store_true'},

        'icmp': {'default': False, 'type': strtobool, 'help': 'Check ICMP.'},
        'tcp': {'default': 0, 'type': int, 'help': 'Check TCP port. Specify default port.'},
        'udp': {'default': 0, 'type': int, 'help': 'Check UDP port. Specify default port.'},
        'http': {'default': 0, 'type': int, 'help': 'Check HTTP response.', 'choices': [0, 1, 2]},

        'version': {'default': False, 'help': 'Show version information.', 'action': 'store_true'}
    }

    ENV_CONFS = ['ipinfo_token']

    FORMAT_PROFILES = {
        'ip': ['ip'],
        'hostname': ['hostname'],
        'country': ['country'],
        'org': ['org'],
        'address': ['address'],
        'timezone': ['timezone'],
        'network': ['cidr', 'network_start', 'network_end'],
        'geo': ['geo'],
        'system': ['ip_type', 'ip_int', 'ip_hex', 'ip_reversed'],
        'web': ['http', 'http_status', 'http_h2', 'http_time'],
        'simple': ['status', 'group', 'country'],
        'default': ['status', 'group', 'country', 'name', 'network_start', 'network_end'],
        'detail': ['status', 'group', 'country', 'name', 'handle', 'org', 'cidr', 'geo', 'address', 'description', 'hostname'],
        'heavy': ['status', 'group', 'country', 'timezone', 'name', 'handle', 'org', 'cidr', 'network_start', 'network_end', 'geo', 'address', 'description', 'hostname', 'errors']
    }

    FORMAT_PARAMS = [
        'success', 'status', 'requests', 'errors', 'identifier', 'identifier_int', 'target.*',
        'sequence', 'original', 'ip', 'ip_int', 'ip_hex', 'ip_reversed', 'port', 'ip_type', 'in_range',
        'group_int', 'group', 'group_found', 'group_status', 'network_start', 'network_end',
        'country', 'cidr',
        'rdap_time', 'port43', 'country_updated', 'name', 'handle', 'address', 'org', 'timezone', 'description',
        'dnstxt_time', 'rir',
        'dnsreverse_time', 'hostname',
        'ipinfo_time', 'geo', 'postal', 'city', 'region',
        'icmp', 'icmp_time', 'tcp', 'tcp_time', 'udp', 'udp_time',
        'http', 'http_time', 'http_status', 'http_size', 'http_h2'
    ]

    MASTER_DATA = {
        'success': False, 'status': '', 'requests': [], 'errors': [],
        'sequence': None, 'original': None, 'target': None, 'ip': None, 'ip_int': None, 'port': -1,
        'group_int': 0, 'group': '', 'group_found': False, 'group_status': '',
    }

    COLLECTORS = ['rdap', 'dnstxt', 'ipinfo', 'dnsreverse']

    HEAD_MSG_SELF = 'Self IP status by https://ipinfo.io'
