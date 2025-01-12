# Command examples

This is introduction of ipsurv's several command examples. You can understand some usage and features. In detail usage, Please read [Command Arguments reference](command_arguments.md).

## Basic usage

### Show help

```
$ipsurv --help
usage: ipsurv [-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

optional arguments:
  -h, --help            show this help message and exit
  --verbose {0,1,2,3}   Verbose mode. [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
  --debug               `--debug` is equivalent to `--verbose=3`.
  --log {string}        Verbose log filename.
  --disable_env         Disable to load env variable for args. Env name: `IPSURV_ARGS`.
  --resolve {0,1}       Resolve the name to IP if target value is domain or hostname automatically.
  --identify_int        Identify IP's int value.
  --autodetect          Autodetect an IP or hostname that is included in the line. [Experimental]
  --begin {number}      Beginning from sequence number.
  --end {number}        Ending to sequence number.
  --collect {string}    Data collectors. See reference manual in detail. ex: rdap;dnstxt;dnsreverse;ipinfo;geoip
  --all_collect         All data collectors.
  --timeout {string}    Timeout seconds. Specify single value - ex: 1,3.2. Or specify values of each connection types. "dns,http,reactivity" - "3;5.1;6"
  --group {string}      Grouping rule. ex: network, 24, 255.255.255.0
  --skip_duplicate {0,1,2}
                        Skip duplicate group. *2: It also skip checking server reactivity[icmp, tcp, udp].
  --range {string}      Check whether IP is in IP/subnet ranges.  The value is CIDR notation. ex: "1.0.0.1/8;192.168.1.1/24"
  --format {string}     Output format. Specify `Profile` or `Parameter`. See reference manual in detail. ex: simple, default, detail, heavy, geo, hostname etc.
  --no_original         Cancel outputting the original line automatically.
  --sequence            Append sequence number.
  --add_ip              Append "ip" to the output format. For example, use when the target is a hostname, etc.
  --ident               Append identifier. Default identifier is ip.
  --enclose {string}    Character of enclose in result line. If you specify "json" option, this option is disabled. ex: '"', "'"
  --delimiter {string}  Delimiter-char in result line.
  --alt_delimiter {string}
                        Alternative delimiter character. If you specify "enclose" or "json" option, this option is disabled.
  --headers {0,1,2,3}   Show headers. 1: LowerCase, 2: PascalCase, 3: UpperCase
  --json {0,1,2}        Output JSON data. *2: Output formatted JSON.
  --json_list           Output JSON list. It makes it easier to parse JSON.
  --exhaustive          Output exhaustive internal values in JSON. Use with "json" option.
  --icmp {0,1}          Check ICMP.
  --tcp {number}        Check TCP port. Specify default port.
  --udp {number}        Check UDP port. Specify default port.
  --http {0,1,2}        Check HTTP response.
  --json_all            `--json_all` is equivalent to `--json=2 --exhaustive`.
  --geoip_only          `--geoip_only` is equivalent to `--collect=geoip --format=area`.
  --host_only           `--host_only` is equivalent to `--collect=dnsreverse --format=hostname`.
  --version             Show version information.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
```

### Specifying IP

Surveying a IP and some IPs.

**Command:**

```bash
$ ipsurv 8.8.8.8
8.8.8.8,OK,,US,GOGL,8.8.8.0,8.8.8.255,dns.google

$ ipsurv 8.8.4.4 1.1.1.1
8.8.4.4,OK,,US,GOGL,8.8.4.0,8.8.4.255,dns.google
1.1.1.1,OK,,AU,APNIC-LABS,1.1.1.0,1.1.1.255,one.one.one.one
```

### Specifying domain

Surveying a domain and some domains.

**Command:**

```bash
$ ipsurv www.wikipedia.org
www.wikipedia.org,OK,,US,WIKIMEDIA-AP,103.102.166.0,103.102.166.255,text-lb.eqsin.wikimedia.org

$ ipsurv www.reddit.com stackoverflow.com
www.reddit.com,NG,,US,SKYCA-3,151.101.0.0,151.101.255.255,
stackoverflow.com,NG,,US,CLOUDFLARENET,172.64.0.0,172.71.255.255,
```


### Multiple rows using pipe

"ipsurv" support the input by pipe. You are able to specify multiple rows.

