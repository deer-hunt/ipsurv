# IpSurv

```ipsurv``` is a command-line program for surveying IP addresses, host information, and more. Also ```ipsurv``` is extensible program by Python.

<div align="center">

<a href="https://pypi.org/project/ipsurv"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/ipsurv.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/lint.yml"><img alt="GitHub Actions build status (Lint)" src="https://github.com/deer-hunt/ipsurv/workflows/Lint/badge.svg"></a>
<a href="https://codecov.io/gh/deer-hunt/ipsurv"><img alt="Coverage" src="https://codecov.io/github/deer-hunt/ipsurv/coverage.svg?branch=main"></a>
<a href="https://pypi.org/project/ipsurv/"><img alt="Newest PyPI version" src="https://img.shields.io/pypi/v/ipsurv.svg"></a>
<a href="https://pypi.org/project/ipsurv/"><img alt="Number of PyPI downloads" src="https://img.shields.io/pypi/dm/ipsurv.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/blob/main/LICENSE.md"><img alt="License - MIT" src="https://img.shields.io/pypi/l/ipsurv.svg"></a>

</div>

<img src="https://raw.githubusercontent.com/deer-hunt/ipsurv/main/docs/images/ipsurv.gif" alt="ipsurv visual image" width="100%" />

## Installation

```bash
$ pip install ipsurv
or
$ pip3 install ipsurv
```

## Requirements

- ```python``` and ```pip``` command
- Python 3.0 or later version.

> If you'd like to use in Python 2.7, you can refactor to Python 2.7 code easily. See "development_debug.md".

## Usage

**Specify IP using Argument**

```bash
$ cat ips.txt|python3 -m ipsurv 192.168.1.10
$ cat ips.txt|python3 -m ipsurv 192.168.1.10 192.168.1.11
```

**Specify IP using PIPE**

```bash
$ cat ips.txt|python3 -m ipsurv
$ cat apache.log|python3 -m ipsurv
```

**Example result**

```bash
8.8.8.8:53,8.8.8.0,US,ICMP_OK,TCP_OK,UDP_OK
```

## Survey-mode

```ipsurv``` have two Survey-mode. Those are "Survey IPs" and "Survey Self". 

| Survey-mode              | Description              |
|-------------------|------------------------|
| **Survey IPs**     | Primary mode. Surveying IP or Host or URL.     |
| **Survey Self**    | Surveying self IP.     |

**Survey Self e.g.**

```bash
$ ipsurv self
Ip: 144.160.*.*
Hostname: 
Organization: AS797 AT&T Services, Inc.
Country: US
City: San Jose
Region: California
Postal: 95103
Geo: 37.3394,-121.8950
Timezone: America/Los_Angeles
LocalIp: 10.0.2.5
LocalDns: ['8.8.8.8', '8.8.4.4']
```

## Features of "Survey IPs mode"

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

## Command options

