# Introduction to "ipscap"

`ipscap` captures "ICMP, TCP, UDP" packets. It supports filtering by various conditions, dumping file, displaying statistics.

### Features of `ipscap`

- Capture TCP, UDP, ICMP packets
- Show IP header values and protocol's header values.
- Output the binary data of headers in HEX format.
- Filter by strings or various criteria.
- Allows tracking matched transfers.
- Various output mode.
- Dump to files.

> IPv6 is not supported.

## Usage

**Options**

```bash
ipscap [-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
			[--find {string}] [--find_mode [REGEX, MATCH, BINARY, HEX]]
			[--port {int}] [--protocol [ICMP, TCP, UDP]]
			[--ip {string}] [--condition {string}] [--tracking]
			[--stat_mode {0,1,2}] [--stat_group {0,1,2}]
			[--output [NONE, HEADER, TEXT, BINARY, HEX, LINE]]
			[--dumpfile {0,1,2}] [--timeout {float}] [--exclude_ssh]
			[--web_port] [--general_port] [--force] [--version]
```

## Optional Arguments

| Option                          | Description                                                                                   |
|---------------------------------|-----------------------------------------------------------------------------------------------|
| -h, --help                      | Show this help message and exit.                                                             |
| --verbose {0,1,2,3}             | Verbose mode. <br><br> [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]                                 |
| --debug                         | `--debug` is equivalent to `--verbose=3`.                                                    |
| --log {string}                 | Verbose log filename.                                                                         |
| --find {string}                | Find character string by regex and ignoring case. <br> ex: "3\d1", "HTTP"                   |
| --find_mode [REGEX, MATCH, BINARY, HEX] | Find mode. [Mode name] or [1 - 4]                                                  |
| --port {int}                   | Filter port. <br> It is source port or destination port. <br> ex: =80, =53,80                |
| --protocol [ICMP, TCP, UDP]    | Filter Protocol. <br> Default: "TCP,UDP"                                                    |
| --ip {string}                  | Filter IP. <br> ex: =192.168.1.10, =192.168.1.10,192.168.1.20                              |
| --condition {string}           | Filter by detail condition. <br> ex: "src_port=80;dest_port<=30000;ttl=64;flags=SYN,PSH" |
| --tracking                     | Tracking transfers that have been matched by filters.                                         |
| --stat_mode {0,1,2}            | Statistics mode. <br><br>0: None, <br> 1: Captured transfers, <br> 2: All transfers            |
| --stat_group {0,1,2}           | Group the transfer in statistics. <br><br> 0: None, <br> 1: Grouping by IPs and service port, <br> 2: Grouping by IPs |
| --output [NONE, HEADER, TEXT, BINARY, HEX, LINE] | Output mode about header and data. [Mode name] or [0 - 5]<br><br>NONE: none, <br> HEADER: header only, <br> TEXT: text data <br> BINARY: binary data, <br> HEX: hex data <br> LINE: single line |
| --dumpfile {0,1,2}             | Dump data to files. <br><br> Dir: `./dump_logs/` <br> 0: Off, <br> 1: Dump data, <br> 2: Dump headers and data |
| --timeout {float}              | Stop automatically after the specified number of seconds.                                     |
| --exclude_ssh                  | `--exclude_ssh` is equivalent to `--condition="port!=22"`.                                   |
| --web_port                     | `--web_port` is equivalent to `--port=80,443,53`.                                            |
| --general_port                 | `--general_port` is equivalent to `--port=21,22,23,25,53,80,110,143,220,443,465,990,993,995,1433,3306`. |
| --force                        | Run force if any filter options aren't specified.                                              |
| --version                      | Show version information.                                                                      |


## Command Examples