**Example:**

```bash
$ cat urls.txt|ipsurv
www.whitehouse.gov,NG,,US,AUTOMATTIC,192.0.64.0,192.0.127.255,
www.state.gov,OK,,US,AMAZON-CF,3.165.0.0,3.165.255.255,server-3-165-39-26.nrt12.r.cloudfront.net
~~~~~~
```

## Various output-format

You can specify output-format flexibly by `--format` option.

**Example:**

```bash
$ cat list.txt|ipsurv --format=simple
$ cat list.txt|ipsurv --format=hostname --add_ip
$ cat list.txt|ipsurv --format=geo
$ cat list.txt|ipsurv --format="{country},{group},{geo},{original}"
$ cat list.txt|ipsurv --format=timezone
$ cat list.txt|ipsurv --format="{status},{group},{country},{name},{hostname}"
$ cat list.txt|ipsurv --format="{status},<web>,{ip}"
$ cat list.txt|ipsurv --format="{status}\t{ip}\t{hostname}"
```

## Output by JSON

Outputting JSON by `--json` option.

**Example:**

```bash
$ cat list.txt|ipsurv --json=1
{"original": "www.whitehouse.gov", "status": "NG", "group": "", "country": "US", "name": "AUTOMATTIC", "network_start": "192.0.64.0", "network_end": "192.0.127.255", "hostname": ""}

$ cat list.txt|ipsurv --json=2
{
  "original": "www.whitehouse.gov",
  "status": "NG",
  "group": "",
  "country": "US",
  "name": "AUTOMATTIC",
  "network_start": "192.0.64.0",
  "network_end": "192.0.127.255",
  "hostname": ""
}

$ cat list.txt|ipsurv --json=1 --json_list --begin=1 --end=2 --format="{ip},{geo},{country}"
[
{"original": "www.whitehouse.gov", "ip": "192.0.66.168", "geo": "37.7749,-122.4194", "country": "US"},
{"original": "www.state.gov", "ip": "3.165.39.61", "geo": "35.6895,139.6917", "country": "JP"},
]
```

**Output detailed data by JSON**

Displaying detailed data vertically in JSON.

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

## Grouping

You are able to group by subnet or provider network by `--group` option. And Skipping the duplicate group using `--skip_duplicate`.

```bash
$ cat list.txt|ipsurv --group=255.255.255.0 --skip_duplicate=1
$ cat list.txt|ipsurv --group=24
$ cat list.txt|ipsurv --group=network --skip_duplicate=1
```


## Show line-number

Show line-number.

**Example:**

```bash
$ cat list.txt|ipsurv --sequence
1,www.whitehouse.gov,OK,192.0.64.1,US,AUTOMATTIC,192.0.64.0/18,HTTP_OK,HTTP2
2,www.state.gov,OK,3.165.0.1,US,AMAZON-CF,3.165.0.0/16,HTTP_OK,HTTP2
3,www.treasury.gov,OK,23.32.0.1,US,AKAMAI,23.32.0.0/11,HTTP_OK,HTTP2
4,www.gov.uk,OK,151.101.0.1,US,SKYCA-3,151.101.0.0/16,HTTP_OK,HTTP2
```


## Starting line-number and Ending line-number

Set starting line-number and ending line-number.

**Example:**

```bash
$ cat list.txt|ipsurv --begin=10
10,91.239.100.101,OK,DK,UNCENSOREDDNS-V4-ANYCAST,91.239.100.0,91.239.100.255
11,45.33.32.156,OK,US,LINODE,45.33.0.0,45.33.127.255
12,45.33.32.157,OK,US,LINODE,45.33.0.0,45.33.127.255
~~~~
```

```bash
$ cat list.txt|ipsurv --begin=25 --end=50 --sequence
```

## Timeout

Set request timeout by ```--timeout```.

**Example:**

```bash
$ cat list.txt|ipsurv --timeout=5.1
$ cat list.txt|ipsurv --timeout="3.5;4.5;3.2" #DNS timeout, HTTP timeout, Reactivity timeout
```

## Change delimiter char

Change delimiter char by ```--delimiter```.

**Example:**

