# [IpSurv] About Using GeoIP2

## Overview

```IpSurv``` support [GeoIP2](https://github.com/maxmind/GeoIP2-python) optionally. If ```GeoIP2``` module is installed and there are ```mmdb``` files, You can use GeoIP2 features via ```IpSurv```.

When using the GeoIP2 module, network communication does not occur, So fast processing can be realized.

```GeoIP2``` is a MaxMind inc's product. There are free version and paid version in ```GeoIP2```.
Free version is [GeoLite2](https://github.com/P3TERX/GeoLite.mmdb). Paid version is [GeoIP Databases](https://www.maxmind.com/en/geoip-databases).

- [Development document](https://dev.maxmind.com/geoip/)
- [MaxMind website](https://www.maxmind.com/en/home)

## GeoIP2 Installation

It's required installing geoip2 python module to use by ```IpSurv```.

```
$ pip install geoip2
```

For more details, please read [here](https://github.com/maxmind/GeoIP2-python).

## Setup GeoIP2 data

After installing GeoIP2 module, Setup GeoIP2 data files - ```mmdb file```.

GeoLite2's data files are [here](https://github.com/P3TERX/GeoLite.mmdb). For the paid version, check the MaxMind web page.
And Store ```mmdb file``` to specified path.

**Example dirs**

- /usr/local/share/GeoIP/

**Example file paths**

- /usr/local/share/GeoIP/GeoLite2-City.mmdb
- /usr/local/share/GeoIP/GeoLite2-Country.mmdb
- /usr/local/share/GeoIP/GeoLite2-ASN.mmdb


## IpSurv's settings

```IpSurv``` detect GeoIP2 typical data dirs and data files automatically. So if the path configuration is as follows, it's unnecessary to settings.

### a. Auto-detect path

**Data dirs**

- /usr/local/share/GeoIP/
- /var/lib/GeoIP/
- /opt/geoip/
- ~/geoip/

**Data files**

- GeoLite2-Country.mmdb, GeoIP2-Country.mmdb
- GeoLite2-City.mmdb, GeoIP2-City.mmdb
- GeoLite2-ASN.mmdb, GeoIP2-ASN.mmdb

### b. Specify path manually

If you'd like to specify paths manually, specifying IpSurv's environment variables - ```IPSURV_CONF```. 

#### IPSURV_CONF's geoip parameters

- Root parameter name is ```geoip```.

-  The structure of the ```geoip``` parameter is as follows.

| Param name    | Description                          | e.g.                 |
|--------|--------------------------------|----------------|
| ```path```   | GeoIP's data directory path.             | /home/user/GeoIP/ |
| ```files```  |  GeoIP's data file names.                    | --
|  ├ ```country``` | Country data file.         | geoip2-country.mmdb   |
|  ├ ```city``` | City data file.         | geoip2-city.mmdb   |
|  ├ ```asn``` | ASN data file.         | geoip2-asn.mmdb   |

#### Examples

**Example1: Output environment variable**

```
$ IPSURV_CONF='{"geoip": {"path": "/home/user/GeoIP/", "files": {"country": "geoip2-country.mmdb"}}}'
$ export IPSURV_CONF
```

**Example2: Add environment variable to ".bashrc"**

```
$ vi ~/.bashrc

Append "IPSURV_CONF" setting.
--
IPSURV_CONF='{"geoip": {"path": "/home/user/GeoIP/", "files": {"country": "geoip2-country.mmdb", "city": "geoip2-city.mmdb"}}}'
export IPSURV_CONF
--

$ source ~/.bashrc
```


## Run IpSurv command

After installation and setup, you can use GeoIp2 features via IpSurv. Here are some usage examples.

**--geoip_only option**

`--geoip_only` is equivalent to `--collect=geoip --format=area`.

```
$ ipsurv 8.8.8.8 --geoip_only
8.8.8.8,NA,North America,US,United States,America/Chicago,AS15169,37.751;-97.822
```

**--collect=geoip option**

```
$ ipsurv 8.8.8.8 --format="{continent},{continent_name},{country},{geo}" --collect="geoip" --headers=1
original,continent,continent_name,country,geo
8.8.8.8,NA,North America,US,37.751;-97.822
```

**Specify domain**

```
$ ipsurv www.wikipedia.org --format="{country},{geo}" --collect=geoip --headers=1
original,country,geo
www.wikipedia.org,US,37.751;-97.822
```

**Bulk Surveying**

```
$ cat ./example_data/government.txt|ipsurv --geoip_only --headers=1
original,continent,continent_name,country,country_name,timezone,geo
www.whitehouse.gov,NA,North America,US,United States,America/Los_Angeles,37.7809;-122.4245
www.state.gov,NA,North America,US,United States,America/Chicago,37.751;-97.822
www.treasury.gov,AS,Asia,JP,Japan,Asia/Tokyo,35.6893;139.6899
www.gov.uk,NA,North America,US,United States,America/Los_Angeles,37.7642;-122.3993
www.gov.uk,NA,North America,US,United States,America/Los_Angeles,37.7642;-122.3993
www.gouvernement.fr,EU,Europe,FR,France,Europe/Paris,48.8582;2.3387
www.diplomatie.gouv.fr,EU,Europe,FR,France,Europe/Paris,48.7688;2.3536
```


### Parameters

Parameters in ```--format```  that can be specified by the GeoIP2 features are as follows.

| Parameter          | Description                               |
|--------------------|-------------------------------------------|
| ```continent```          | Continent code. |
| ```continent_name```     | Continent name. |
| ```country```            | Country code. |
| ```country_name```       | Country name.  |
| ```subdivision```        | Subdivision code. Not support GeoLite2.  |
| ```subdivision_name```   | Subdivision name. Not support GeoLite2. |
| ```city```               | City code. Not support GeoLite2.                    |
| ```city_name```          | City name. Not support GeoLite2.                |
| ```timezone```           | Timezone. |
| ```geo```                | Geographical coordinates (latitude and longitude) |
| ```asn```                | ASN.                   |
| ```org```                | Organization. |

## About "collect" mode

When using GeoIp2, ```--collect=geoip``` or ```--geoip_only``` is recommended.  Default value of ```collect option``` is ```rdap;dnstxt;ipinfo;dnsreverse;geoip```, therefore, GeoIP2 data collection is ran last.

**Recommend option**

```--collect=geoip``` or ```--geoip_only```

**Prefer GeoIP2**

```--colect="geoip;ipinfo"```

**Supplemented by GeoIP2**

```--colect="rdap;ipinfo;geoip"```


## Troubleshooting

If you are unable to use GeoIP2 features despite having installed it correctly, please refer to the following.

**Output debug information by ```--debug```**

```
$ ipsurv reddit.com --geoip_only --headers=1 --debug
```

**Error example1** 

The following example shows a failure to load GeoIP2 data file due to a "path" specification error, ```/home/dummy/GeoIP/```.
Check each "CHECK" points.

```
2024-12-09 07:47:42,608 - INFO - ENV(IPSURV_ARGS):
{}
2024-12-09 07:47:42,608 - INFO - ENV(IPSURV_CONF):        # [CHECK-1] ---------------------------------- Load IPSURV_CONF.
{ 'geoip': { 'files': {'country': 'country.mmdb'},
             'path': '/home/dummy/GeoIP/'}}                    # Error
2024-12-09 07:47:42,608 - INFO - ARGUMENTS:
~~~~~~~~~~~~~~~~~~~~~
2024-12-09 07:47:42,608 - INFO - ARGUMENTS_JSON:
~~~~~~~~~~~~~~~~~~~~~
2024-12-09 07:47:42,608 - INFO - Fixed delimiter:,
2024-12-09 07:47:42,609 - INFO - Fixed format:{original},{continent},{continent_name},{country},{country_name},{timezone},{geo}
2024-12-09 07:47:42,609 - INFO - Fixed timeout:{'dns': 8.0, 'http': 8.0, 'reactivity': 8.0}
2024-12-09 07:47:42,609 - INFO - Fixed enclose:
2024-12-09 07:47:42,609 - INFO - Fixed ranges:[]
2024-12-09 07:47:42,609 - INFO - Fixed collectors:['geoip']
2024-12-09 07:47:42,609 - INFO - MODE:SURVEY_IPS
2024-12-09 07:47:42,616 - INFO - GEOIP:ENABLED                  # [CHECK-2] ---------------------------------- GEOIP is enabled.
2024-12-09 07:47:42,616 - INFO - GEOIP_DATA_PATH:/home/dummy/GeoIP/ # [CHECK3] ---------------------- Data path.
2024-12-09 07:47:42,616 - INFO - GEOIP_DATA_FILES:{'country': 'country.mmdb', 'city': None, 'asn': None} # [CHECK4] ------ Data files.
~~~~~~~~~~~~~~~~~~~~~~
2024-12-09 07:47:42,623 - DEBUG - GEOIP ERROR                  # [CHECK-5] --------------------------------- Error occur
Traceback (most recent call last):
  File "/path/to/ipsurv/data_collector/data_collector.py", line 33, in request
    (success, response) = self.request_data(target, requires)
  File "/path/to/ipsurv/data_collector/geoip_collector.py", line 54, in request_data
    raise error_city
  File "/path/to/ipsurv/data_collector/geoip_collector.py", line 69, in _request_city
    res = self.requester.request_city(ip)
  File "/path/to/ipsurv/requester/geoip.py", line 140, in request_city
    self.reader_city = self._create_reader(self.TYPE_CITY)
  File "/path/to/ipsurv/requester/geoip.py", line 94, in _create_reader
    raise Exception("GeoIp data file none.({})".format(gtype))        # [CHECK-6] --------------------------------- Error reason1
Exception: GeoIp data file none.(city)                                   # [CHECK-7] --------------------------------- Error reason2
2024-12-09 07:47:42,623 - DEBUG - GEOIP_DATA:
{'error': 'GeoIp data file none.(city)'}
```

- **Error example2**

The following example shows a failure to load ```IPSURV_CONF```.

```
Enable verbose mode. Current:3 [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
2024-12-09 22:59:20,064 - DEBUG - Env parse error.(IPSURV_CONF)                        # Error
Traceback (most recent call last):
  File "/path/to/ipsurv/util/args_util.py", line 109, in load_env
    tv = json.loads(v)
  File "/usr/local/lib/python3.7/json/__init__.py", line 348, in loads
    return _default_decoder.decode(s)
  File "/usr/local/lib/python3.7/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "/usr/local/lib/python3.7/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 1 column 85 (char 84)
2024-12-09 22:59:20,065 - INFO - Fail to load env.(IPSURV_CONF)
```

The JSON format of ```IPSURV_CONF``` may be error. JSON format checks using tools like [jsonlint](https://prantlf.github.io/jsonlint/) and others are recommended.
