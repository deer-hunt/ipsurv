# Command examples

This is introduction of ipscap's several command examples. You can understand some usage and features.

### Basic Usage

```
$ sudo su -

# ipscap --help

usage: ipscap [-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
              [--find {string}] [--find_mode [REGEX, MATCH, BINARY, HEX]]
              [--port {int}] [--protocol [ICMP, TCP, UDP]] [--ip {string}]
              [--condition {string}] [--tracking] [--stat_mode {0,1,2}]
              [--stat_group {0,1,2}]
              [--output [NONE, HEADER, TEXT, BINARY, BINARY_ALL, HEX, HEX_ALL, BASE64, BASE64_ALL, LINE]]
              [--dumpfile {0,1,2}] [--timeout {float}] [--exclude_ssh]
              [--web_port] [--general_port] [--force] [--version]

`ipscap` captures "ICMP, TCP, UDP" packets. It supports filtering by various conditions, dumping file, displaying statistics.

optional arguments:
  -h, --help            show this help message and exit
  --verbose {0,1,2,3}   Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
  --debug               `--debug` is equivalent to `--verbose=3`.
  --log {string}        Verbose log filename.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
# ipscap --exclude_ssh
 
Start capture packets...

Press `Ctrl + C` to stop.

Time:           2025-01-03 14:55:13.5109 / ~~~~~.5109, Passage number: 1
IP header:      Version: 4, IP header length: 20, Total length: 55, TTL: 64, IP protocol: UDP[17]
UDP header:     UDP header length: 8
Source:         IP: 10.0.2.15                 Port: 36305
Destination:    IP: 8.8.8.8                   Port: 53
Direction:      SEND [ >>> ]
Data length:    27 byte
IP-H data:      45 00 00 37 e4 3b 40 00 40 11 3a 5c 0a 00 02 0f 08 08 08 08 
UDP-H data:     8d d1 00 35 00 23 1c 53 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```


### Filter port

- Filter 80 port

> `--port` option filter receive or send packets.

```bash
# ipscap --port=80


Time:           2025-01-02 14:59:45.9329 / ~~~~~~~~.932, Passage number: 3
IP header:      Version: 4, IP header length: 20, Total length: 316, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1536002, Acknowledgement: 844367953, Window: 65535, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 74.6.231.20               Port: 80
Destination:    IP: 10.0.2.15                 Port: 51196
Direction:      RECEIVE [ <<< ]
Data length:    276 byte
IP-H data:      45 00 01 3c 00 c0 00 00 40 06 3b d3 4a 06 e7 14 0a 00 02 0f 
TCP-H data:     00 50 c7 fc 00 17 70 02 32 54 08 51 50 18 ff ff 52 a4 00 00 

HTTP/1.1 301 Moved Permanently
Date: Sun, 12 Jan 2025 05:59:37 GMT
Connection: keep-alive
Server: ATS
Cache-Control: no-store, no-cache
```

- Filter 80 and 443 port

```bash
# ipscap --port=80,443

Time:           2025-01-02 14:58:14.3874 / ~~~~~~~~.3874, Passage number: 1
IP header:      Version: 4, IP header length: 20, Total length: 44, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 24, Sequence: 1216001, Acknowledgement: 254560287, Window: 65535, Flags: ['SYN', 'ACK']
TCP options:    mss:1460
Source:         IP: 98.137.11.164             Port: 443
Destination:    IP: 10.0.2.15                 Port: 56118
Direction:      RECEIVE [ <<< ]
Data length:    2 byte
IP-H data:      45 00 00 2c 00 a7 00 00 40 06 ff e9 62 89 0b a4 0a 00 02 0f 
TCP-H data:     01 bb db 36 00 12 8e 01 0f 2c 48 1f 60 12 ff ff 5b 8a 00 00 02 04 05 b4 
```

- Filter except 22 port

```bash
# ipscap --condition="port!=22"

# ipscap --exclude_ssh
```

- Filter port range

```
# ipscap --condition="port>=10000"

# ipscap --condition="port>=25; port <=3306"
```

- Filter only dest port

```
# ipscap --condition="dest_port=80"
```

- Filter only source port

```
# ipscap --condition="src_port=80"
```


## Find and Find mode

**TEXT**

```
# ipscap --find="HTTP"
```

**MATCH**

```
# ipscap --find="http" --find_mode=MATCH
```

**BINARY**

```
# ipscap --find="\x05yahoo\x03com" --find_mode=BINARY --port=53
```

**HEX**

```
# ipscap --find="45 00 00 37" --find_mode=HEX
```


## Filter protocol


**UDP**

```
# ipscap --protocol=UDP
```

**ICMP**

```
# ipscap --protocol=ICMP
```

