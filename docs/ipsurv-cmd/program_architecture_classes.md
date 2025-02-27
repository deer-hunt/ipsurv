# Program architecture and Classes

## Modules and Classes and Methods docs.

The following are the documentation for Modules, Classes, and Methods.

- [Module Index](https://deer-hunt.github.io/ipsurv/py-modindex.html)
- [Classes and Methods docs](https://deer-hunt.github.io/ipsurv/genindex.html)


## Process flow

The following is overview of process flow. You would be better off checking the python code, because the process is simple and easy.


#### [Initializing]

**1. Process start.**

**2. Creating basic class objects:** `ObjectFactory`

**3. Parsing command arguments and reading from STDIN.**

**4. Detecting mode:** `Survey-mode`

> The following is description of "Survey IPs" mode.

**5. Creating each class objects:** `ObjectFactory`

#### [Process in each input row]

> The data is passed by `ValueData` object in each processes.

**6. Parsing the target:** `TargetParser`, `Target`

**7. Finding the group:** `TargetGroup`

**8. Collecting the source data:** `DataCollector`, `Requester`

**9. Outputting the result:** `Serializer`

#### [Back to primary flow]

**10. Process complete.**


## Survey-mode

"ipsurv" have two Survey-mode. Those are "Survey IPs" and "Survey Self". 

| Survey-mode              | Filename        | Class      |
|-------------------|------------------|-----------------|
| Survey IPs     | survey_ips.py    | `SurveyIps`     |
| Survey Self    | survey_self.py   | `SurveySelf`    |


## Configure and Constant

The following is description of Configure and Constant.

| Class            | Filename           | Description       |
|------------------|-------------------|-------------------|
| `ArgsBuilder`    | ./configure/args_builder.py    | Building args object.         |
| Validator classes | ./configure/args_validators.py | Arguments specifying complex conditions.      |
| [`Config`](https://deer-hunt.github.io/ipsurv/modules/ipsurv.config.html)         | config.py         | Configure class. There are various configure variables. Example: config_customize.py     |
| `Constant`       | config.py         | Constant class.     |


## ObjectFactory

`ObjectFactory` class provide customizing classes and creating original classes. Important classes are generated in `ObjectFactory`.
If you'd like to create original factory class , extending `ObjectFactory`. And injecting to `IpSurvCmd` class.

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [ObjectFactory](https://deer-hunt.github.io/ipsurv/modules/ipsurv.core.object_factory.html)   |
| **Path**     | ./core/object_factory.py   |
| **Example**  | object_factory_original_headers.py   |


## ValueData

`ValueData` class is the role of storing data. It's used by various process. `ValueData` object is created by `ValueDataFactory`.
You are able to customize `ValueData` class by `ValueDataFactory` class.

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [ValueData](https://deer-hunt.github.io/ipsurv/modules/ipsurv.core.entity.html), ValueDataFactory   |
| **Path**     | ./core/entity.py        |


## Target

`Target` class is the role of target data for surveying. It includes "IP", "URL", "FQDN", "port" or any other source data.
`Target` object is created by `TargetParser` class. And `Target` object is stored as "target" in `ValueData` object, outputting with the name "target.*" in serializing.

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [Target](https://deer-hunt.github.io/ipsurv/modules/ipsurv.core.entity.html)   |
| **Path**     | ./core/entity.py        |
| **Example**    | target_parser_customize.py                  |


## TargetParser

`TargetParser` class is the role of parsing input row and creating `Target` object. You are able to customize parsing process, and store original source data.

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [TargetParser](http://deer-hunt.github.io/ipsurv/modules/ipsurv.core.misc.html)   |
| **Path**     | ./core/target_parser.py        |
| **Example**    | target_parser_customize.py                  |


## Pipeline

`Pipeline` class provide catching and customizing the data in each processing. `Pipeline` class allows for modifying process behaviors or adding specifications without a lot of class extensions or changing the structure.
It's available to very fine data control.


| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [Pipeline](http://deer-hunt.github.io/ipsurv/modules/ipsurv.core.pipeline.html)   |
| **Path**     | ./core/pipeline.py      |
| **Example**    | pipeline_customize.py                  |

**Pipeline's methods**

When Pipeline's methods are dispatched:

| Methods                  | When it dispatch                                            | Processing e.g.                   |
|---------------------------|--------------------------------------------------------|------------------------|
| `init_configure`            | Initializing arguments values.                         | Customizing arguments and env.                            |
| `pre_configure`             | Before configuring arguments.                          | Customizing arguments before configuring.         |
| `post_configure`            | After configuring arguments.                           | Customizing arguments after configuring.            |
| `detect_survey_mode`     | Detecting Survey-mode.                                | Changing Survey-mode.                               |
| `begin_process`             | Before beginning processes.                            | Initializing.                              |
| `pre_target_parse`          | Before parsing the target.                            | Check or Modify row data before parsing.               |
| `pre_target_identify`       | Before identifying the target.                         | Customizing parsed data.                               |
| `pre_output_headers`      | Before outputting headers.                  | Customizing headers.                                        |
| `pre_collect`                | Before collecting for each row.                       |                               |
| `find_group`                | When finding the group.                                  | Customizing grouping.                              |
| `get_group_identify`        | When identifying the group.                            | Customizing grouping.                               |
| `create_group`              | After identifying the group and creating the group.   | Customizing grouping.                              |
| `pre_request`               | Before collecting each data collection.                |                               |
| `post_request`              | After collecting each data collection.                 | Customizing response data.                              |
| `post_collect`               | After collecting for each row.                        | Customizing collected data.                              |
| `build`                     | Building the output data and transforming data.           | Customizing output data.                              |
| `build_error`               | When a system error occurs and building error data.   |                               |
| `output_result`             | When outputting result in each process.              | Customizing outputting result.                              |
| `output_result_self`        | In self-mode, when outputting the result.             |                               |
| `complete_process`          | After completing processes.                            | Final processing.                              |


## DataCollector

`DataCollector` class provide call `Requester` class and collect response data. Approximately, `DataCollector` class can be considered a wrapper class for `Request` class.

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [DataCollector](http://deer-hunt.github.io/ipsurv/modules/ipsurv.data_collector.basic.html)   |
| **Path**     | ./data_collector/data_collector.py, Classes in the same hierarchy.      |
| **Example**    | check_wordpress_site.py                  |


## Requester

`Requester` class provide requesting outer data. 

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [Requester](http://deer-hunt.github.io/ipsurv/modules/ipsurv.requester.html)    |
| **Path**     | ./requester/requester.py, Classes in the same hierarchy.      |
| **Example**    | check_favicon.py, use_requester_directly.py                  |


## Serializer

`Serializer` class provide displaying data and transforming data for presentation. `LineSerializer` class provide feature of line output. `JsonSerializer` class provide JSON output. Also, you are able to create original Serializer.

| Attribute    | Value             |
|----------------------|--------------------------------------------------|
| **Class**     | [Serializer](http://deer-hunt.github.io/ipsurv/modules/ipsurv.serializer.html), LineSerializer, JsonSerializer   |
| **Path**     | ./serializer/serializer.py, line_serializer.py, json_serializer.py |
| **Example**    | object_factory_original_headers.py                  |

**Serializer's methods**

Serializer's methods:

| Methods                  | Description                                               |
|------------------------------|-----------------------------------------------------------|
| `set_survey_mode`            | Set the survey mode.                                     |
| `set_delimiter`              | Set the delimiter (separator character).                 |
| `output_begin`   | Output in beginning the process.                                 |
| `create_labels`              | Create labels.                                         |
| `get_label`                  | Get a specified label.                              |
| `set_status`                 | Set the status of the process.                           |
| `build`                      | Build the data structure.                            |
| `transform`                  | Transforms the data.                                      |
| `filter_value`               | Filters value.                                           |
| `build_row`                  | Build a row.                                        |
| `build_error`                | Build error.                             |
| `output_result`              | Output the result.                                      |
| `output`                     | Output the value.                               |
| `output_complete`   | Output in completing the process.                                   |
| `transform_key_labels`       | Transforms key labels.                                   |
| `output_message`             | Outputs a message.                                      |
| `output_item`                | Output an item.                                         |


## Utils

In `./util`, there are some util classes. Those are used in various places.

| Path                      | Classes                     |
|----------------------|--------------------------------------------------|
| ./util/args_util.py      | `ArgValidator`, `StdinLoader` |
| ./util/network_util.py    | `DnsUtil`        |
| ./util/sys_util.py       | `AppException`, `System`    |


## Internal specifications / Misc

### About "RDAP" Data

- RDAP data is JSON data by RDAP structure. However, the data like country code is not perfect. There is not country code rarely. In such cases, the country code is analyzed from the address.
- In rare cases, the RDAP server's data may be incorrect.

### About "DNSTXT" Data

- "DNSTXT" data is collected from TXT-record of "origin.asn.cymru.com".

### About "IPINFO" Data

- "IPINFO" data is collected from "ipinfo.io".
