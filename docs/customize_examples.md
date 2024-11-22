# [IpSurv] Customizing and Examples

## Overview

"ipsurv" is implemented with customizable program architecture. It provide extending features and several classes.

## Program Architecture and Classes

See `program_architecture_classes.md`.

## Example programs

There are several example programs of how to customize. Please refer to the comments in each program for more details..

**Path:** ``./examples/``

| Program                  | Description                                      |
|-------------------------------|--------------------------------------------------|
| add_original_option.py        | Adding original options to the configuration.     |
| check_favicon.py        | Checking "/favicon.ico".            |
| check_cloud_service.py        | Checking the status of cloud services.            |
| check_wordpress_site.py       | Checking WordPress site and WordPress theme. |
| config_customize.py | Customizing Config class.         |
| force_json.py                 | Forces data to be output in JSON format.        |
| group_customize.py            | Customizing group settings.         |
| inject_original_class.py            | Injecting original class object.         |
| object_factory_original_headers.py      | Injecting original classes.   |
| pipeline_customize.py          | Customizing by pipeline class.         |
| show_original_headers.py      | Displaying the original headers.              |
| simple_totalize.py            | Simple totalization by the given data.     |
| target_parser_customize.py            | Customizing TargetParser.     |
| use_requester_directly.py            | Using requester class directly.     |
| extract_regex_data.py              | Extracting text by regex, and generate CRC and MD5 values.   |


## Execution examples

**Program:** object_factory_original_headers.py

```bash
$ python object_factory_original_headers.py

 __  .______     _______. __    __  .______     ____    ____ 
|  | |   _  \   /       ||  |  |  | |   _  \    \   \  /   / 
|  | |  |_)  | |   (----`|  |  |  | |  |_)  |    \   \/   /  
|  | |   ___/   \   \    |  |  |  | |      /      \      /   
|  | |  |   .----)   |   |  `--'  | |  |\  \----.  \    /    
|__| | _|   |_______/     \______/  | _| `._____|   \__/     


No target data.

Complete!
```


**Program:** extract_regex_data.py

```bash
$ python extract_regex_data.py "#123456#" "#abcdef#" "#XYZ#" --headers=1

original,my_text,crc,md5
#123456#,123456,158520161,e10adc3949ba59abbe56e057f20f883e
#abcdef#,abcdef,1267612143,e80b5017098950fc58aad83c8c14978e
#XYZ#,XYZ,2099902701,e65075d550f9b5bf9992fa1d71a131be
```