**TCP & ICMP**

```
# ipscap --protocol="TCP,ICMP"
```

**ALL**

```
# ipscap --protocol=ALL
```

## IP

```
# ipscap --ip=192.168.10.101
```

```
# ipscap --ip="192.168.10.101,192.168.10.102"
```

## Condition

```
# ipscap --condition="port!=22"
```

```
# ipscap --condition="client_port=80"
```

```
# ipscap --condition="src_port=80;dest_port<=30000;ttl=64"
```

```
# ipscap --condition="flags=SYN,PSH"
```

```
# ipscap --condition="sack=1;window>1000"
```

```
# ipscap --condition="wscale>1"
```


## Tracking

```
# ipscap --find="HTTP" --tracking

Time:           2025-01-12 22:42:42.3306 / ~~~~~~~~~.3306, Passage number: 1
IP header:      Version: 4, IP header length: 20, Total length: 114, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 3663095182, Acknowledgement: 1344002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60694
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    74 byte
IP-H data:      45 00 00 72 eb 76 40 00 40 06 d5 f6 0a 00 02 0f 8e fb de 0e 
TCP-H data:     ed 16 00 50 da 56 65 8e 00 14 82 02 50 18 72 10 79 7d 00 00 

GET / HTTP/1.1
User-Agent: curl/7.29.0
Host: google.com
Accept: */*


Time:           2025-01-12 22:42:42.3315 / ~~~~~~~~~.3315, Passage number: 1
IP header:      Version: 4, IP header length: 20, Total length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1344002, Acknowledgement: 3663095256, Window: 65535, Flags: ['ACK']
TCP options:    -
Source:         IP: 142.251.222.14            Port: 80
Destination:    IP: 10.0.2.15                 Port: 60694
Direction:      RECEIVE [ <<< ]
Data length:    6 byte
IP-H data:      45 00 00 28 00 4c 00 00 40 06 01 6c 8e fb de 0e 0a 00 02 0f 
TCP-H data:     00 50 ed 16 00 14 82 02 da 56 65 d8 50 10 ff ff 87 0f 00 00 

Time:           2025-01-12 22:42:42.4078 / ~~~~~~~~~.4078, Passage number: 2
IP header:      Version: 4, IP header length: 20, Total length: 813, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1344002, Acknowledgement: 3663095256, Window: 65535, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 142.251.222.14            Port: 80
Destination:    IP: 10.0.2.15                 Port: 60694
Direction:      RECEIVE [ <<< ]
Data length:    773 byte
IP-H data:      45 00 03 2d 00 4d 00 00 40 06 fe 65 8e fb de 0e 0a 00 02 0f 
TCP-H data:     00 50 ed 16 00 14 82 02 da 56 65 d8 50 18 ff ff fc 38 00 00 

HTTP/1.1 301 Moved Permanently
Location: http://www.google.com/
Content-Type: text/html; charset=UTF-8
Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-87RMr0fpufi3bqueM4np7A' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
Date: Sun, 12 Jan 2025 13:42:34 GMT
Expires: Tue, 11 Feb 2025 13:42:34 GMT
Cache-Control: public, max-age=2592000
Server: gws
Content-Length: 219
X-XSS-Protection: 0
X-Frame-Options: SAMEORIGIN

<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>


Time:           2025-01-12 22:42:42.4083 / ~~~~~~~~~.4083, Passage number: 2
IP header:      Version: 4, IP header length: 20, Total length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 3663095256, Acknowledgement: 1344775, Window: 30147, Flags: ['ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60694
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    0 byte
IP-H data:      45 00 00 28 eb 77 40 00 40 06 d6 3f 0a 00 02 0f 8e fb de 0e 
TCP-H data:     ed 16 00 50 da 56 65 d8 00 14 85 07 50 10 75 c3 79 33 00 00 
```


## Output mode

**NONE**

```
# ipscap --port=80 --output=NONE

> Nothing is displayed.
```

**HEADER**

```
# ipscap --port=80 --output=HEADER

Time:           2025-01-12 22:54:09.7662 / ~~~~~~~~~~..7662, Passage number: 3
IP header:      Version: 4, IP header length: 20, Total length: 114, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 133034702, Acknowledgement: 1600002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60698
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    74 byte
IP-H data:      45 00 00 72 fe 8b 40 00 40 06 c2 e1 0a 00 02 0f 8e fb de 0e 
TCP-H data:     ed 1a 00 50 07 ed f2 ce 00 18 6a 02 50 18 72 10 79 7d 00 00 

Time:           2025-01-12 22:54:09.7679 / ~~~~~~~~~~..7679, Passage number: 2
IP header:      Version: 4, IP header length: 20, Total length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1600002, Acknowledgement: 133034776, Window: 65535, Flags: ['ACK']
TCP options:    -
Source:         IP: 142.251.222.14            Port: 80
Destination:    IP: 10.0.2.15                 Port: 60698
Direction:      RECEIVE [ <<< ]
Data length:    6 byte
IP-H data:      45 00 00 28 00 5a 00 00 40 06 01 5e 8e fb de 0e 0a 00 02 0f 
TCP-H data:     00 50 ed 1a 00 18 6a 02 07 ed f3 18 50 10 ff ff e4 30 00 00 
```

