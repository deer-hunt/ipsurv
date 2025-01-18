# Command arguments

This document is description of ipscap's command arguments.

## Index

- [General and Debugging](#general-and-debugging)
- [Filtering](#filtering)
- [Output](#output)
- [Statistics](#statistics)
- [Miscellaneous](#miscellaneous)

## General and Debugging

### `--verbose`

Verbose mode. Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG.

- **Type:** `int`
- **Default:** `0`
- **Choices:**

| Value | Description                                 |
|-------|---------------------------------------------|
| 1     | TRACE_ERROR. Output error with trace.       |
| 2     | INFO. Output setting values and internal values. |
| 3     | DEBUG. Output maximum debug information.    |

- **Example:**

```
INPUT:
--verbose=1, --verbose=2, --verbose=3

RESULT:
Enable verbose mode. Current:3 [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]
```

### `--debug`

`--debug` is equivalent to `--verbose=3`.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --debug
```

### `--log`

Verbose log filename.

- **Type:** `str`
- **Default:** `None`

- **Example:**

```
INPUT: --log=verbose.log
```

## Filtering

### `--find`

Find character string by regex and ignoring case.

- **Type:** `str`
- **Default:** `''`

- **Example:**

```
INPUT: --find="HTTP"
```

### `--find_mode`

Find mode. REGEX, MATCH, BINARY, HEX.

- **Type:** `str`
- **Default:** `REGEX`

- **Choices:**

| Value  | Description |
|--------|-------------|
| REGEX  | Regular expression mode. |
| MATCH  | Match mode. |
| BINARY | Binary mode. |
| HEX    | Hex mode.   |

- **Example:**

```
INPUT: 
--find_mode=HEX
--find_mode=BINARY
```

### `--port`

Filter port. It is source port or destination port.

- **Type:** `str`
- **Default:** `''`

- **Example:**

```
INPUT: 
--port=80
--port=80,443
```

### `--protocol`

Filter Protocol. Default: "TCP,UDP".

- **Type:** `str`
- **Default:** `TCP,UDP`

- **Example:**

```
INPUT: 
--protocol=TCP
--protocol=TCP,ICMP
```

### `--ip`

Filter IP.

- **Type:** `str`
- **Default:** `''`

- **Example:**

```
INPUT:
--ip=192.168.1.10
--ip=192.168.1.101,192.168.1.102
```

### `--condition`

Filter by detail condition.

**Condition Rules**

| Key         | Type | Description                                       |
|-------------|------|---------------------------------------------------|
| port        | int  | Port number. Source or Destination.               |
| client_port | int  | Client port number.                               |
| src_port    | int  | Source port number.                               |
| dest_port   | int  | Destination port number.                          |
| ttl         | int  | TTL.                                              |
| flags       | str  | TCP flags. Uppercase, list of flags, single flag. |
| seq         | int  | Sequence number.                                  |
| ack         | int  | Acknowledgement number.                           |
| window      | int  | Window size.                                      |
| mss         | int  | mss.                                              |
| wscale      | int  | wscale.                                           |
| sack        | int  | sack.                                             |

- **Type:** `str`
- **Default:** `''`

- **Example:**

```
INPUT:
--condition="src_port=80;dest_port<=30000;ttl=64;flags=SYN,PSH"
```

```
# ipscap --condition="port!=22"
# ipscap --condition="port>=25; port <=3306"
# ipscap --condition="src_port=80;dest_port<=30000;ttl=64"
# ipscap --condition="flags=SYN,PSH"
# ipscap --condition="wscale>1"
```

### `--tracking`

Tracking transfers that have been matched by filters.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --tracking
```

## Output

### `--output`

Output mode about header and data. NONE, HEADER, TEXT, BINARY, BINARY_ALL, HEX, HEX_ALL, LINE.

- **Type:** `str`
- **Default:** `TEXT`

- **Choices:**

| Value       | Description |
|-------------|-------------|
| NONE        | None        |
| HEADER      | Header only |
| TEXT        | Text data   |
| BINARY      | Binary data |
| BINARY_ALL  | Binary headers and data |
| HEX         | Hex data    |
| HEX_ALL     | Hex headers and data |
| LINE        | Single line |

- **Example:**

```
INPUT:
--output=HEX
--output=BINARY
--output=BINARY_ALL

--output=HEX
--output=HEX_ALL

--output=LINE
```

### `--dumpfile`

Dump data to files. Dir: `./dump_logs/`.

- **Type:** `int`
- **Default:** `0`

- **Choices:**

| Value | Description       |
|-------|-------------------|
| 0     | Off               |
| 1     | Dump data         |
| 2     | Dump headers and data |

- **Example:**

```
INPUT: --dumpfile=1
```

## Statistics

### `--stat_mode`

Statistics mode. 0: None, 1: Captured transfers, 2: All transfers.

- **Type:** `int`
- **Default:** `1`

- **Choices:**

| Value | Description             |
|-------|-------------------------|
| 0     | None                    |
| 1     | Captured transfers      |
| 2     | All transfers           |

- **Example:**

```
INPUT: --stat_mode=2
```

### `--stat_group`

Group the transfer in statistics. 0: None, 1: Grouping by IPs and service port, 2: Grouping by IPs.

- **Type:** `int`
- **Default:** `0`

- **Choices:**

| Value | Description                       |
|-------|-----------------------------------|
| 0     | None                              |
| 1     | Grouping by IPs and service port  |
| 2     | Grouping by IPs                   |

- **Example:**

```
INPUT: --stat_group=1
```

### `--timeout`

Stop automatically after the specified number of seconds.

- **Type:** `float`
- **Default:** `None`

- **Example:**

```
INPUT: --timeout=60.0
```


## Miscellaneous

### `--exclude_ssh`

`--exclude_ssh` is equivalent to `--condition="port!=22"`.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --exclude_ssh
```

### `--web_port`

`--web_port` is equivalent to `--port=80,443,53`.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --web_port
```

### `--general_port`

`--general_port` is equivalent to `--port=21,22,23,25,53,80,110,143,220,443,465,990,993,995,1433,3306`.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --general_port
```

### `--force`

Run force if any filter options aren't specified.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --force
```

### `--version`

Show version information.

- **Type:** `bool`
- **Default:** `False`

- **Example:**

```
INPUT: --version
```

