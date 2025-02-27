# Introduction to "ipsurv"

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

`ipsurv` have two Survey-mode. Those are "Survey IPs" and "Survey Self". 

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
- Use GeoIP2 via ipsurv optionally.

## Command options

`ipsurv` have many options. Please read [Command arguments(.md) reference](https://deer-hunt.github.io/ipsurv/pages/ipscap-cmd/command_arguments.html).

**Options**

```
ipsurv [-h] [--verbose {0,1,2,3}] [--debug] [--log {string}]
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
$ ipsurv wikipedia.org --json_all    # `--json_all` is equivalent to `--json=2 --exhaustive`
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

**Check HTTP response**

```
$ ipsurv https://www.reddit.com --format="{ip},{http},{http_status},{http_size},{http_mime},{http_server},{http_h2},{http_time}" --http=1
https://www.reddit.com,151.101.129.140,HTTP_OK,200,707634,text/html,snooserv,N/A,130.2

$ ipsurv https://anaconda.org/ --format="{ip},{http},{http_status},{http_size},{http_mime},{http_server},{http_h2},{http_time}" --http=2
https://anaconda.org/,104.19.144.37,HTTP_OK,403,7054,text/html,cloudflare,HTTP2,86.5

$ ipsurv https://www.youtube.com/feed/you --format=web --http=2 --headers=1
original,http,http_status,http_size,http_server,http_mime,http_h2,http_time,http
https://www.youtube.com/feed/you,HTTP_OK,200,558086,ESF,text/html,HTTP2,284.0,HTTP_OK
```

**Check Host name or PC name**

```
$ ipsurv 192.168.1.120 --host_only
$ ipsurv 192.168.1.120 --format="hostname"
192.168.1.100,MYPC-016
```

> You can also find the Windows PC name in private network.

More examples are [here](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_examples.html).


## Output Format

You can customize "Output Format" by ```--format``` option as follows. There are ```parameter - {}``` and ```profile - <>``` in ```--format```.
For more information, please read [--format description](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#format), [Profiles](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#profiles), [Parameters](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#parameters).

```
$ ipsurv github.io --format=heavy            # Profile
$ ipsurv github.io --format=simple           # Profile

$ ipsurv 8.8.8.8 --format="{status},{ip},{country},{address}"   # Parameters
$ ipsurv 8.8.8.8 --format="{status}\t{ip}\t{hostname}"         # Parameters, TAB char

$ ipsurv cloudflare.com --format="{ip},<address>,<system>"      # Parameters + Profile
$ ipsurv wikipedia.org --format="<address>,{hostname},{ip_type}"     # Profile + Parameters
```


## Using GeoIP2 optionally

`ipsurv` support [GeoIP2](https://github.com/maxmind/GeoIP2-python) optionally. If ```GeoIP2``` module is installed and there are ```mmdb``` files, You can use GeoIP2 features via `ipsurv`.
When using the GeoIP2 module, network communication does not occur, which enables faster processing.

Please refer to the [Using GeoIP2](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/using_geoip2.html) documentation in detail.

**Examples**

```
$ ipsurv 8.8.8.8 --geoip_only
8.8.8.8,NA,North America,US,United States,America/Chicago,AS15169,37.751;-97.822
```

```
$ ipsurv www.wikipedia.org --format="{country},{geo}" --collect=geoip --headers=1
original,country,geo
www.wikipedia.org,US,37.751;-97.822

$ ipsurv 8.8.8.8 --format="{continent},{continent_name},{country},{geo}" --collect="geoip" --headers=1
original,continent,continent_name,country,geo
8.8.8.8,NA,North America,US,37.751;-97.822
```

> `IpSuv` support customizing GeoIP2 data path by `IPSURV_CONF` env. Please read [here](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html#environment-variable-ipsurv-conf) about `IPSURV_CONF`.


## Documents

The following documents exist in `ipsurv`. You can read documents in [Documentation site](https://deer-hunt.github.io/ipsurv/).

| Title                       | Path                                        |
|-------------------------------|---------------------------------------------|
| **Command arguments**    | [command_arguments.md](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_arguments.html) |
| **Command examples**               | [command_examples.md](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/command_examples.html)   |
| **Program architecture and Classes** | [program_architecture_classes.md](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/program_architecture_classes.html) |
| **Customizing and Examples**       | [customize_examples.md](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/customize_examples.html) |
| **Development and Debugging**          | [development_debug.md](https://github.com/deer-hunt/ipsurv/blob/main/docs/development_debug.md)   |
| **About Using GeoIP2** | [using_geoip2.md](https://deer-hunt.github.io/ipsurv/pages/ipsurv-cmd/using_geoip2.html)  |
| **ipsurv's Major Modules and Classes** | [github.io / Modules and Classes reference](https://deer-hunt.github.io/ipsurv/py-modindex.html)  |


## Debugging

In verbose mode, outputting internal data and behaviors in detail.

```bash
$ ipsurv ***** --verbose=2    #INFO
$ ipsurv ***** --verbose=3    #DEBUG

$ ipsurv ***** --debug     #DEBUG  This option is equivalent to "--verbose=3"
```

## Customizing ipsurv

`ipsurv` is implemented as customizable program architecture. `ipsurv` provide extending features and several classes. 
And you can use ipsurv's internal classes in your program. Please read ```program_architecture_classes.md```.

**Classes for major customization**

| Classes    | Description            |
|----------------------|----------------------------------------------|
| **Pipeline**   | Pipeline class provide catching and customizing the data in each processing. ```./examples/pipeline_customize.py```         |
| **ObjectFactory**   | ObjectFactory class provide customizing classes and creating original classes. ```./examples/object_factory.py```      |
| **Serializer, LineSerializer, JsonSerializer**   | Serializer class provide displaying data and transforming data for presentation. ```./examples/object_factory_original_headers.py```      |


## Dependencies

- [dnspython](https://github.com/rthalley/dnspython)
- [geoip2](https://github.com/maxmind/GeoIP2-python) [Optional]