```bash
# ipscap --port="80;53" --find="GET"
# ipscap --port="80" --find="3\d1"
# ipscap --find="HTTP/1.1 \d01"
# ipscap --find="http" --find_mode=MATCH
# ipscap --find="00 99 f0 e0 78 4e 23 70 a1" --find_mode=HEX
# ipscap --find="Accept-Ranges: bytes\r\n\r\n\x00\x00\x01\x00\x01\x00" --find_mode=BINARY
# ipscap --find="HTTP" --tracking
# ipscap --condition="port!=22"
# ipscap --condition="port=80,443,53,-1" --protocol=TCP,UDP,ICMP
# ipscap --condition="src_port>=80;src_port<=500;flags=SYN,PSH"
# ipscap --condition="ttl>=120"
# ipscap --stat_mode=2 --protocol=TCP,UDP --output=NONE
# ipscap --port=80,443 --stat_group=1
# ipscap --port=80 --dumpfile=1
# ipscap --exclude_ssh
# ipscap --force
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
Time:           2025-01-03 22:34:35.7259 / 1735863240.7259, Passage number: 2
IP header:      Version: 4, IP header length: 20, Packet length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 3577694814, Acknowledgement: 68032002, Window: 29200, Flags: ['ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 50396
Destination:    IP: 103.102.166.224           Port: 80
Direction:      SEND [ >>> ]
Data length:    0 byte
IP-H data:      45 00 00 28 cb 64 40 00 40 06 55 16 0a 00 02 0f 67 66 a6 e0 
TCP-H data:     c4 dc 00 50 d5 3f 4a 5e 04 0e 16 02 50 10 72 10 1a 70 00 00 

Time:           2025-01-03 22:34:35.7262 / 1735863240.7262, Passage number: 3
IP header:      Version: 4, IP header length: 20, Packet length: 117, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 3577694814, Acknowledgement: 68032002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 50396
Destination:    IP: 103.102.166.224           Port: 80
Direction:      SEND [ >>> ]
Data length:    77 byte
IP-H data:      45 00 00 75 cb 65 40 00 40 06 54 c8 0a 00 02 0f 67 66 a6 e0 
TCP-H data:     c4 dc 00 50 d5 3f 4a 5e 04 0e 16 02 50 18 72 10 1a bd 00 00 

GET / HTTP/1.1
User-Agent: curl/7.29.0
Host: wikipedia.org
Accept: */*


Time:           2025-01-03 22:34:35.7263 / 1735863240.7263, Passage number: 2
IP header:      Version: 4, IP header length: 20, Packet length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 68032002, Acknowledgement: 3577694891, Window: 65535, Flags: ['ACK']
TCP options:    -
Source:         IP: 103.102.166.224           Port: 80
Destination:    IP: 10.0.2.15                 Port: 50396
Direction:      RECEIVE [ <<< ]
Data length:    6 byte
IP-H data:      45 00 00 28 3e ac 00 00 40 06 21 cf 67 66 a6 e0 0a 00 02 0f 
TCP-H data:     00 50 c4 dc 04 0e 16 02 d5 3f 4a ab 50 10 ff ff 96 57 00 00 
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
Time:           2025-01-02 22:29:48.9683 / 1735787388.9683, Passage number: 3
IP header:      Version: 4, IP header length: 20, Packet length: 316, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 67776002, Acknowledgement: 1486460925, Window: 65535, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 74.6.143.25               Port: 80
Destination:    IP: 10.0.2.15                 Port: 46494
Direction:      RECEIVE [ <<< ]
Data length:    276 byte
IP-H data:      45 00 01 3c 3e 9f 00 00 40 06 55 ef 4a 06 8f 19 0a 00 02 0f 
TCP-H data:     00 50 b5 9e 04 0a 2e 02 58 99 97 fd 50 18 ff ff 4c 2b 00 00 

48 54 54 50 2f 31 2e 31 20 33 30 31 20 4d 6f 76 65 64 20 50 65 72 6d 61 6e 65 6e 74 6c 79 0d 0a 44 61 74 65 3a 20 53 61 74 2c 20 31 31 20 4a 61 6e 20 32 30 32 35
20 31 33 3a 32 39 3a 34 30 20 47 4d 54 0d 0a 43 6f 6e 6e 65 63 74 69 6f 6e 3a 20 6b 65 65 70 2d 61 6c 69 76 65 0d 0a 53 65 72 76 65 72 3a 20 41 54 53 0d 0a 43 61
63 68 65 2d 43 6f 6e 74 72 6f 6c 3a 20 6e 6f 2d 73 74 6f 72 65 2c 20 6e 6f 2d 63 61 63 68 65 0d 0a 43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a 20 74 65 78 74 2f 68 74 6d
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
6c 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 61 6e 67 75 61 67 65 3a 20 65 6e 0d 0a 58 2d 46 72 61 6d 65 2d 4f 70 74 69 6f 6e 73 3a 20 53 41 4d 45 4f 52 49 47 49 4e 0d 0a 4c
6f 63 61 74 69 6f 6e 3a 20 68 74 74 70 73 3a 2f 2f 79 61 68 6f 6f 2e 63 6f 6d 2f 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 65 6e 67 74 68 3a 20 38 0d 0a 0d 0a 72 65 64 69 72 65 
```


**Filtering and tracking**

```bash
# ipscap --port=80 --find=GET --tracking --output=HEX


Time:           2025-01-04 22:41:22.7246 / 1735940482.7246, Passage number: 1
IP header:      Version: 4, IP header length: 20, Packet length: 114, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 67488716, Acknowledgement: 68672002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60288
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    74 byte
IP-H data:      45 00 00 72 73 bb 40 00 40 06 4d b2 0a 00 02 0f 8e fb de 0e 
TCP-H data:     eb 80 00 50 04 05 cb cc 04 17 da 02 50 18 72 10 79 7d 00 00 

GET / HTTP/1.1
User-Agent: curl/7.29.0
Host: google.com
Accept: */*

Time:           2025-01-04 22:41:22.7251 / 1735940482.7251, Passage number: 1
IP header:      Version: 4, IP header length: 20, Packet length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 68672002, Acknowledgement: 67488790, Window: 65535, Flags: ['ACK']
TCP options:    -
Source:         IP: 142.251.222.14            Port: 80
Destination:    IP: 10.0.2.15                 Port: 60288
Direction:      RECEIVE [ <<< ]
Data length:    6 byte
IP-H data:      45 00 00 28 3e da 00 00 40 06 c2 dd 8e fb de 0e 0a 00 02 0f 
TCP-H data:     00 50 eb 80 04 17 da 02 04 05 cc 16 50 10 ff ff 9c b5 00 00 

Time:           2025-01-04 22:41:22.8006 / 1735940482.8006, Passage number: 2
IP header:      Version: 4, IP header length: 20, Packet length: 813, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 68672002, Acknowledgement: 67488790, Window: 65535, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 142.251.222.14            Port: 80
Destination:    IP: 10.0.2.15                 Port: 60288
Direction:      RECEIVE [ <<< ]
Data length:    773 byte
IP-H data:      45 00 03 2d 3e db 00 00 40 06 bf d7 8e fb de 0e 0a 00 02 0f 
TCP-H data:     00 50 eb 80 04 17 da 02 04 05 cc 16 50 18 ff ff ab 50 00 00 

HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
X-Frame-Options: SAMEORIGIN

<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
```

