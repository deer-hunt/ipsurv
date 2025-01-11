# IpSurv

<div>

<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests-windows.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests-windows.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests-macos.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests-macos.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/lint.yml"><img alt="GitHub Actions build status (Lint)" src="https://github.com/deer-hunt/ipsurv/workflows/Lint/badge.svg"></a>
<a href="https://anaconda.org/conda-forge/ipsurv"> <img src="https://anaconda.org/conda-forge/ipsurv/badges/platforms.svg" /> </a>
<a href="https://codecov.io/gh/deer-hunt/ipsurv"><img alt="Coverage" src="https://codecov.io/github/deer-hunt/ipsurv/coverage.svg?branch=main"></a>
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/ipsurv">
<a href="https://github.com/deer-hunt/ipsurv/blob/main/LICENSE.md"><img alt="License - MIT" src="https://img.shields.io/pypi/l/ipsurv.svg"></a>
<a href="https://pypi.org/project/ipsurv/"><img alt="Newest PyPI version" src="https://img.shields.io/pypi/v/ipsurv.svg"></a>
<a href="https://anaconda.org/conda-forge/ipsurv"> <img src="https://anaconda.org/conda-forge/ipsurv/badges/version.svg" /></a>
<a href="https://pypi.org/project/ipsurv/"><img alt="Number of PyPI downloads" src="https://img.shields.io/pypi/dm/ipsurv.svg"></a>
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/deer-hunt/ipsurv">
<a href="https://pypi.org/project/ipsurv"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/ipsurv.svg"></a>
<a href="https://deer-hunt.github.io/ipsurv/" alt="IpSurv's documentation site"><img src="https://img.shields.io/badge/stable%20docs-github.io-brightgreen?style=flat&color=%2373DC8C&label=Docs"/></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fdeer-hunt%2Fipsurv?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdeer-hunt%2Fipsurv.svg?type=shield"/></a>

</div>

<div>
<img width="100" height="100" src="https://raw.githubusercontent.com/deer-hunt/ipsurv/main/docs/images/ipsurv-logo.png" align="left" />

```ipsurv``` is a command-line tool for surveying IP addresses, host information, and more. Additionally ```ipscap``` bundling tool is a packet capture tool that supports the ICMP, TCP, and UDP protocols. Each tools and internal program are extensible using Python.

</div>

<p>&nbsp;</p>

<img src="https://raw.githubusercontent.com/deer-hunt/ipsurv/main/docs/images/ipsurv.gif" alt="ipsurv visual image" width="100%" />

## Installation

**PyPI**

```bash
$ pip install ipsurv
or
$ pip3 install ipsurv
```

**Conda**

```
$ conda install conda-forge::ipsurv
```

> `ipscap` is also installed with it.


## Requirements

- ```python``` and ```pip``` command
- Python 3.0 or later version.

> If you use in Python 3.0 - 3.2, please run ```pip install ipaddress```.

> If you'd like to use in Python 2.7, you can refactor to Python 2.7 code easily. See "development_debug.md".


## Commands

| Command     | Description                                                                                             |
|----------|---------------------------------------------------------------------------------------------------------|
| `ipsurv` | `ipsurv` is surveying IP tool. You can conduct bulk surveys of specified IPs, URLs, and more. It also allows retrieving country codes for IP addresses, performing ping tests, and checking ports. |
| `ipscap` | `ipscap` is packet capture tool like `tcpdump` which supports "ICMP, TCP, UDP" protocols. `ipscap` has various filtering options, displays IP header and TCP header, and dumping files functions. <br><br>* `ipscap` must be executed as "root" user. And It does not support Windows.   |
| `ipsend` | Coming soon.   |

It’s best to refer to the help to recognize the functions.

```
$ ipsurv --help

# ipscap --help
```


## Documentation site

IpSurv's documentation site is [https://deer-hunt.github.io/ipsurv/](https://deer-hunt.github.io/ipsurv/).


## "ipsurv" command

`ipsurv` command reference is [here](./docs/ipsurv-cmd/README.md).

### Features

- Grouping by IP or Subnet.
- Skip duplicate by the group.
- Autodetect IP in line. Trying to resolve the name automatically.
- Autodetect delimiter-char.
- Customize output format. There are many format.
- Output JSON format.
- Show headers.
- Check ICMP, TCP, UDP, HTTP.
- Set timeout.
- Load env variable. And changing arguments and internal configures.
- Use GeoIP2 via IpSurv optionally.