```bash
$ cat list.txt|ipsurv --delimiter=";"
8.8.8.8:53;OK;US;GOGL;8.8.8.0;8.8.8.255
8.8.4.4:53;OK;US;GOGL;8.8.4.0;8.8.4.255
```

```bash
$ cat list.txt|ipsurv --delimiter="\t"
8.8.8.8:53      OK      US      GOGL    8.8.8.0 8.8.8.255
8.8.4.4:53      OK      US      GOGL    8.8.4.0 8.8.4.255
```

```bash
$ cat list.txt|ipsurv --delimiter="&"
8.8.8.8:53&OK&US&GOGL&8.8.8.0&8.8.8.255
8.8.4.4:53&OK&US&GOGL&8.8.4.0&8.8.4.255
```

## Add enclose char

Add enclose char by ```--enclose```.

**Example:**

```bash
cat list.txt|ipsurv --enclose=1
cat list.txt|ipsurv --enclose='"'
"8.8.8.8:53","OK","US","GOGL","8.8.8.0","8.8.8.255"
"8.8.4.4:53","OK","US","GOGL","8.8.4.0","8.8.4.255"
```

```bash
$ cat list.txt|ipsurv --enclose="'"
'8.8.8.8:53','OK','US','GOGL','8.8.8.0','8.8.8.255'
'8.8.4.4:53','OK','US','GOGL','8.8.4.0','8.8.4.255'
```

```bash
cat list.txt|ipsurv --enclose='`'
`8.8.8.8:53`,`OK`,`US`,`GOGL`,`8.8.8.0`,`8.8.8.255`
`8.8.4.4:53`,`OK`,`US`,`GOGL`,`8.8.4.0`,`8.8.4.255`
```


## Check whether IP is in IP/subnet ranges

Set ```--range``` and ```{in_range}```.

**Example:**

```bash
$ ipsurv 192.168.1.10 1.0.0.1 --format="{in_range}" --identify_int --range="1.0.0.1/24;192.168.1.8/24"
192.168.1.10,RANGE_OK
1.0.0.1,RANGE_OK
```

```bash
$ ipsurv 10.0.0.1 --format="{in_range}" --identify_int --range="1.0.0.1/24;192.168.1.8/24"
10.0.0.1,RANGE_NG
```

## Public IP or Private IP

```bash
$ ipsurv 192.168.1.100 --format="{ip_type}"
192.168.1.100,PRIVATE
```

## IP address <--> IP int

```bash
$ ipsurv 192.168.1.100 --format="{ip_int}"
192.168.1.100,3232235876
```

```bash
$ ipsurv 16777217 --format="{ip}" --identify_int
16777217,1.0.0.1
```


## Check ICMP

```bash
$ cat list.txt|ipsurv --icmp=1
$ cat list.txt|ipsurv --icmp=1 --format="{ip},{icmp},{icmp_time}"
```

## Check TCP port

```bash
$ cat list.txt|ipsurv --tcp=1
$ cat list.txt|ipsurv --tcp=80 --format=country
$ cat list.txt|ipsurv --tcp=1 --format="{ip},{tcp},{tcp_time}"
```

## Check UDP port

```bash
$ cat list.txt|ipsurv --udp=1
$ cat list.txt|ipsurv --udp=53 --format=country --sequence
$ cat list.txt|ipsurv --udp=1 --format="{ip},{udp},{udp_time}"
```

## Check HTTP response

```bash
$ cat list.txt|ipsurv --http=1
$ cat list.txt|ipsurv --http=2 --format=country --add_ip
$ cat list.txt|ipsurv --http=2 --format="{ip},{http},{http_status},{http_h2}"
$ cat list.txt|ipsurv --http=2 --format="{ip},{http},{http_status},{http_size},{http_mime},{http_server},{http_h2}"
$ cat list.txt|ipsurv --http=2 --format="web"
```

```
$ ipsurv https://www.youtube.com/feed/you --format=web --http=1 --headers=1
original,http,http_status,http_size,http_server,http_mime,http_h2,http_time,http
https://www.youtube.com/feed/you,HTTP_OK,200,558086,ESF,text/html,N/A,184.0,HTTP_OK
```

```
$ ipsurv https://www.reddit.com --format="{ip},{http},{http_status},{http_size},{http_mime},{http_server},{http_h2},{http_time}" --http=1
https://www.reddit.com,151.101.129.140,HTTP_OK,200,707634,text/html,snooserv,N/A,130.2
```

```
$ ipsurv https://anaconda.org/ --format="{ip},{http},{http_status},{http_size},{http_mime},{http_server},{http_h2},{http_time}" --http=2
https://anaconda.org/,104.19.144.37,HTTP_OK,403,7054,text/html,cloudflare,HTTP2,86.5
```


## Apache log

```bash
$ cat /var/log/httpd/access_log|ipsurv --add_ip --no_original
192.168.56.100,OK,US,PRIVATE-ADDRESS-CBLK-RFC1918-IANA-RESERVED,192.168.0.0,192.168.255.255
~~~

