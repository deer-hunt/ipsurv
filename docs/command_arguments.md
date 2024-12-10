# [IpSurv] Command arguments reference

## Index

- [General and Debugging](#general-and-debugging)
- [Environment variable](#environment-variable)
- [Input behaviors](#input-behaviors)
- [Data collections](#data-collections)
- [Grouping](#grouping)
- [Output format](#output-format)
- [Output behaviors](#output-behaviors)
- [Server reactivity](#server-reactivity)


## General and Debugging

### `--verbose`

Verbose mode. Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG.

- **Type:** `int`
- **Default:** `0`
- **Choices:** 

| Value          | Description                                 |
|----------------|---------------------------------------------|
| 1 | TRACE_ERROR. Output error with trace.                    |
| 2 | INFO. Output setting values and internal values.  |
| 3 | DEBUG. Output maximum debug information.           |

- **Example:**

```
INPUT:
--verbose=1, --verbose=2, --verbose=3

RESULT:
Enable verbose mode. Current:3 [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
2024-10-23 18:44:19,022 - INFO - Fixed delimiter:,
2024-10-23 18:44:19,022 - INFO - Fixed format:{original},{geo}
~~~~~
```

### `--debug`

`--debug` is equivalent to `--verbose=3`.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT:
--debug

RESULT:
Enable verbose mode. Current:3 [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
2024-12-08 15:57:53,591 - INFO - ENV(IPSURV_ARGS):
~~~~~
```


### `--log`

Verbose log filename. If you specify filename, verbose log is written to a file. Use with `--verbose` option.

- **Type:** `str`
- **Default:** `None`
- **Example:**

```
INPUT: --log=app.log

RESULT:
[app.log]
--
2024-10-23 18:38:40,930 - INFO - Fixed delimiter:,
2024-10-23 18:38:40,930 - INFO - Fixed format:{original},{geo}
2024-10-23 18:38:40,930 - INFO - Fixed timeout:{'dns': 8.0, 'http': 8.0, 'reactivity': 8.0}
~~~~~
```

### `--disable_env`

Disable to load env variable for args. See **"Command arguments by Environment variable"** below for details.

- **Type:** `bool`
- **Default:** `False`
- **Example:**

```
INPUT: --disable_env
```


### `--version`

Show version information.

- **Type:** bool
- **Default:** `False`



### `--help`

Show help.


## Command arguments by Environment variable

"IpSurv" support specifying "Command arguments" by Environment variable (`IPSURV_ARGS`). You are able to change default value by Environment variable.
Also you are able to disable to load Environment variable by `--disable_env` option.

| Item       | Value  |
|---------------|--------------|
| Environment variable name  | `IPSURV_ARGS`         |
| Value format  | `JSON` *   |
*You should specify by correct JSON format.


**Example:**

```bash
$ IPSURV_ARGS='{"group": 8, "skip_duplicate": 1, "format": "network", "original": true, "sequence": true, "json": 2}'
$ export IPSURV_ARGS

RESULT:
--
{
  "sequence": 1,
  "original": "www.whitehouse.gov",
  "cidr": "192.0.64.0/18",
  "network_start": "192.0.64.0",
  "network_end": "192.0.127.255"
}
```

## "Internal configures" by Environment variable

"IpSurv" support specifying "Internal configures" by Environment variable (`IPSURV_CONF`). 

| Item       | Value  |
|---------------|--------------|
| Environment variable name  | `IPSURV_CONF`         |
| Value format  | `JSON` *   |
*You should specify by correct JSON format.

**Internal configures**

| Name       | Description  |
|---------------|--------------|
| `ipinfo_token`  |   ipinfo.io's token.        |

```bash
$ IPSURV_CONF='{"ipinfo_token": "???????"}'
$ IPSURV_CONF='{"geoip": {"path": "/home/user/GeoIP/", "files": {"country": "geoip2-country.mmdb"}}}'
$ export IPSURV_CONF
```

## Input behaviors

### `--resolve`

Resolve the name to IP if the target value is a domain or hostname automatically.

- **Type:** `bool`
- **Default:** `True`
- **Example:**

```
INPUT: --resolve=0
> Disable to resolve the name.
```

### `--identify_int`

Identifying IP's int value.

- **Type:** `bool`
- **Default:** `False`
- **Example:**

```
INPUT: ipsurv 16777217 --format="{ip_type}" --identify_int --add_ip
RESULT:
16777217,1.0.0.1,PUBLIC
```



### `--autodetect`

Autodetect an IP or hostname that is included in the line. This option is experimental.

- **Type:** bool
- **Default:** `False`
- **Example:**

```
INPUT: --autodetect=1
```

### `--begin`

Beginning line number.

- **Type:** `int`
- **Default:** `-1`

- **Example:**

```
INPUT: --begin=20
```

### `--end`

Ending line number

- **Type:** `int`
- **Default:** `-1`
- **Example:**

```
INPUT: --end=25
```


## Data collections

### `--collect`

Data collectors. Those are collected by specific order.

- **Type:** `str`
- **Default:** `'rdap;dnstxt;ipinfo;dnsreverse;geoip'`
- **Values:**

| Type        | Description                                         | Format parameters  |
|-------------|-----------------------------------------------------|----------|
| `rdap`        | Collecting by RDAP server. | country,cidr,network_start,network_end,country_updated,<br>name,port43,handle,org,address,description    |
| `dnstxt`      | Collecting by DNS TXT record. | country,cidr,network_start,network_end,rir    |
| `ipinfo`   | Collecting by reverse ipinfo.net. | country,hostname,city_name,region_name,postal,geo,org,timezone    |
| `dnsreverse`      | Collecting by DNS lookup. | hostname    |
| `geoip`      | Collecting by geoip. | continent, continent_name, country, country_name, timezone, geo, asn, org, (city, city_name)    |

- **Example:**

```
INPUT: 
--collect="rdap;dnstxt"  # rdap -> dnstxt
--collect="ipinfo"
--collect="geoip"
--collect="geoip;ipinfo" # geoip -> ipinfo
--collect="ipinfo;geoip" # ipinfo -> geoip
```

### `--all_collect`

Activate all data collections. Normally, the data collection is done at the minimum required. The collection of further data will be skipped if the required data is sufficient.
If this option is activated, continuing to collect data forcibly.

- **Type:** bool
- **Default:** `False`
- **Example:**

```
INPUT:
--all_collect --json=2 --exhaustive

RESULT:
{
  "success": true,
  "status": "OK",
  "requests": [
    "RDAP",
    "DNSTXT",
    "DNSREVERSE",
    "IPINFO"
  ],
  "errors": [],
  "sequence": 1,
  "original": "www.cao.go.jp",
  "target_raw": "www.cao.go.jp"
  ~~ All data ~~
}
```


### `--timeout`

Timeout in seconds. Specify a single value (e.g., `1`, `3.2`) or specify values for each connection type.

- **Type:** `float, str`
- **Default:** `'8.0'`

| Type           | Description                           | Example                              |
|----------------|---------------------------------------|--------------------------------------|
| Single value   | Common timeout.                       |  8.2                                    |
| Multiple value | DNS timeout, HTTP timeout, Reactivity timeout. | "3;5;6", "2.5;2.5;6.2"         |

- **Example:**

```
INPUT: --timeout=5.1, --timeout=12, --timeout="3;5.1;6"
```

## Grouping

### `--group`

Grouping rule. You can specify "Subnet mask", "CIDR", "network".  e.g.: `255.255.255.0`, `24`, `network`

- **Type:** `str`
- **Default:** `None`

| Type      | Example                    |
|----------------|----------------------------|
| Subnet mask     | 255.255.255.0              |
| CIDR value      | 24                         |
| Group by provider-aggregatable address         | network    |

- **Example:**

```
INPUT: --group=8, --group=network
```


### `--skip_duplicate`

Skip duplicate group. Use with `--group` option. If you don't specify `--group` option, skipping duplicate ip.

- **Type:** `int`
- **Default:** `0`
- **Choices:** `[0, 1, 2]`

| Value | Description                                                      |
|-----|------------------------------------------------------------------|
| 1   | Skip duplicate group.                                |
| 2   | It also skips checking server reactivity [icmp, tcp, udp, http]. |


- **Example:**

```
INPUT:
--skip_duplicate=1, --skip_duplicate=2

RESULT:
8.8.8.8:53,OK,8.8.8.8,US,GOGL,8.8.8.0,8.8.8.255,dns.google
8.8.8.8:53,SKIP,8.8.8.8,,,,,
```

### `--range`

Check whether IP is in IP/subnet ranges.  The value is CIDR notation. ex: "1.0.0.1/8;192.168.1.1/24"

- **Type:** `str`
- **Default:** ``

- **Example:**

```
INPUT:
--range="1.0.0.1/24;1.1.0.8/24" --format="{in_range}"

RESULT:
192.168.1.10,RANGE_OK
2.2.2.2,RANGE_NG
```


## Output format

### `--format`

Output format. Specify `Profile` or `Parameter`. 
> The define of profiles and parameters is `Config.FORMAT_PROFILES` and `Config.FORMAT_PARAMS` in `./config.py`.

| Type     | Value                        |
|----------|--------------------------------|
| Profile  | `"profile"`, `"<profile>"`        |
| Parameter | `"{parameter}"`                |
| Mixed    | `"<profile>,{parameter}"`      |

- **Type:** Str
- **Default:** `default`
- **Values:**

**Profiles**

| Profile        | Description                |
|------------|----------------------------------------------------------------|
| **ip**         | IP address.                |
| **hostname**   | Hostname.                |
| **country**   | Country code.           |
| **org**     | Organization.            |
| **address**    | Address.    |
| **timezone**   | Timezone.                      |
| **network**    | CIDR.              |
| **geo**        | Geolocation with Country code.                  |
| **area**        | Country name, Geo, Timezone, etc..                  |
| **system**        | IP for system. ip_int, ip_hex, ip_reversed                  |
| **web**       | HTTP response.     |
| **simple**     | Group, Country.      |
| **default**    | Group, Country, Network, Hostname.|
| **detail**     | Default + Organization, CIDR, Address, Description.       |
| **heavy**    | Heavy parameters. |

> You can see concrete profile's parameters by using `--headers=1` option.

**Parameters**

> In the case of JSON output, "OK" and "NG" will be output as "true" and "false".

| Parameter               | Description                  | e.g.               |
|--------------------|------------------------------------|------------------------|
| **success**            | Success or Failure.               | OK, NG                   |
| **status**             | Status.                     | ILLEGAL_FORMAT , RESOLVE_FAIL           |
| **requests**           | Requested collects. If multiple collections by ```--collect``` is specified, data that does not need to be collected will not be requested.    | ["RDAP", "DNSREVERSE", "IPINFO"]                      |
| **errors**             | Error messages.                   | ["[Errno 1] Unknown host"]          |
| **sequence**           | Line number.                    | 1                  |
| **original**           | Original input data.                      | 8.8.8.8                 |
| __target.*__         | Internal variables.                    | 8.8.8.8          |
| **ip**                 | IP address.                         | 192.168.1.100          |
| **ip_int**             | IP int value.       | 3232235777             |
| **ip_hex**             | IP HEX value.       | 8E.FA.C4.6E         |
| **ip_reversed**       | Reverse IP address notation.       | 100.1.168.192             |
| **port**               | Port. If the port was identified.          | 80                     |
| **ip_type**            | Type of IP.                         | PUBLIC, PRIVATE                 |
| **in_range**            | Whether IP is within in cidr range. Refer to ```--range``` option.                         | RANGE_OK, RANGE_NG       |
| **group**              | Group value. If ```--group``` is specified.      | 8.8.8.1                |
| **group_int**          | Group int value                   | 3232235777               |
| **group_found**        | Grouped or Not             | OK, NG       |
| **group_status**       | Group status. Ex: First grouping.                       | FOUND, NEW               |
| **network_start**      | Start IP of the network. If ```--group``` is specified.          | 192.168.1.0          |
| **network_end**        | End IP of the network. If ```--group``` is specified.         | 192.168.1.255        |
| **cidr**               | CIDR notation.                      | 192.168.1.0/24       |
| **hostname**           | Reverse hostname.                           | nrt4512s35-in-f14.1e200.net      |
| **icmp**               | ICMP status.                          | OK, NG |
| **icmp_time**          | ICMP request ms time.                  | 100.9 |
| **tcp**                | TCP status.                           | OK, NG |
| **tcp_time**           | TCP request ms time.                   | 50.9 |
| **udp**                | UDP status.                           | OK, NG   |
| **udp_time**           | UDP request ms time.                   | 100.8 |
| **http**               | HTTP status.                          | OK, NG   |
| **http_time**          | HTTP request ms time.                  | 200.9 |
| **http_status**        | HTTP response status.               | 200, 404   |
| **http_size**          | Size of HTTP response.              | 10243                    |
| **http_h2**           | HTTP/2 support status.                       | HTTP2     |
| **rdap_time**          | RDAP request ms time.                  | 10.9 |
| **dnstxt_time**        | DNS TXT record ms time.                | 15.9 |
| **dnsreverse_time**    | DNS reverse lookup ms time.            | 30.9 |
| **ipinfo_time**        | IP information retrieval ms time.      | 20.9 |
| **geo**                | Geographical coordinates. (latitude and longitude) | 37.7642;-122.3993 |
| **timezone**           | Timezone. | America/Los_Angeles |
| **asn**                | ASN.                   | AS115169 |
| **org**                | Organization name.                  | Example Organization Inc.  |
| **name**               | Identifying name in RDAP.                               | SKYCA-4          |
| **handle**             | Handle value.                        | SKYCA-4          |
| **region_name**        | Region name.                | California                |
| **country**            | Country code.                       | US                |
| **country_name**       | Country name.  | United States |
| **country_updated**    | Whether the country was updated by parsing the address. | true, false  |
| **city**               | City code.                    |  |
| **city_name**          | City name.               | San Francisco |
| **postal**             | Postal code.                        | 194107             |
| **address**            | Address.                            | PO Box 25782669 San Francisco CA 194107 United States      |
| **description**        | Description in RDAP.                        | "Example description"   |
| **rir**                | Regional Internet Registry.         | ARIN                 |
| **port43**             | Whois server by RDAP data.           | whois.arin.net   |
| **continent**          | Continent code. | NA  |
| **continent_name**     | Continent name. | North America |
| **subdivision**        | Subdivision code.  | CA |
| **subdivision_name**   | Subdivision name. | California  |



- **Example:**

```
INPUT: 
--format="simple", --format="{success},{country},{http}", --format="{sequence},{ip},{country},<network>"

RESULT:
1,www.whitehouse.gov,37.7749;-122.4194
2,www.state.gov,35.6895;139.6917
3,www.treasury.gov,35.6895;139.6917
```

### `--sequence`

Append sequence number.

- **Default:** `False`
- **Example:**

```
INPUT: --sequence --format=geo

RESULT:
1,www.whitehouse.gov,37.7749;-122.4194
2,www.state.gov,35.6895;139.6917
3,www.treasury.gov,35.6895;139.6917
```

### `--no_original`

Cancel outputting the original line automatically..

- **Type:** `bool`
- **Default:** `False`
- **Example:**

```
INPUT: --no_original

RESULT:
37.7749;-122.4194
35.6895;139.6917
```

### `--add_ip`

Append "ip" to the output format. For example, use when the target is a hostname, etc.

- **Type:** `bool`
- **Default:** `False`
- **Example:**

```
INPUT: --add_ip --format=default

RESULT:
www.whitehouse.gov,192.0.66.168,OK,,US,AUTOMATTIC,192.0.64.0,192.0.127.255
www.state.gov,3.165.39.61,OK,,US,AMAZON-CF,3.165.0.0,3.165.255.255
```


### `--ident`

Append identifier. Default identifier is ip.

- **Type:** `bool`
- **Default:** `False`
- **Example:**

```
INPUT: --ident --format=geo

RESULT:
www.whitehouse.gov,192.0.66.168,37.7749;-122.4194
www.state.gov,3.165.39.26,35.6895;139.6917
```


### `--enclose`

Character to enclose in result line. If you specify "json" option, this option is disabled. e.g.: `'"'`, `"'"`,`1`, `2`, `3`

- **Type:** `int, str`
- **Default:** `None`
- **Example:**

```
INPUT:
--enclose='"', --enclose=1, --enclose=2, --enclose=3

RESULT:
'"': "www.whitehouse.gov","37.7749,-122.4194"
1: "www.whitehouse.gov","37.7749,-122.4194"
2: 'www.whitehouse.gov','37.7749,-122.4194'
3: |www.whitehouse.gov|,|37.7749,-122.4194|

'"': "Address ,""Building"", U.S.","35.8901,-106.2952"
"{""ip"":""8.8.8.8"",""hostname"":""hostname.com"",""port"":80}", "OK"
```


### `--delimiter`

Delimiter character in result. If this option is not specified, detecting a char automatically from "--format" option.

- **Type:** `str`
- **Default:** `None`
- **Example:**

```
INPUT:
--delimiter="\t", --delimiter=";"

RESULT:
www.gov.uk      37.7621,-122.3971
www.gouvernement.fr;48.8534,2.3488
```

### `--alt_delimiter`

Alternative delimiter character. If you specify "enclose" or "json" option, this option is disabled.

- **Type:** `str`
- **Default:** `;`
- **Example:**

```
INPUT: --alt_delimiter=";"

RESULT:
www.state.gov,NG,,US,AMAZON-CF,AMAZON-4,Amazon.com; Inc.,3.165.0.0/16,1918 8th Ave SEATTLE WA 98101-1244 United States,,server-3-165-39-15.nrt12.r.cloudfront.net
```

## Output behaviors

### `--headers`

Show headers.

- **Type:** `int`
- **Default:** `0`
- **Choices:** `[0, 1, 2, 3]`

| Value | Description        |
|-----|--------------|
| 1   | LowerCase    |
| 2   | PascalCase   |
| 3   | UpperCase    |

- **Example:**

```
INPUT: --headers=1, --headers=2

RESULT:
1: sequence;original;status;group;country;name;handle;org;cidr;address;hostname
2: Sequence;Original;Status;Group;Country;Name;Handle;Org;Cidr;Address;Hostname
3: SEQUENCE;ORIGINAL;STATUS;GROUP;COUNTRY;NAME;HANDLE;ORG;CIDR;ADDRESS;HOSTNAME
```

### `--json`

Output JSON data.

- **Type:** `int`
- **Default:** `0`
- **Choices:** `[0, 1, 2]`

| Value          | Description                |
|-----------------|----------------------------|
| 1 | One line of JSON.     |
| 2 | Formatted JSON. |


- **Example:**

```
INPUT: --json=1

RESULT:
{"sequence": 1, "original": "www.canada.ca", "geo": "35.6895,139.6917"}
```


### `--json_list`

Output JSON data by list. It makes it easier to parse JSON.

- **Type:** `bool`
- **Default:** `False`
- **Example:**

```
INPUT: --json=1 --json_list

RESULT:
[
{"original": "www.whitehouse.gov", "status": "NG", "group": "", "country": "US", "hostname": ""},
{"original": "www.state.gov", "status": "OK", "group": "", "country": "US", "hostname": "server-3-165-39-129.nrt12.r.cloudfront.net"},
]
```


### `--exhaustive`

Output exhaustive internal values in JSON. Use with "json" option.

- **Type:** bool
- **Default:** `False`
- **Example:**

```
INPUT: --json=2 --exhaustive

RESULT:
{
  "success": true,
  "status": "OK",
  "requests": [
    "IPINFO"
  ],
  "errors": [],
  "sequence": 1,
  "original": "********",
  "target_raw": "********",
  "target": "160.*.*.*",
  "ip": "160.*.*.*",
  "ip_int": ******,
  "port": null,
  "group_int": 0,
  "group": "",
  "group_found": false,
  "group_status": "-",
  "name": "*********",
  "network_start": "********",
  "network_end": "********",
  "ip_hex": "********",
  "ip_reversed": "********",
  "ip_type": "PUBLIC",
  "geo": "35.5333,139.6100",
  "ipinfo_time": 171.3,
  "hostname": "",
  "country": "JP",
  "city_name": "Marunouchi",
  "region_name": "Tokyo",
  "postal": "******",
  "org": "******** Inc.",
  "timezone": "Asia/Tokyo"
}
```

### `--json_all`

`--json_all` is equivalent to `--json=2 --exhaustive`.

- **Type:** bool
- **Default:** `False`
- **Example:**

```
INPUT: --json_all

RESULT:
{
  "success": true,
  "status": "OK",
  "requests": [
    "IPINFO"
  ],
  "errors": [],
  "sequence": 1,
  "original": "********",
  "target_raw": "********",
  "target": "160.*.*.*",
  "ip": "160.*.*.*",
  "ip_int": ******,
  "port": null,
  "group_int": 0,
  "group": "",
  "group_found": false,
  "group_status": "-",
  "name": "*********",
  "network_start": "********",
  "network_end": "********",
  "ip_hex": "********",
  "ip_reversed": "********",
  "ip_type": "PUBLIC",
  "geo": "35.5333,139.6100",
  "ipinfo_time": 171.3,
  "hostname": "",
  "country": "JP",
  "city_name": "Marunouchi",
  "region_name": "Tokyo",
  "postal": "******",
  "org": "******** Inc.",
  "timezone": "Asia/Tokyo"
}
```


### `--geoip`

`--geoip_only` is equivalent to `--collect=geoip --format=area`.

- **Type:** bool
- **Default:** `False`
- **Example:**

```
INPUT:
$ ipsurv google.com --geoip

RESULT:
google.com,NA,North America,US,United States,America/New_York,40.7306;-73.4313
```

##  Server reactivity

### `--icmp`

Check ICMP. "ping" command is used.

- **Type:** `bool`
- **Default:** `False`

**Activate format parameters**

| Parameter    | Description                                           |
|--------------|-------------------------------------------------------|
| icmp         | T/F. If the response is success, the value is True. |
| icmp_time    | Millisecond time to response.                        |


- **Example:**

```
INPUT: --icmp=1
```

### `--tcp`

Check TCP port. Specify the default port. If there is a port value in line, those value is used. e.g.: 192.168.1.10:80

- **Type:** `int`
- **Default:** `0`

**Activate format parameters**

| Parameter    | Description                                           |
|--------------|-------------------------------------------------------|
| tcp         | T/F. If the response is success, the value is True. |
| tcp_time    | Millisecond time to response.                        |


- **Example:**

```
INPUT: --tcp=1, --tcp=80
```


### `--udp`

Check UDP port. Specify the default port. If there is a port value in line, those value is used. e.g.: 192.168.1.10:53

- **Type:** `int`
- **Default:** `0`

**Activate format parameters**

| Parameter    | Description                                           |
|--------------|-------------------------------------------------------|
| udp         | T/F. If the response is success, the value is True. |
| udp_time    | Millisecond time to response.                        |


- **Example:**

```
INPUT: --udp=1, --udp=53
```


### `--http`

Check HTTP response.

- **Type:** `int`
- **Default:** `0`
- **Choices:** `[0, 1, 2]`

| Value | Description                                                               |
|-----|---------------------------------------------------------------------------|
| 1   | Check HTTP or HTTPS response.                                             |
| 2   | Check "HTTP/2" by checking h2 support of TLS ALPN.             |


**Activate format parameters**

| Parameter    | Description                                           |
|--------------|-------------------------------------------------------|
| http         | T/F. If HTTP status code is 200, the value is True. |
| http_status  | Response HTTP status code.                            |
| http_size    | Response byte size.                                  |
| http_h2      | HTTP/2 enabled or not.                               |
| http_time    | Millisecond time to response.                        |


- **Example:**

```
INPUT: --http=1, --http=2
```

