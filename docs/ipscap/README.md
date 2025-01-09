# ipscap

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

```bash
ipscap [-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
       [--find {string}] [--find_case_sensitive] [--find_hex {string}]
       [--port {int}] [--protocol [ICMP, TCP, UDP]] [--ip {string}]
       [--condition {string}] [--tracking] [--stat_mode {0,1,2}]
       [--stat_group {0,1,2}]
       [--output [NONE, HEADER, TEXT, BINARY, HEX, LINE]]
       [--dumpfile {0,1,2}] [--timeout {float}] [--exclude_ssh]
       [--web_port] [--general_port] [--force] [--version]
```

## Optional Arguments

| Option                            | Description                                                                                |
|-----------------------------------|--------------------------------------------------------------------------------------------|
| `-h, --help`                      | Show this help message and exit.                                                          |
| `--verbose {0,1,2,3}`            | Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]                                  |
| `--debug`                         | `--debug` is equivalent to `--verbose=3`.                                                |
| `--log {string}`                  | Verbose log filename.                                                                      |
| `--find {string}`                 | Find character string by regex and ignoring case. ex: "3\d1", "HTTP"                    |
| `--find_case_sensitive`           | Find with case sensitivity.                                                                 |
| `--find_hex {string}`             | Find HEX data. ex: "00 99 f0 e0 78 4e 23 70 a1"                                         |
| `--port {int}`                    | Filter port. It is source port or destination port. ex: =80, =53,80                      |
| `--protocol [ICMP, TCP, UDP]`     | Filter Protocol. Default: "TCP,UDP"                                                       |
| `--ip {string}`                   | Filter IP. ex: =192.168.1.10, =192.168.1.10,192.168.1.20                                |
| `--condition {string}`            | Filter by detail condition. ex: "src_port=80;dest_port<=30000;ttl=64;flags=SYN,PSH"    |
| `--tracking`                      | Tracking transfers that have been matched by filters.                                      |
| `--stat_mode {0,1,2}`            | Statistics mode.                                                                           |
|                                   | - 0: None<br>- 1: Captured transfers<br>- 2: All transfers                              |
| `--stat_group {0,1,2}`           | Group the transfer in statistics.                                                          |
|                                   | - 0: None<br>- 1: Grouping by IPs and service port<br>- 2: Grouping by IPs              |
| `--output [NONE, HEADER, TEXT, BINARY, HEX, LINE]` | Output mode about header and data. [Mode] or [0 - 5]             |
|                                   | - NONE:<br>- HEADER: header only<br>- TEXT: text data<br>- BINARY: binary data<br>- HEX: hex data<br>- LINE: single line |
| `--dumpfile {0,1,2}`             | Dump data to files. Dir: `./dump_logs/`                                                   |
|                                   | - 0: Off<br>- 1: Dump data<br>- 2: Dump headers and data                                 |
| `--timeout {float}`               | Stop automatically after the specified number of seconds.                                  |
| `--exclude_ssh`                   | `--exclude_ssh` is equivalent to `--condition="port!=22"`.                              |
| `--web_port`                      | `--web_port` is equivalent to `--port=80,443,53`.                                       |
| `--general_port`                  | `--general_port` is equivalent to `--port=21,22,23,25,53,80,110,143,220,443,465,990,993,995,1433,3306`. |
| `--force`                         | Run force if any filter options aren't specified.                                          |
| `--version`                       | Show version information.                                                                   |



## Command Examples

```bash
ipscap --port="80;53" --find="GET"
ipscap --port="80" --find="3\d1"
ipscap --find_hex="00 99 f0 e0 78 4e 23 70 a1"
ipscap --find="HTTP" --tracking
ipscap --condition="port!=22"
ipscap --condition="port=80,443,53,-1" --protocol=TCP,UDP,ICMP
ipscap --condition="src_port>=80;src_port<=500;flags=SYN,PSH"
ipscap --condition="ttl>=120"
ipscap --output=HEADER
ipscap --output=BYTE --port="80,443"
ipscap --output=LINE --port="80,443"
ipscap --stat_mode=2 --protocol=TCP,UDP --output=NONE
ipscap --port=80,443 --stat_group=1
ipscap --port=80 --dumpfile=1
ipscap --exclude_ssh
ipscap --force
```

