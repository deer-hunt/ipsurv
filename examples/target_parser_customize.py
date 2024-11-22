from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData, Target

from ipsurv.core.target_parser import TargetParser
from ipsurv.util.network_util import IpUtil

from ipsurv.ip_surv_cmd import IpSurvCmd

import json

'''
TargetParser customize.

Specification:
- Customizing Target class.
- Customizing TargetParser class.

Command:
# python3 target_parser_customize.py '{"ip":"8.8.8.8","hostname":"hostname.com","port":80,"sample1":1,"sample2":2,"sample3":"ABC"}' --format="{target.ip},{target.port},{target.sample1},{target.sample2},{target.sample3}"
'''


class JsonTarget(Target):
    def __init__(self, raw=None):
        super().__init__(raw)

        self.sample1 = None
        self.sample2 = None
        self.sample3 = None


class JSONTargetParser(TargetParser):
    def _create_target(self, raw):
        return JsonTarget(raw)

    def _identify_target_ip(self, data, target, args):
        # type: (ValueData, Target, object) -> bool

        data = json.loads(target.raw)

        target.ip = data['ip']
        target.identifier = target.ip
        target.identifier_int = IpUtil.get_ip_int(target.identifier)

        target.fqdn = data['hostname']
        target.port = data['port']
        target.sample1 = data['sample1']
        target.sample2 = data['sample2']
        target.sample3 = data['sample3']

        # target.dump()

        return True


class MyObjectFactory(ObjectFactory):
    def create_target_parser(self, args, pipeline, dns_resolver):
        return JSONTargetParser(args, pipeline, dns_resolver)


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
