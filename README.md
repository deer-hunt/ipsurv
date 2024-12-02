# IpSurv

<div>
<img width="165" height="165" src="https://raw.githubusercontent.com/deer-hunt/ipsurv/main/docs/images/ipsurv-logo.png" align="left" />

```ipsurv``` is a command-line program for surveying IP addresses, host information, and more. Also ```ipsurv``` is extensible program by Python.

<div>

<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests-windows.yml"><img alt="CI - Test" src="https://github.com/deer-hunt/ipsurv/actions/workflows/unit-tests-windows.yml/badge.svg"></a>
<a href="https://github.com/deer-hunt/ipsurv/actions/workflows/lint.yml"><img alt="GitHub Actions build status (Lint)" src="https://github.com/deer-hunt/ipsurv/workflows/Lint/badge.svg"></a>
<a href="https://codecov.io/gh/deer-hunt/ipsurv"><img alt="Coverage" src="https://codecov.io/github/deer-hunt/ipsurv/coverage.svg?branch=main"></a>
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/ipsurv">
<a href="https://github.com/deer-hunt/ipsurv/blob/main/LICENSE.md"><img alt="License - MIT" src="https://img.shields.io/pypi/l/ipsurv.svg"></a>
<a href="https://pypi.org/project/ipsurv/"><img alt="Newest PyPI version" src="https://img.shields.io/pypi/v/ipsurv.svg"></a>
<a href="https://pypi.org/project/ipsurv/"><img alt="Number of PyPI downloads" src="https://img.shields.io/pypi/dm/ipsurv.svg"></a>
<img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/deer-hunt/ipsurv">
<a href="https://pypi.org/project/ipsurv"><img alt="Supported Versions" src="https://img.shields.io/pypi/pyversions/ipsurv.svg"></a>
<a href="https://deer-hunt.github.io/ipsurv/" alt="IpSurv's documentation site"><img src="https://img.shields.io/badge/stable%20docs-github.io-brightgreen?style=flat&color=%2373DC8C&label=Docs"/></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fdeer-hunt%2Fipsurv?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fdeer-hunt%2Fipsurv.svg?type=shield"/></a>

</div>
</div>

<p>&nbsp;</p>

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

**Specify Target using Argument**

```bash
$ ipsurv 192.168.1.10
$ ipsurv 192.168.1.10 192.168.1.11
$ ipsurv test-example-sample-ipsurv.com --add_ip
$ ipsurv x.x.x.x --format=geo
```

**Specify Target using PIPE**

```bash
$ cat ips.txt|ipsurv
$ cat apache.log|ipsurv --add_ip
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

```ipsurv``` have many options. Please read [Command arguments(.md) reference](https://github.com/deer-hunt/ipsurv/blob/main/docs/command_arguments.md).

**Options**

```
[-h] [--verbose {0,1,2,3}] [--log LOG] [--disable_env]
[--resolve RESOLVE] [--autodetect AUTODETECT]
[--begin BEGIN] [--end END] [--collect COLLECT]
[--all_collect] [--timeout TIMEOUT]
[--group GROUP] [--skip_duplicate {0,1,2}] [--range RANGE] [--format FORMAT]
[--no_original] [--sequence] [--add_ip] [--ident]
[--enclose ENCLOSE] [--delimiter DELIMITER] [--alt_delimiter ALT_DELIMITER]
[--headers {0,1,2,3}] [--json {0,1,2}] [--json_list]
[--exhaustive] [--icmp ICMP] [--tcp TCP] [--udp UDP]
[--http {0,1,2}] [--version]
[target [target ...]]
```

**Example options**

```bash
$ cat ips.txt|ipsurv --group=24
$ cat ips.txt|ipsurv --group=network
$ cat ips.txt|ipsurv --format=country
$ cat ips.txt|ipsurv --format=hostname
$ cat ips.txt|ipsurv --format="{country},{name}"
$ cat ips.txt|ipsurv --format="{country},{ip_int},{handle},{port43}"
$ cat /var/log/httpd/access_log|ipsurv --ident --no_original

