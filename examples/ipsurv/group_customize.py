from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData
from ipsurv.core.entity import Target, TargetGroup

from ipsurv.ip_surv_cmd import IpSurvCmd

import re

'''
Group customize.

Specification:
- Customizing Pipeline class.

Command:
# cat examples.txt|python3 group_customize.py

Result e.g.:
python3 group_customize.py 192.168.1.1 192.168.1.2 192.169.1.1 --group=1 --skip_duplicate=1
'''


class GroupCustomizePipeline(Pipeline):
    def get_group_identify(self, data, target):
        # type: (ValueData, Target) -> int
        if re.search(r'^192\.16[89]', target.identifier):
            return 1

        return target.identifier_int

    def create_group(self, data, target, group_type, cidr):
        # type: (ValueData, Target, str, str) -> TargetGroup

        group = None

        if re.search(r'^192\.16[89]', target.identifier):
            group = TargetGroup(1, value=1)

        return group


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return GroupCustomizePipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