> IPv6 is not supported.


### Usage

**Specify the target using Argument**

```bash
$ ipsurv 192.168.1.10
$ ipsurv 192.168.1.10 192.168.1.11
$ ipsurv test-example-sample-ipsurv.com --add_ip
$ ipsurv x.x.x.x --format=geo
```

**Specify the target using PIPE**

```bash
$ cat ips.txt|ipsurv
$ cat apache.log|ipsurv --add_ip
```

```bash
$ cat ./example_data/government.txt|ipsurv --sequence --add_ip
1,www.whitehouse.gov,192.0.66.168,OK,US,AUTOMATTIC,192.0.64.0,192.0.127.255
2,www.state.gov,3.165.39.61,OK,US,AMAZON-CF,3.165.0.0,3.165.255.255
3,www.treasury.gov,23.50.118.187,OK,US,AKAMAI,23.32.0.0,23.67.255.255
4,www.gov.uk,151.101.192.144,OK,US,SKYCA-3,151.101.0.0,151.101.255.255
```

**Output by JSON**

```
$ ipsurv wikipedia.org --format=default --json=2 --add_ip
{
  "original": "wikipedia.org",
  "ip": "103.102.166.224",
  "status": "OK",
  "group": "",
  "country": "US",
  "name": "WIKIMEDIA-AP",
  "network_start": "103.102.166.0",
  "network_end": "103.102.166.255"
}
```

**Format profile/parameters**