$ cat ips.txt|ipsurv --group=255.255.255.0
$ cat ips.txt|ipsurv --delimiter="\t"
$ cat ips.txt|ipsurv --format="{group}\t{ip_int}\t{country}\t{handle}\t{port43}" 
$ cat ips.txt|ipsurv --format="{country},{ip_int},{handle},{port43},{icmp},{port},{tcp}" --group=network --icmp=1 --tcp=1 --timeout=2
```

## Command examples

**Show headers**

```bash
$ cat ./example_data/government.txt|ipsurv --headers=1 --format="{status},{group},{country},{name},{cidr},{http},{http_h2}" --group=network --http=2
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

**Add line-number**

```bash
$ cat ./example_data/government.txt|ipsurv --sequence --add_ip
1,www.whitehouse.gov,192.0.66.168,OK,US,AUTOMATTIC,192.0.64.0,192.0.127.255
2,www.state.gov,3.165.39.61,OK,US,AMAZON-CF,3.165.0.0,3.165.255.255
3,www.treasury.gov,23.50.118.187,OK,US,AKAMAI,23.32.0.0,23.67.255.255
4,www.gov.uk,151.101.192.144,OK,US,SKYCA-3,151.101.0.0,151.101.255.255
```

**Output by JSON**

```bash
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

**Output detailed data by JSON**

```bash
$ ipsurv wikipedia.org --format=default --json=2 --exhaustive
{
  "success": true,
  "status": "OK",
  "requests": [
    "RDAP"
  ],
  "errors": [],
  "sequence": 1,
  "original": "wikipedia.org",
  "target": "103.102.166.224",
  "ip": "103.102.166.224",
  "ip_int": 1734780640,
  "port": null,
  "group_int": 0,
  "group": "",
  "group_found": false,
  "group_status": "-",
  "country": "US",
  "name": "WIKIMEDIA-AP",
  "network_start": "103.102.166.0",
  "network_end": "103.102.166.255",
  "ip_hex": "67.66.A6.E0",
  "ip_reversed": "224.166.102.103",
  "ip_type": "PUBLIC",
~~~~~~~~~~~~~
  "org": "Wikimedia Foundation, Inc.",
  "address": "1 Montgomery Street Suite 1600",
  "description": "Wikimedia Foundation, Inc.",
  "target.raw": "wikipedia.org",
  "target.identifier": "103.102.166.224",
  "target.identifier_int": 1734780640,
  "target.identified": true,
  "target.ip": "103.102.166.224",
  "target.url": null,
  "target.fqdn": "wikipedia.org",
  "target.port": null,
  "target.status": "EXIST"
}
```

More examples is [here](https://deer-hunt.github.io/ipsurv/pages/command_examples.html)


## Documents

IpSurv's documentation site is [https://deer-hunt.github.io/ipsurv/](https://deer-hunt.github.io/ipsurv/).

| Title                       | Path                                        |
|-------------------------------|---------------------------------------------|
| **Command arguments reference**    | [command_arguments.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/command_arguments.md) |
| **Command examples**               | [command_examples.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/command_examples.md)   |
| **Program architecture and Classes** | [program_architecture_classes.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/program_architecture_classes.md) |
| **Customizing and Examples**       | [customize_examples.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/customize_examples.md) |
| **Development and Debugging**          | [development_debug.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/development_debug.md)   |
| **Major Modules and Classes** | [github.io / Modules and Classes reference](https://deer-hunt.github.io/ipsurv/py-modindex.html)  |


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
$ ipsurv ***** --verbose=2  #INFO
$ ipsurv ***** --verbose=3  #DEBUG
```

## Customizing IpSurv

```ipsurv``` is implemented as customizable program architecture. ```ipsurv``` provide extending features and several classes. 
And you can use ipsurv's internal classes in your program. Please read ```program_architecture_classes.md```.

**Classes for major customization**

| Classes    | Description            |
|----------------------|----------------------------------------------|
| **Pipeline**   | Pipeline class provide catching and customizing the data in each processing. ```./examples/pipeline_customize.py```         |
| **ObjectFactory**   | ObjectFactory class provide customizing classes and creating original classes. ```./examples/object_factory.py```      |
| **Serializer, LineSerializer, JsonSerializer**   | Serializer class provide displaying data and transforming data for presentation. ```./examples/object_factory_original_headers.py```      |


## Dependencies

- [dnspython](https://github.com/rthalley/dnspython)
