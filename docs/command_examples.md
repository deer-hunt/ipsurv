# [IpSurv] Command examples

This is several command examples. You can understand some usage and features. In detail usage, Please read [Command Arguments reference](command_arguments.md).

## Basic usage

### Specifying IP

Surveying a IP and some IPs.

**Command:**

```
# ipsurv 8.8.8.8
8.8.8.8,OK,,US,GOGL,8.8.8.0,8.8.8.255,dns.google

# ipsurv 8.8.4.4 1.1.1.1
8.8.4.4,OK,,US,GOGL,8.8.4.0,8.8.4.255,dns.google
1.1.1.1,OK,,AU,APNIC-LABS,1.1.1.0,1.1.1.255,one.one.one.one
```

### Specifying domain

Surveying a domain and some domains.

**Command:**

```
# ipsurv www.wikipedia.org
www.wikipedia.org,OK,,US,WIKIMEDIA-AP,103.102.166.0,103.102.166.255,text-lb.eqsin.wikimedia.org

# ipsurv www.reddit.com stackoverflow.com
www.reddit.com,NG,,US,SKYCA-3,151.101.0.0,151.101.255.255,
stackoverflow.com,NG,,US,CLOUDFLARENET,172.64.0.0,172.71.255.255,
```


### Multiple rows using pipe

"IpSurv" support the input by pipe. You are able to specify multiple rows.

**Example:**

```
# cat urls.txt|ipsurv
www.whitehouse.gov,NG,,US,AUTOMATTIC,192.0.64.0,192.0.127.255,
www.state.gov,OK,,US,AMAZON-CF,3.165.0.0,3.165.255.255,server-3-165-39-26.nrt12.r.cloudfront.net
~~~~~~
```

## Various output-format

You can specify output-format flexibly by `--format` option.

**Example:**

```
# cat list.txt|ipsurv --format=simple
# cat list.txt|ipsurv --format=hostname --ident
# cat list.txt|ipsurv --format=geo
# cat list.txt|ipsurv --format="{country},{group},{geo},{original}"
# cat list.txt|ipsurv --format=timezone
# cat list.txt|ipsurv --format="{status},{group},{country},{name},{hostname}"
# cat list.txt|ipsurv --format="{status},<web>,{ip}"
# cat list.txt|ipsurv --format="{status}\t{ip}\t{hostname}"
```

## Outputting JSON

Outputting JSON by `--json` option.

**Example:**

```
# cat list.txt|ipsurv --json=1
{"original": "www.whitehouse.gov", "status": "NG", "group": "", "country": "US", "name": "AUTOMATTIC", "network_start": "192.0.64.0", "network_end": "192.0.127.255", "hostname": ""}

# cat list.txt|ipsurv --json=2
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

# cat list.txt|ipsurv --json=1 --json_list --begin=1 --end=2 --format="{ip},{geo},{country}"
[
{"original": "www.whitehouse.gov", "ip": "192.0.66.168", "geo": "37.7749,-122.4194", "country": "US"},
{"original": "www.state.gov", "ip": "3.165.39.61", "geo": "35.6895,139.6917", "country": "JP"},
]
```

## Starting line-number and Ending line-number

Set starting line-number and ending line-number.

**Example:**

```
# cat list.txt|ipsurv --begin=10
# cat list.txt|ipsurv --begin=25 --end=50 --sequence
```

## Grouping

You are able to group by subnet or provider network by `--group` option. And Skipping the duplicate group using `--skip_duplicate`.

```
# cat list.txt|ipsurv --group=255.255.255.0 --skip_duplicate=1
# cat list.txt|ipsurv --group=24
# cat list.txt|ipsurv --group=network --skip_duplicate=1
```

## Timeout

Set request timeout.

**Example:**

```
# cat list.txt|ipsurv --timeout=5.1
# cat list.txt|ipsurv --timeout="3.5;4.5;3.2"
```

## Check ICMP

```
# cat list.txt|ipsurv --icmp=1
# cat list.txt|ipsurv --icmp=1 --format="{ip},{icmp},{icmp_time}"
```

## Check TCP port

```
# cat list.txt|ipsurv --tcp=1
# cat list.txt|ipsurv --tcp=80 --format=country
# cat list.txt|ipsurv --tcp=1 --format="{ip},{tcp},{tcp_time}"
```

## Check UDP port

```
# cat list.txt|ipsurv --udp=1
# cat list.txt|ipsurv --udp=53 --format=country --sequence
# cat list.txt|ipsurv --udp=1 --format="{ip},{udp},{udp_time}"
```

## Check HTTP response

```
# cat list.txt|ipsurv --http=1
# cat list.txt|ipsurv --http=2 --format=country --ident
# cat list.txt|ipsurv --http=2 --format="{ip},{http},{http_h2}"
```


## Apache log

```
# cat /var/log/httpd/access_log|ipsurv --format=country --ident --no_original
# cat /var/log/httpd/access_log|ipsurv --format=geo --ident --no_original
```

## Survey Self

Surveying self global IP and local IP information.

**Command:**

```
# ipsurv self 
```

**Result:**

```
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