You can customize "Output Format" by ```--format``` option as follows. There are ```parameter - {}``` and ```profile - <>``` in ```--format```.
For more information, please read [--format description](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#format), [Profiles](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#profiles), [Parameters](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#parameters).

```
$ ipsurv github.io --format=heavy            # Profile
$ ipsurv github.io --format=simple           # Profile

$ ipsurv 8.8.8.8 --format="{status},{ip},{country},{address}"   # Parameters
```

**Check HTTP response**

```
$ ipsurv https://www.reddit.com --format="{ip},{http},{http_status},{http_size},{http_mime},{http_server},{http_h2},{http_time}" --http=1
https://www.reddit.com,151.101.129.140,HTTP_OK,200,707634,text/html,snooserv,N/A,130.2
```

**GeoIP**

```
$ ipsurv 8.8.8.8 --geoip_only
8.8.8.8,NA,North America,US,United States,America/Chicago,AS15169,37.751;-97.822
```


### Command options

```ipsurv``` have many options. Please read [Command arguments(.md) reference](https://github.com/deer-hunt/ipsurv/blob/main/docs/ipsurv/ipsurv-cmd/command_arguments.md).

```
[-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
[--disable_env] [--resolve {0,1}] [--identify_int]
[--autodetect] [--begin {number}] [--end {number}]
[--collect {string}] [--all_collect] [--timeout {string}]
[--group {string}] [--skip_duplicate {0,1,2}]
[--range {string}] [--format {string}] [--no_original]
[--sequence] [--add_ip] [--ident] [--enclose {string}]
[--delimiter {string}] [--alt_delimiter {string}]
[--headers {0,1,2,3}] [--json {0,1,2}] [--json_list]
[--exhaustive] [--icmp {0,1}] [--tcp {number}]
[--udp {number}] [--http {0,1,2}] [--json_all]
[--geoip_only] [--host_only] [--version]
[target [target ...]]
```


## "ipscap" command

`ipscap` command reference is [here](./docs/ipscap-cmd/README.md).

### Features

- Capture TCP, UDP, ICMP packets
- Show IP header values and protocol's header values.
- Output the binary data of headers in HEX format.
- Filter by strings or various criteria.
- Allows tracking matched transfers.
- Various output mode.
- Dump to files.

> IPv6 is not supported.


### Usage

```bash
# ipscap --exclude_ssh
# ipscap --force
  
# ipscap --port="80;53" --find="GET"
# ipscap --condition="port=80,443,53,-1" --protocol=TCP,UDP,ICMP
# ipscap --find="HTTP" --tracking

# ipscap --port=80,443 --stat_group=1
```

**Filterings**

```
# ipscap --find="HTTP/1.1 \d01"
# ipscap --find="http" --find_mode=MATCH
# ipscap --find="00 99 f0 e0 78 4e 23 70 a1" --find_mode=HEX
# ipscap --find="Accept-Ranges: bytes\r\n\r\n\x00\x00\x01\x00\x01\x00" --find_mode=BINARY
# ipscap --find="HTTP" --tracking
# ipscap --condition="port!=22"
# ipscap --condition="src_port>=80;src_port<=500;flags=SYN,PSH"
# ipscap --condition="ttl>=120"
```

**Dump files**

```bash
# ipscap --port=80 --dumpfile=1
```

```bash

# ipscap --output=HEADER # HEADER only
# ipscap --output=BINARY --port="80" # BINARY
# ipscap --output=LINE --port="80" #LINE
# ipscap --output=HEX --port="80" # HEX
```

**Capture 80 port**

```bash
# ipscap --port=80
Time:           2025-01-02 14:48:07.9597 / 1704200887.9597, Passage number: 2
IP header:      Version: 4, IP header length: 20, Packet length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1187996480, Acknowledgement: 2944002, Window: 29200, Flags: ['ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60684
Destination:    IP: 151.101.1.140             Port: 80
Direction:      SEND [ >>> ]
Data length:    0 byte
IP-H data:      45 00 00 28 43 54 40 00 40 06 52 7c 0a 00 02 0f 97 65 01 8c 
TCP-H data:     ed 0c 00 50 46 cf 63 40 00 2c ec 02 50 10 72 10 a5 1a 00 00 

Time:           2025-01-02 14:48:07.9599 / 1704200887.9599, Passage number: 3
IP header:      Version: 4, IP header length: 20, Packet length: 118, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1187996480, Acknowledgement: 2944002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60684
Destination:    IP: 151.101.1.140             Port: 80
Direction:      SEND [ >>> ]
Data length:    78 byte
IP-H data:      45 00 00 76 43 55 40 00 40 06 52 2d 0a 00 02 0f 97 65 01 8c 
TCP-H data:     ed 0c 00 50 46 cf 63 40 00 2c ec 02 50 18 72 10 a5 68 00 00 

GET / HTTP/1.1
User-Agent: curl/7.29.0
Host: www.reddit.com
Accept: */*
```

**Output line format**

```bash
# ipscap --port=80 --output=LINE
2025-01-02 14:55:55.7247, 1,  4, 20, 64, 60,      TCP, 40, 1165755664, 0, 29200,          ['SYN'],              0,      10.0.2.15:57910,         151.101.129.140:80,      SEND,          mss:1460;sack;nop;wscale:7
2025-01-02 14:55:55.7275, 1,  4, 20, 64, 44,      TCP, 24, 3072001, 1165755665, 65535,    ['SYN', 'ACK'],       2,      151.101.129.140:80,      10.0.2.15:57910,         RECEIVE,       mss:1460
2025-01-02 14:55:55.7277, 2,  4, 20, 64, 40,      TCP, 20, 1165755665, 3072002, 29200,    ['ACK'],              0,      10.0.2.15:57910,         151.101.129.140:80,      SEND,          -
2025-01-02 14:55:55.7278, 3,  4, 20, 64, 118,     TCP, 20, 1165755665, 3072002, 29200,    ['PSH', 'ACK'],       78,     10.0.2.15:57910,         151.101.129.140:80,      SEND,          -
2025-01-02 14:55:55.7278, 2,  4, 20, 64, 40,      TCP, 20, 3072002, 1165755743, 65535,    ['ACK'],              6,      151.101.129.140:80,      10.0.2.15:57910,         RECEIVE,       -
2025-01-02 14:55:55.7322, 3,  4, 20, 64, 982,     TCP, 20, 3072002, 1165755743, 65535,    ['PSH', 'ACK'],       942,    151.101.129.140:80,      10.0.2.15:57910,         RECEIVE,       -
2025-01-02 14:55:55.7324, 4,  4, 20, 64, 40,      TCP, 20, 1165755743, 3072944, 30144,    ['ACK'],              0,      10.0.2.15:57910,         151.101.129.140:80,      SEND,          -
2025-01-02 14:55:55.7325, 5,  4, 20, 64, 40,      TCP, 20, 1165755743, 3072944, 30144,    ['FIN', 'ACK'],       0,      10.0.2.15:57910,         151.101.129.140:80,      SEND,          -
2025-01-02 14:55:55.7326, 4,  4, 20, 64, 40,      TCP, 20, 3072944, 1165755743, 65535,    ['FIN', 'ACK'],       6,      151.101.129.140:80,      10.0.2.15:57910,         RECEIVE,       -
2025-01-02 14:55:55.7327, 6,  4, 20, 64, 40,      TCP, 20, 1165755744, 3072945, 30144,    ['ACK'],              0,      10.0.2.15:57910,         151.101.129.140:80,      SEND,          -
2025-01-02 14:55:55.7327, 5,  4, 20, 64, 40,      TCP, 20, 3072944, 1165755744, 65535,    ['FIN', 'ACK'],       6,      151.101.129.140:80,      10.0.2.15:57910,         RECEIVE,       -
```

**Output HEX**

```bash
# ipscap --port=80 --output=HEX
Time:           2025-01-02 22:29:48 / 1735787388.957, Passage number: 3
IP header:      Version: 4, IP header length: 20, Packet length: 978, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 67904002, Acknowledgement: 172468636, Window: 65535, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 151.101.129.140           Port: 80
Destination:    IP: 10.0.2.15                 Port: 52386
Direction:      RECEIVE [ <<< ]
Data length:    938 byte
IP-H data:      45 00 03 d2 3e a6 00 00 40 06 13 80 97 65 81 8c 0a 00 02 0f 
TCP-H data:     00 50 cc a2 04 0c 22 02 0a 47 a9 9c 50 18 ff ff 06 2f 00 00 

48 54 54 50 2f 31 2e 31 20 33 30 31 20 52 65 64 69 72 65 63 74 0d 0a 44 61 74 65 3a 20 53 61 74 2c 20 31 31 20 4a 61 6e 20 32 30 32 35 20 31 32 3a 34 35 3a 34 36 20 47 4d 54 0d 0a 
43 6f 6e 6e 65 63 74 69 6f 6e 3a 20 6b 65 65 70 2d 61 6c 69 76 65 0d 0a 43 61 63 68 65 2d 43 6f 6e 74 72 6f 6c 3a 20 6e 6f 2d 73 74 6f 72 65 0d 0a 4c 6f 63 61 74 69 6f 6e 3a 20 68 74
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
4c 61 6e 67 75 61 67 65 3a 20 65 6e 0d 0a 41 63 63 65 70 74 2d 43 48 3a 20 53 65 63 2d 43 48 2d 55 41 2d 46 75 6c 6c 2d 56 65 72 73 69 6f 6e 2d 4c 69 73 74 2c 20 53 65 63 2d 43
72 63 68 3d 2a 0d 0a 50 65 72 6d 69 73 73 69 6f 6e 73 2d 50 6f 6c 69 63 79 3a 20 75 6e 6c 6f 61 64 3d 28 29 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 65 6e 67 74 68 3a 20 31 0d 0a 0d 0a 20 
```


### Command options

```
[-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
[--find {string}] [--find_mode [REGEX, MATCH, BINARY, HEX]]
[--port {int}] [--protocol [ICMP, TCP, UDP]]
[--ip {string}] [--condition {string}] [--tracking]
[--stat_mode {0,1,2}] [--stat_group {0,1,2}]
[--output [NONE, HEADER, TEXT, BINARY, HEX, LINE]]
[--dumpfile {0,1,2}] [--timeout {float}] [--exclude_ssh]
[--web_port] [--general_port] [--force] [--version]
```

## Path summary

| Directory        | Description                                         |
|-----------------------|-----------------------------------------------------|
| `.github`            | GitHub Actions files          |
| `docs`               | Documentation files                                 |
| `example_data`       | Sample data files for testing                       |
| `examples`           | Example programs                 |
| `ipscap`             | ipscap package/Sources                            |
| `ipsurv`             | Main package/Sources                            |
| `tests`              | Test files                     |


## Debugging

In verbose mode, outputting internal data and behaviors in detail.

```bash
$ ipsurv ***** --verbose=2    #INFO
$ ipsurv ***** --verbose=3    #DEBUG

$ ipsurv ***** --debug     #DEBUG  This option is equivalent to "--verbose=3"
```

```bash
# ipscap ***** --verbose=2    #INFO
# ipscap ***** --verbose=3    #DEBUG

# ipscap ***** --debug     #DEBUG  This option is equivalent to "--verbose=3"
```


## Dependencies

- [dnspython](https://github.com/rthalley/dnspython)
- [geoip2](https://github.com/maxmind/GeoIP2-python) [Optional]