$ cat /var/log/httpd/access_log|ipsurv --format=country --add_ip --no_original
$ cat /var/log/httpd/access_log|ipsurv --format=geo --add_ip --no_original
```


## Check Host name or PC name
   
```
$ ipsurv 192.168.1.120 --host_only
$ ipsurv 192.168.1.120 --format="hostname"
192.168.1.100,MYPC-00176
```

> You can also find the Windows PC name in private network.


## Survey Self

Surveying self global IP and local IP information.

**Command:**

```bash
$ ipsurv self 
```

**Result:**

```bash
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

## IP values for system

```
$ ipsurv reddit.com --format=system --add_ip --headers=1
original,ip,ip_type,ip_int,ip_hex,ip_reversed
reddit.com,151.101.129.140,PUBLIC,2540011916,97.65.81.8C,140.129.101.151
```

## Using GeoIP2

```ipsurv``` support [GeoIP2](https://github.com/maxmind/GeoIP2-python) optionally.

Please refer to the [Using GeoIP2](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/using_geoip2.html) documentation in detail.


```
$ ipsurv 8.8.8.8 --geoip_only
8.8.8.8,NA,North America,US,United States,America/Chicago,AS15169,37.751;-97.822
```

```
$ ipsurv 192.168.1.100 --format="{country},{geo}" --collect="geoip" --headers=1

$ ipsurv 8.8.8.8 --format="{continent},{continent_name},{country},{geo}" --collect="geoip" --headers=1
original,continent,continent_name,country,geo
8.8.8.8,NA,North America,US,37.751;-97.822
```

```
$ ipsurv 8.8.8.8 --collect=geoip --format=area
$ ipsurv 8.8.8.8 --format="{continent},{continent_name},{country},{country_name},{timezone},{geo}" --collect="geoip"
8.8.8.8,NA,North America,US,United States,America/Chicago,AS15169,37.751;-97.822
```

```
$ ipsurv reddit.com --geoip_only --headers=1
original,continent,continent_name,country,country_name,timezone,geo
reddit.com,NA,North America,US,United States,America/Los_Angeles,37.7642;-122.3993
```

## Enable verbose log

```
$ ipsurv 192.168.1.100 --verbose=1 # TRACE ERROR
$ ipsurv 192.168.1.100 --verbose=2 # INFO
$ ipsurv 192.168.1.100 --verbose=3 # DEBUG
```

```
$ ipsurv 192.168.1.100 --verbose=3
Enable verbose mode. Current:3 [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
2024-12-01 13:06:36,572 - INFO - ENV(IPSURV_ARGS):
{}
2024-12-01 13:06:36,573 - INFO - ENV(IPSURV_CONF):
{}
2024-12-01 13:06:36,573 - INFO - ARGUMENTS:
{ 'add_ip': False,
  'all_collect': False,
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~
2024-12-01 13:06:37,413 - INFO - RDAP:OK
2024-12-01 13:06:37,413 - INFO - RDAP_TIME(ms):832.5
2024-12-01 13:06:37,413 - DEBUG - UNNECESSARY:DNSTXT
2024-12-01 13:06:37,413 - DEBUG - UNNECESSARY:DNSREVERSE
2024-12-01 13:06:37,413 - DEBUG - UNNECESSARY:IPINFO
2024-12-01 13:06:37,414 - INFO - COLLECTED_DATA:
{ 'address': '12025 Waterfront Drive Suite 300 Los Angeles CA 90292 United '
             'States',
  'cidr': '192.168.0.0/16',
  'country': 'US',
~~~~~~~~~~~~~~~~~~~~~~~~~~~
```
