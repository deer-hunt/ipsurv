# Introduction to "ipsend"

`ipsend` is a network transmission tool that supports TCP, SSL, UDP, and Raw sockets, as well as interactive transmission.

### Features

- Transmit by TCP, UDP, SSL.
- Transmit by Raw socket.
- Support Instant transmission and Interactive transmission.
- Specify Input and Output format - TEXT, HEX, BINARY, BASE64.
- Set SSL context - SSLv3, TLS1.0, TLS1.1, TLS1.2, TLS1.3.

> IPv6 is not supported.


## Usage

**Options**

```bash
usage: ipsend [-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
                   [--mode {TCP,UDP,SSL,IP_HEADER,TCP_HEADER,UDP_HEADER,ICMP_HEADER,IP_PAYLOAD,TCP_PAYLOAD,UDP_PAYLOAD,ICMP_PAYLOAD}]
                   [--input {TEXT,BINARY,HEX,BASE64}]
                   [--output {NONE,TEXT,BINARY,HEX,BASE64}]
                   [--interactive {int}]
                   [--ssl_context {SSLV3,TLS1.0,TLS1.1,TLS1.2,TLS1.3}]
                   [--output_send {int}] [--auto_lb {bool}] [--dest {string}]
                   [--port {int}] [--timeout {float}] [--ip_flags {int}]
                   [--ip_identification {int}] [--ip_ttl {int}]
                   [--ip_protocol {int}] [--src_ip {int}] [--src_port {int}]
                   [--dest_ip {int}] [--dest_port {int}] [--tcp_flags {str}]
                   [--tcp_seq {int}] [--tcp_ack {int}] [--tcp_window {int}]
                   [--icmp_type {int}] [--icmp_code {int}] [--icmp_id {int}]
                   [--icmp_seq {int}] [-I] [--http] [--https] [--version]
```


## Optional Arguments

| Option                                                          | Description                                                                                                                                  |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| -h, --help                                                      | Show this help message and exit                                                                                                              |
| --verbose {0,1,2,3}                                             | Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]                                                                                       |
| --debug                                                         | `--debug` is equivalent to `--verbose=3`.                                                                                                    |
| --log {string}                                                  | Verbose log filename.                                                                                                                        |
| --mode  | Transmission mode. <br>[TCP,UDP,SSL,IP_HEADER,TCP_HEADER,UDP_HEADER,ICMP_HEADER,IP_PAYLOAD,TCP_PAYLOAD,UDP_PAYLOAD,ICMP_PAYLOAD] |　
| --input {TEXT,BINARY,HEX,BASE64}                                | Input format. Default: TEXT                                                                                                                  |
| --output {NONE,TEXT,BINARY,HEX,BASE64}                          | Output format. Default: TEXT                                                                                                                 |
| --interactive {int}                                             | Enable INTERACTIVE mode. <br>[1: Line-break to send, 2: Ctrl-key to send]                                                                    |
| --ssl_context               | SSL context.<br>[SSLv3, TLS1.0, TLS1.1, TLS1.2, TLS1.3]                                                                                      |
| --output_send {int}                                             | Output Send-data in INSTANT mode. [1: Output & Send, 2: Only output]                                                                         |
| --auto_lb {bool}                                                | Append Line-break in INSTANT mode and `TEXT` input format.                                                                                   |
| --dest {string}                                                 | Destination IP or Hostname.                                                                                                                  |
| --port {int}                                                    | Destination port.                                                                                                                            |
| --timeout {float}                                               | Timeout. Default: 20.0                                                                                                                       |
| --version                                                       | Show version information.                                                                                                                    |
| --ip_flags {int}                                                | IP flags.                                                                                                                                    |
| --ip_identification {int}                                       | IP identification.                                                                                                                           |
| --ip_ttl {int}                                                  | IP TTL.                                                                                                                                      |
| --ip_protocol {int}                                             | IP Protocol number.                                                                                                                          |
| --src_ip {int}                                                  | Source IP.                                                                                                                                   |
| --src_port {int}                                                | Source port.                                                                                                                                 |
| --dest_ip {int}                                                 | Destination IP.                                                                                                                              |
| --dest_port {int}                                               | Destination port.                                                                                                                            |
| --tcp_flags {str}                                               | TCP flags. ex: FIN,SYN,RST,PSH,ACK                                                                                                           |
| --tcp_seq {int}                                                 | TCP sequence number.                                                                                                                         |
| --tcp_ack {int}                                                 | TCP acknowledgment number.                                                                                                                   |
| --tcp_window {int}                                              | TCP window size.                                                                                                                             |
| --icmp_type {int}                                               | ICMP type.                                                                                                                                   |
| --icmp_code {int}                                               | ICMP code.                                                                                                                                   |
| --icmp_id {int}                                                 | ICMP identifier.                                                                                                                             |
| --icmp_seq {int}                                                | ICMP sequence number.                                                                                                                        |
| -I                                                              | `-I` is equivalent to `--interactive=1`.                                                                                                     |
| --http                                                          | `--http` is equivalent to `--port=80`.                                                                                                       |
| --https                                                         | `--https` is equivalent to `--port=443 --mode=SSL`.                                                                                          |