**BINARY**

```
# ipscap --port=80 --output=BINARY

Time:           2025-01-12 22:55:07.3860 / ~~~~~~~~~~..3860, Passage number: 3
IP header:      Version: 4, IP header length: 20, Total length: 114, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 231131098, Acknowledgement: 1728002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60700
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    74 byte
IP-H data:      45 00 00 72 2a 86 40 00 40 06 96 e7 0a 00 02 0f 8e fb de 0e 
TCP-H data:     ed 1c 00 50 0d c6 c7 da 00 1a 5e 02 50 18 72 10 79 7d 00 00 

b'GET / HTTP/1.1\r\nUser-Agent: curl/7.29.0\r\nHost: google.com\r\nAccept: */*\r\n\r\n'
```


**HEX**

```
# ipscap --port=80 --output=HEX

Time:           2025-01-12 22:54:09.7662 / ~~~~~~~~~~.7662, Passage number: 3
IP header:      Version: 4, IP header length: 20, Total length: 114, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 133034702, Acknowledgement: 1600002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60698
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    74 byte
IP-H data:      45 00 00 72 fe 8b 40 00 40 06 c2 e1 0a 00 02 0f 8e fb de 0e 
TCP-H data:     ed 1a 00 50 07 ed f2 ce 00 18 6a 02 50 18 72 10 79 7d 00 00 

47 45 54 20 2f 20 48 54 54 50 2f 31 2e 31 0d 0a 55 73 65 72 2d 41 67 65 6e 74 3a 20 63 75 72 6c 2f 37 2e 32 39 2e 30 0d 0a 48 6f 73 74 3a 20 67 6f 6f 67 6c 65 2e 63 6f 6d 0d 0a 41 63 63 65 70 74 3a 20 2a 2f 2a 0d 0a 0d 0a 

Time:           2025-01-12 22:54:09.7679 / ~~~~~~~~~~.7679, Passage number: 2
IP header:      Version: 4, IP header length: 20, Total length: 40, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 160002, Acknowledgement: 133034776, Window: 65535, Flags: ['ACK']
TCP options:    -
Source:         IP: 142.251.222.14            Port: 80
Destination:    IP: 10.0.2.15                 Port: 60698
Direction:      RECEIVE [ <<< ]
Data length:    6 byte
IP-H data:      45 00 00 28 00 5a 00 00 40 06 01 5e 8e fb de 0e 0a 00 02 0f 
TCP-H data:     00 50 ed 1a 00 18 6a 02 07 ed f3 18 50 10 ff ff e4 30 00 00 

00 00 00 00 00 00 
```


**BASE64**

```
# ipscap --port=80 --output=BASE64

Time:           2025-01-22 22:55:07.3860 / ~~~~~~~~~~.2860, Passage number: 3
IP header:      Version: 4, IP header length: 20, Total length: 114, TTL: 64, IP protocol: TCP[6]
TCP header:     TCP header length: 20, Sequence: 1098, Acknowledgement: 28002, Window: 29200, Flags: ['PSH', 'ACK']
TCP options:    -
Source:         IP: 10.0.2.15                 Port: 60700
Destination:    IP: 142.251.222.14            Port: 80
Direction:      SEND [ >>> ]
Data length:    74 byte
IP-H data:      45 00 00 72 2a 86 40 00 40 06 96 e7 0a 00 02 0f 8e fb de 0e 
TCP-H data:     ed 1c 00 50 0d c6 c7 da 00 1a 5e 02 50 18 72 10 79 7d 00 00 

SFRUUC8xLjEgMzAxIE1vdmVkIFBlcm1hbmVudGx5DQpMb2NhdGlvbjogaHR0cDovL3d3dy5nb29nb ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Ij5oZXJlPC9BPi4NCjwvQk9EWT48L0hUTUw+DQo=BASE64
```


**LINE**

