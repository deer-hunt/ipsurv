from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.target_parser import TargetParser
from ipsurv.core.entity import ValueData, Target
from ipsurv.core.pipeline import Pipeline
import binascii
import hashlib
import re

from ipsurv.ip_surv_cmd import IpSurvCmd

'''
Extracting text by regex, and generate CRC and MD5 values.

Specification:
- Customizing DataCollector class.
- Customizing TargetParser class.

Command:
# cat examples.txt|python3 extract_regex_data.py
# python3 extract_regex_data.py "#123456#" "#abcdef#" "#XYZ#" --headers=1
'''


class MyTargetParser(TargetParser):
    def _identify_target_ip(self, data, target, args):
        # type: (ValueData, Target, object) -> bool

        m = re.search(r'#([^#]*)#', target.raw)

        if m:
            target.my_text = m.group(1)
        else:
            target.my_text = ''

        return True


class RegexDataCollector(DataCollector):
    def __init__(self, requester, args):
        super().__init__(requester, args)

    def get_name(self):
        return 'REGEX_DATA'

    def request_data(self, target):
        return (True, {})

    def get_requires(self):
        return ['crc', 'md5']

    def build_data(self, target, data, success, response, response_time):
        v = target.my_text

        crc = binascii.crc32(v.encode()) & 0xffffffff
        data.set('crc', crc)

        md5_hash = hashlib.md5(v.encode())
        md5 = md5_hash.hexdigest()
        data.set('md5', md5)


class MyPipeline(Pipeline):
    def pre_configure(self, args, env_args, env_conf):
        args.format = '{target.my_text},{crc},{md5}'

    def post_configure(self, args, env_args, env_conf):
        args.fixed_collectors = ['regex_data']

    def begin_process(self, mode, args, rows):
        super().begin_process(mode, args, rows)

        message = 'CRC and MD5 of #char#'

        print('\033[32m' + message + '\033[0m')


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()

    def create_target_parser(self, args, pipeline, dns_resolver):
        return MyTargetParser(args, pipeline, dns_resolver)

    def create_collectors(self, args, dns_resolver):
        collectors = {}

        collectors['regex_data'] = RegexDataCollector(None, args)

        return collectors


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