```ipsurv``` have many options. Please read [Command Arguments(.md) reference](https://github.com/deer-hunt/ipsurv/blob/main/docs/command_arguments.md).

**Options**

```
[-h] [--verbose {0,1,2,3}] [--log LOG] [--disable_env]
[--resolve RESOLVE] [--autodetect AUTODETECT]
[--begin BEGIN] [--end END] [--collect COLLECT]
[--all_collect] [--timeout TIMEOUT] [--group GROUP]
[--skip_duplicate {0,1,2}] [--format FORMAT]
[--no_original] [--sequence] [--enclose ENCLOSE]
[--delimiter DELIMITER] [--alt_delimiter ALT_DELIMITER]
[--headers {0,1,2,3}] [--json {0,1,2}] [--json_list]
[--exhaustive] [--icmp ICMP] [--tcp TCP] [--udp UDP]
[--http {0,1,2}] [--version]
[target [target ...]]
```

**Example options**

```bash
$ cat ips.txt|python3 -m ipsurv --group=24
$ cat ips.txt|python3 -m ipsurv --group=network
$ cat ips.txt|python3 -m ipsurv --format="{country},{name}"
$ cat ips.txt|python3 -m ipsurv --format="{country},{ip_int},{handle},{port43}"
$ cat /var/log/httpd/access_log|ipsurv --ident --no_original

$ cat ips.txt|python3 -m ipsurv --group=255.255.255.0
$ cat ips.txt|python3 -m ipsurv --delimiter="\t"
$ cat ips.txt|python3 -m ipsurv --format="{group}\t{ip_int}\t{country}\t{handle}\t{port43}" 
$ cat ips.txt|python3 -m ipsurv --format="{country},{ip_int},{handle},{port43},{icmp},{port},{tcp}" --group=network --icmp=1 --tcp=1 --timeout=2
```

## Example result

```bash
$ cat .dev/test/government.txt|ipsurv --headers=1 --format="{status},{group},{country},{name},{cidr},{http},{http_h2}" --group=network --http=2

original,status,group,country,name,cidr,http,http_h2
www.whitehouse.gov,OK,192.0.64.1,US,AUTOMATTIC,192.0.64.0/18,HTTP_OK,HTTP2
www.state.gov,OK,3.165.0.1,US,AMAZON-CF,3.165.0.0/16,HTTP_OK,HTTP2
www.treasury.gov,OK,23.32.0.1,US,AKAMAI,23.32.0.0/11,HTTP_OK,HTTP2
www.gov.uk,OK,151.101.0.1,US,SKYCA-3,151.101.0.0/16,HTTP_OK,HTTP2
www.gouvernement.fr,OK,217.70.184.1,FR,GANDIFR-NET4,217.70.184.0/24,HTTP_OK,HTTP1
www.diplomatie.gouv.fr,OK,77.128.0.1,FR,FR-SFR-20100831,77.128.0.0/11,HTTP_OK,HTTP1
www.economie.gouv.fr,OK,141.101.88.1,EU,CLOUDFLARE-EU,141.101.88.0/21,HTTP_OK,HTTP2
www.bundesregierung.de,OK,185.173.230.1,DE,BABIEL-NET-230,185.173.230.0/24,HTTP_OK,HTTP2
```

## Documents

| Title                       | Path                                        |
|-------------------------------|---------------------------------------------|
| **Command arguments reference**    | [command_arguments.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/command_arguments.md) |
| **Command examples**               | [command_examples.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/command_examples.md)   |
| **Program architecture and Classes** | [program_architecture_classes.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/program_architecture_classes.md) |
| **Customizing and Examples**       | [customize_examples.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/customize_examples.md) |
| **Development and Debugging**          | [development_debug.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/development_debug.md)   |


## Path summary

| Directory        | Description                                         |
|-----------------------|-----------------------------------------------------|
| `.github`            | GitHub Actions files          |
| `docs`               | Documentation files                                 |
| `example_data`       | Sample data files for testing                       |
| `examples`           | Example programs                 |
| `ipsurv`             | Main package/Sources                            |
| `tests`              | Test files                     |



## Debugging

In verbose mode, outputting internal data and behaviors in detail.

```bash
$ python -m ipsurv --verbose=2 #INFO
$ python -m ipsurv --verbose=3 #DEBUG
```

## Customizing ipsurv

```ipsurv``` is implemented as customizable program architecture. ```ipsurv``` provide extending features and several classes. Please read ```program_architecture_classes.md```.

**Classes for Major Customization**

| Classes    | Description             | Example program |
|----------------------|--------------|--------------------------------------------------|
| **Pipeline**   | Pipeline class provide catching and customizing the data in each processing. | pipeline_customize.py                  |
| **ObjectFactory**   | ObjectFactory class provide customizing classes and creating original classes. | ./core/object_factory.py   |
| **Serializer, LineSerializer, JsonSerializer**   | Serializer class provide displaying data and transforming data for presentation. | object_factory_original_headers.py                  |


## Dependencies

- [dnspython](https://github.com/rthalley/dnspython)