```
# ipscap --port=80 --output=LINE

2025-01-11 22:57:43.6990, 1,  4, 20, 64, 60,      TCP, 40, 2193112253, 0, 29200,          ['SYN'],              0,      10.0.2.15:60702,         142.251.222.14:80,       SEND,          mss:1460;sack;timestamp:601968655;nop;wscale:7
2025-01-11 22:57:43.7241, 1,  4, 20, 64, 44,      TCP, 24, 1856001, 2193112254, 65535,    ['SYN', 'ACK'],       2,      142.251.222.14:80,       10.0.2.15:60702,         RECEIVE,       mss:1460
2025-01-11 22:57:43.7244, 2,  4, 20, 64, 40,      TCP, 20, 2193112254, 1856002, 29200,    ['ACK'],              0,      10.0.2.15:60702,         142.251.222.14:80,       SEND,          -
2025-01-11 22:57:43.7251, 3,  4, 20, 64, 114,     TCP, 20, 2193112254, 1856002, 29200,    ['PSH', 'ACK'],       74,     10.0.2.15:60702,         142.251.222.14:80,       SEND,          -
2025-01-11 22:57:43.7253, 2,  4, 20, 64, 40,      TCP, 20, 1856002, 2193112328, 65535,    ['ACK'],              6,      142.251.222.14:80,       10.0.2.15:60702,         RECEIVE,       -
2025-01-11 22:57:43.8116, 3,  4, 20, 64, 813,     TCP, 20, 1856002, 2193112328, 65535,    ['PSH', 'ACK'],       773,    142.251.222.14:80,       10.0.2.15:60702,         RECEIVE,       -
2025-01-11 22:57:43.8122, 4,  4, 20, 64, 40,      TCP, 20, 2193112328, 1856775, 30147,    ['ACK'],              0,      10.0.2.15:60702,         142.251.222.14:80,       SEND,          -
2025-01-11 22:57:43.8126, 5,  4, 20, 64, 40,      TCP, 20, 2193112328, 1856775, 30147,    ['FIN', 'ACK'],       0,      10.0.2.15:60702,         142.251.222.14:80,       SEND,          -
2025-01-11 22:57:43.8139, 4,  4, 20, 64, 40,      TCP, 20, 1856775, 2193112329, 65535,    ['ACK'],              6,      142.251.222.14:80,       10.0.2.15:60702,         RECEIVE,       -
2025-01-11 22:57:43.8341, 5,  4, 20, 64, 40,      TCP, 20, 1856775, 2193112329, 65535,    ['FIN', 'ACK'],       6,      142.251.222.14:80,       10.0.2.15:60702,         RECEIVE,       -
2025-01-11 22:57:43.8344, 6,  4, 20, 64, 40,      TCP, 20, 2193112329, 1856776, 30147,    ['ACK'],              0,      10.0.2.15:60702,         142.251.222.14:80,       SEND,          -
```


## Dumpfile

```
# ipscap --port=80 --dumpfile=1

~~~~~~~~~~
************************************************************************************************************************
                                                   Captured Dump Logs                                                   
************************************************************************************************************************

Path:   /path/dump_logs/
Files:  4


# ls -la ./dump_logs/

total 20
drwxr-xr-x   2 root root  228 Jan 10 23:03 .
dr-xr-x---. 19 root root 4096 Jan 10 23:03 ..
-rw-r--r--   1 root root  773 Jan 10 23:03 tcp_10.0.2.15_60704_142.251.222.14_80_receive.dat
-rw-r--r--   1 root root   74 Jan 10 23:03 tcp_10.0.2.15_60704_142.251.222.14_80_send.dat
-rw-r--r--   1 root root  773 Jan 10 23:03 tcp_10.0.2.15_60706_142.251.222.14_80_receive.dat
-rw-r--r--   1 root root   74 Jan 10 23:03 tcp_10.0.2.15_60706_142.251.222.14_80_send.dat
```

## Grouping in statistics

```
# ipscap --port=80 --stat_group=1

~~~~~~~~~~~~~


*The following is the statistics for captured transfers only. If you'd like see to the statistics for all transfers, set`--stat_mode=2` option.


[TCP] 10.0.2.15 <-> 142.251.42.206       Port: 80
 SEND:      num: 18, unique: 3, size: 222
 RECEIVE:   num: 15, unique: 3, size: 2379
 GROUPS:    3

[TCP] 10.0.2.15 <-> 142.250.199.110      Port: 80
 SEND:      num: 6, unique: 1, size: 74
 RECEIVE:   num: 5, unique: 1, size: 793
 GROUPS:    1

[TCP] 10.0.2.15 <-> 142.251.222.14       Port: 80
 SEND:      num: 6, unique: 1, size: 74
 RECEIVE:   num: 5, unique: 1, size: 793
 GROUPS:    1
```

## Timeout

```
# ipscap --port=80 --timeout=10

Start capture packets...

`--timeout` option is enabled. The capture will stop 10.0 seconds automatically.
```