## Command Examples


**INSTANT mode**

```
$ ipsend "GET /index.html HTTP/1.1\n" --dest=google.com --http

HTTP/1.1 200 OK
Date: Sat, 25 Jan 2025 ~~:~~:~~ GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
Content-Security-Policy-Report-Only: object-src 'none';base-uri 'self';script-src 'nonce-w83nSY4SHEvUEbhHyzS0hw' 'strict-dynamic' 'report-sample' 'unsafe-eval' 'unsafe-inline' https: http:;report-uri https://csp.withgoogle.com/csp/gws/other-hp
P3P: CP="This is not a P3P policy! See g.co/p3phelp for more info."
Server: gws
X-XSS-Protection: 0
```

```
$ ipsend "GET / HTTP/1.1\n" --dest=google.com --https

HTTP/1.1 200 OK
Date: Sat, 25 Jan 2025 ~~:~~:~~ GMT
Expires: -1
Cache-Control: private, max-age=0
Content-Type: text/html; charset=ISO-8859-1
```

```
$ ipsend "GET / HTTP/1.1\n" --dest=wikipedia.org --mode=SSL --port=443

HTTP/1.1 400 Bad Request
date: Sat, 25 Jan 2025 ~~:~~:~~ GMT
server: Varnish
x-cache: cp5022 int
x-cache-status: int-front
```


**INTERACTIVE mode**

```
$ ipsend --mode=TCP --dest=google.com --port=80 --interactive=1

python3 -m ipsend --mode=TCP --dest=google.com --port=80 --interactive=1
[INTERACTIVE] / Line-break to send

Please input send-data. Input a line break to send.

GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Mon, 27 Jan 2025 10:25:13 GMT
```

```
$ ipsend --dest=wikipedia.org --https -I
[INTERACTIVE] / Line-break to send

Please input send-data. Input a line break to send.

GET / HTTP/1.1

HTTP/1.1 400 Bad Request
```

```
$ ipsend --dest=google.com --https -I --output=BASE64
[INTERACTIVE] / Line-break to send

Please input send-data. Input a line break to send.

GET / HTTP/1.1

SFRUUC8xLjEgMjAwIE9LDQpEYXRlOiBNb24sIDI3IEphbiAyMDI1IDEwOjI4OjA4IEdNVA0KRXhwaXJlczogLTENCkNhY2hlLUNvbnRyb2w6IHByaXZhdGUsIG1heC1hZ~~~~~~
```

