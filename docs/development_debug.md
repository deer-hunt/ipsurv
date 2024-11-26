# [IpSurv] Development and Debugging

## Overview

This is description of development related "IpSurv".
You are able to customize "IpSurv".


## Program specification

| **Item**          | **Description**            |
|-------------------|-----------------------|
| **Python version**| 3.0 or later. * |
| **Dependencies**   | dnspython              |

*: "IpSurv" doesn't support Python 2.7, However it's easy to refactor to Python 2.7. See the bottom of this document.


## Program Architecture and Classes

Please read [Program Architecture and Classes(.md)](program_architecture_classes.md). There are description of several important classes.


## Customizing and Examples

Please read [Customizing and Examples(.md)](customize_examples.md). There are some example programs.


## Debugging

You can see detailed debug information by specifying `--verbose=3`. In detail, please read `--verbose` option in [Command Arguments(.md)](command_arguments.md).


### Log sample and description

The following is debugging log with each comments.

```
Enable verbose mode. Current:3 [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]          // Displaying verbose level.
2024-10-26 23:26:03,193 - INFO - ENV(IPSURV_ARGS):          // "Command arguments" by Environment variable.
{}
2024-10-26 23:26:03,193 - INFO - ENV(IPSURV_CONF):         // "Internal configures" by Environment variable.
{}
2024-10-26 23:26:03,193 - INFO - ARGUMENTS:            // Arguments with default value.
{ 'all_collect': False,
  'alt_delimiter': ';',
  'autodetect': False,
  'begin': -1,
  'collect': 'rdap;dnstxt;dnsreverse;ipinfo',
  'delimiter': None,
  'disable_env': False,
  'enclose': None,
  'end': -1,
  'exhaustive': False,
  'format': 'default',
  'group': None,
  'headers': 0,
  'http': 0,
  'icmp': False,
  'json': 0,
  'log': None,
  'original': True,
  'resolve': True,
  'sequence': False,
  'skip_duplicate': 0,
  'target': [],
  'tcp': 0,
  'timeout': '8.0',
  'udp': 0,
  'verbose': 3,
  'version': False}
2024-10-26 23:26:03,194 - INFO - ARGUMENTS_JSON:          // Arguments JSON. You can use as environment variable.
{"verbose": 3, "log": null, "disable_env": false, "target": [], "resolve": true, ~~~~~~~~~~~~~~~~ "icmp": false, "tcp": 0, "udp": 0, "http": 0, "version": false}
//"Fixed ~~~" are values which generating by arugment value for internal process.
2024-10-26 23:26:03,194 - INFO - Fixed delimiter:,
2024-10-26 23:26:03,194 - INFO - Fixed format:{original},{status},{group},{country},{name},{network_start},{network_end},{hostname}
2024-10-26 23:26:03,195 - INFO - Fixed timeout:{'dns': 8.0, 'http': 8.0, 'reactivity': 8.0}
2024-10-26 23:26:03,195 - INFO - Fixed enclose:
2024-10-26 23:26:03,195 - INFO - Fixed collectors:['rdap', 'dnstxt', 'dnsreverse', 'ipinfo']
2024-10-26 23:26:03,195 - INFO - MODE:SURVEY_IPS          // Detected Mode.
2024-10-26 23:26:03,219 - INFO - IP:192.0.66.168          // Target IP
2024-10-26 23:26:03,219 - INFO - FQDN:www.whitehouse.gov          // FQDN
2024-10-26 23:26:03,220 - INFO - PORT:None          // port
2024-10-26 23:26:03,220 - DEBUG - TARGET_RAW:www.whitehouse.gov          // Raw
2024-10-26 23:26:03,220 - INFO - TARGET_IDENTIFIER:192.0.66.168          // Target identifier value.
2024-10-26 23:26:03,220 - INFO - TARGET_DATA:          // Target data values.
{ 'fqdn': 'www.whitehouse.gov',
  'identifier': '192.0.66.168',
  'identifier_int': 3221242536,
  'ip': '192.0.66.168',
  'port': None,
  'raw': 'www.whitehouse.gov',
  'status': 'EXIST',
  'url': None}
2024-10-26 23:26:03,221 - INFO - REQUEST RDAP...           // Start requesting RDAP.
2024-10-26 23:26:03,239 - INFO - RDAP_URL:https://rdap.arin.net/registry/ip/192.0.66.168
2024-10-26 23:26:03,783 - DEBUG - RDAP_DATA:          // Response data.
{ 'arin_originas0_originautnums': [2635],
  'cidr': '192.0.64.0/18',
  'cidr0_cidrs': [{'length': 18, 'v4prefix': '192.0.64.0'}],
  'country': 'US',
  'country_updated': True,
  'endAddress': '192.0.127.255',
  'entities': [ { 'entities': [ { 'events': [ { 'eventAction': 'last changed',
                                                'eventDate': '2024-08-22T09:08:56-04:00'},
                                              { 'eventAction': 'registration',
                                                'eventDate': '2011-10-04T02:07:42-04:00'}],
                                  'handle': 'NOC12276-ARIN',
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  'remarks': [ { 'description': ['Geofeed https://as2635.network/geofeed.csv'],
                 'title': 'Registration Comments'}],
  'startAddress': '192.0.64.0',
  'status': ['active'],
  'type': 'DIRECT ALLOCATION'}
2024-10-26 23:26:03,784 - INFO - RDAP:OK          // Response status.
2024-10-26 23:26:03,784 - INFO - RDAP_TIME(ms):558.4          // Response time.
2024-10-26 23:26:03,784 - DEBUG - UNNECESSARY:DNSTXT          // Skip unnecessary requesting.
2024-10-26 23:26:03,784 - INFO - REQUEST DNSREVERSE...          // Start requesting DNSREVERSE.
2024-10-26 23:26:03,811 - DEBUG - DNSREVERSE ERROR          // Response error - Unknown host. This error is not a bug.
Traceback (most recent call last):
  File "/usr/local/~~~/ipsurv/data_collector/data_collector.py", line 32, in request
    (success, response) = self.request_data(target)
  File "/usr/local/~~~/ipsurv/data_collector/basic_collectors.py", line 116, in request_data
    return self.requester.request_reverse(target.ip)
  File "/usr/local/~~~/ipsurv/requester/dns_resolver.py", line 31, in request_reverse
    hostname = DnsUtil.reverse(ip, timeout=self.timeout)
  File "/usr/local/~~~/ipsurv/util/network_util.py", line 48, in reverse
    cls._run(thread, timeout)
  File "/usr/local/~~~/ipsurv/util/network_util.py", line 61, in _run
    raise thread.e
  File "/usr/local/~~~/ipsurv/util/network_util.py", line 97, in run
    vals = socket.gethostbyaddr(self.ip)
socket.herror: [Errno 1] Unknown host
2024-10-26 23:26:03,811 - DEBUG - DNSREVERSE_DATA:          // Response data.
{'error': '[Errno 1] Unknown host'}
2024-10-26 23:26:03,811 - INFO - DNSREVERSE:NG          // Response status.
2024-10-26 23:26:03,811 - INFO - DNSREVERSE_TIME(ms):26.7          // Response time.
2024-10-26 23:26:03,811 - INFO - REQUEST IPINFO...                                 // Start requesting IPINFO.
2024-10-26 23:26:03,824 - INFO - IPINFO_URL:https://ipinfo.io/192.0.66.168/json?
2024-10-26 23:26:04,477 - DEBUG - IPINFO_DATA:          // Response data.
{ 'anycast': True,
  'city': 'San Francisco',
  'country': 'US',
  'ip': '192.0.66.168',
  'loc': '37.7749,-122.4194',
  'org': 'AS2635 Automattic, Inc',
  'postal': '94102',
  'readme': 'https://ipinfo.io/missingauth',
  'region': 'California',
  'timezone': 'America/Los_Angeles'}
2024-10-26 23:26:04,477 - INFO - IPINFO:OK          // Response status.
2024-10-26 23:26:04,477 - INFO - IPINFO_TIME(ms):665.4          // Response time.
2024-10-26 23:26:04,478 - INFO - COLLECTED_DATA:          // Collected data.
{ 'address': '60 29th Street #343 San Francisco CA 94110 United States',
  'cidr': '192.0.64.0/18',
  'city': 'San Francisco',
  'country': 'US',
  'country_updated': True,
  'description': 'Geofeed https://as2635.network/geofeed.csv',
  'dnsreverse_time': 26.7,
  'errors': ['[Errno 1] Unknown host'],
  'geo': '37.7749,-122.4194',
  'group': '',
  'group_found': False,
  'group_int': 0,
  'group_status': '-',
  'handle': 'AUTOM-93',
  'hostname': '',
  'identifier': '192.0.66.168',
  'identifier_int': 3221242536,
  'ip': '192.0.66.168',
  'ip_int': 3221242536,
  'ipinfo_time': 665.4,
  'name': 'AUTOMATTIC',
  'network_end': '192.0.127.255',
  'network_start': '192.0.64.0',
  'org': 'AS2635 Automattic, Inc',
  'original': 'www.whitehouse.gov',
  'port': None,
  'port43': 'whois.arin.net',
  'postal': '94102',
  'rdap_time': 558.4,
  'region': 'California',
  'requests': ['RDAP', 'DNSREVERSE', 'IPINFO'],
  'sequence': 1,
  'status': 'NG',
  'success': False,
  'target': '192.0.66.168',
  'target.fqdn': 'www.whitehouse.gov',
  'target.identifier': '192.0.66.168',
  'target.identifier_int': 3221242536,
  'target.ip': '192.0.66.168',
  'target.port': None,
  'target.raw': 'www.whitehouse.gov',
  'target.status': 'EXIST',
  'target.url': None,
  'timezone': 'America/Los_Angeles'}
2024-10-26 23:26:04,478 - DEBUG - REQUESTS:          // Requested collectors except skipped collectors.
['RDAP', 'DNSREVERSE', 'IPINFO']
```


## Not support Python 2.7 ?

"IpSurv" doesn't support Python 2.7. However "IpSurv" has been developed to avoid using the latest Python specifications as much as possible, So you can refactor to Python 2.7 code easily.

**Refactoring points**

- ABC module
- http.client module
- urllib module

> And any other few modules.

