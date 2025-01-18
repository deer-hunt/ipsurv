from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline

from ipsurv.ip_surv_cmd import IpSurvCmd

import re

'''
Simple totalize.

Specification:
- Customizing Pipeline class.

Command:
# cat examples.txt|python3 simple_totalize.py
'''


class MyPipeline(Pipeline):
    def __init__(self):
        super().__init__()
        self._total = 0
        self._success = 0

    def pre_collect(self, data, target, args):
        self._total += 1

    def post_collect(self, data, target, args, skip):
        if data.get('success'):
            self._success += 1

    def complete_process(self, mode, args, rows):
        self.serializer.output('Total:' + str(self._total))
        self.serializer.output('Success:' + str(self._success))


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