```
$ ipsend --dest=gmail-smtp-in.l.google.com --port=25 -I
[INTERACTIVE] / Line-break to send

Please input send-data. Input a line break to send.

220 mx.google.com ESMTP d2e1a72fcca58-72f8a78e16asi10830435b3a.292 - gsmtp

EHLO gmail.com
MAIL FROM:<???????@???????.com>
RCPT TO:<????????@gmail.com>
DATA

451-4.5.0 SMTP protocol violation. For more information, go to
```

```
$ ipsend --dest=google.com --port=80 --interactive=2
[INTERACTIVE] / Ctrl-key to send

Please input send-data. Press `Ctrl+D` to send.
~~~~~
```


**Various output**

```
$ ipsend --mode=TCP --dest=wikipedia.org --http -I --output=HEX
[INTERACTIVE] / Line-break to send

Please input send-data. Input a line break to send.

GET / HTTP/1.1

48 54 54 50 2f 31 2e 31 20 33 30 31 20 4d 6f 76 65 64 20 50 65 72 6d 61 6e 65 6e 74 6c 79 0d 0a 63 6f 6e 74 65 ~~~~~~~~ 6f 6e 6e 65 63 74 69 6f 6e 3a 20 63 6c 6f 73 65 0d 0a 0d 0a
```

```
$ ipsend --mode=TCP --dest=wikipedia.org --http -I --output=BASE64
```

```
$ ipsend --mode=UDP --dest=8.8.8.8 --port=53 --input=BINARY --interactive=2
[INTERACTIVE] / Ctrl-key to send

Please input send-data. Press `Ctrl+D` to send.

\xdb!\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x03www\x06google\x03com\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x00
!wwwgooglecom)
```

```
$ ipsend --mode=TCP --dest=wikipedia.org --https -I --output=BINARY
[INTERACTIVE] / Line-break to send

Please input send-data. Input a line break to send.

GET / HTTP/1.1

b'HTTP/1.1 400 Bad Request\r\ndate: Mon, 27 Jan 2025 10:32:55 GMT\r\nserver: Varnish\r\nx-cache: ~~~~~ </div>\n</html>\n'
```


**Header send**

```bash
# ipsend '47 45 54 20 2f 69 6e 64 65 78 2e 68 74 6d 6c 20 48 54 54 50 2f 31 2e 31 0a 0a 0a' --mode=TCP --dest=172.217.31.174 --port=80 --input=HEX
# ipsend 'R0VUIC9pbmRleC5odG1sIEhUVFAvMS4xCkhvc3Q6IHd3dy5nb29nbGUuY29tCgo=' --mode=TCP --dest=172.217.31.174 --port=80 --input=BASE64

# ipsend '\xaa\x1e\x00P\xc9\x94o"\x005\xb6\x02P\x18r\x10y}\x00\x00GET / HTTP/1.1\r\nAccept: */*\r\n\r\n' --mode=TCP_HEADER --dest=google.com --input=BINARY
# ipsend '\xaa\x1e\x00P\xc9\x94o"\x005\xb6\x02P\x18r\x10y}\x00\x00GET / HTTP/1.1\r\nHost: google.com\r\n\r\n' --mode=TCP_HEADER --dest=172.217.31.174 --input=binary
```


## Documents

The following documents exist in `ipsurv`. You can read documents in [Documentation site](https://deer-hunt.github.io/ipsurv/).

| Title                       | Path                                                                                                                             |
|-------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| **Command arguments**    | [command_arguments.md](https://deer-hunt.github.io/ipsurv/pages/ipsend-cmd/command_arguments.html)                       |
| **Customizing and Examples**       | [customize_examples.md](https://deer-hunt.github.io/ipsurv/pages/ipsend-cmd/customize_examples.html)                     |
| **Development and Debugging**          | [development_debug.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/development_debug.md)                                  |
| **ipsurv's Major Modules and Classes** | [github.io / Modules and Classes reference](https://deer-hunt.github.io/ipsurv/py-modindex.html)                                 |
