from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData

from ipsurv.ip_surv_cmd import IpSurvCmd

import re

'''
Pipeline customize.

Specification:
- Customizing Pipeline class.
- Creating ObjectFactory class.

Command:
# cat examples.txt|python3 pipeline_customize.py
'''


class MyPipeline(Pipeline):
    def pre_configure(self, args, env_args, env_conf):
        args.sequence = True

    def post_collect(self, data, target, args, skip):
        data.update('sequence', lambda v: 'A' + str(v))

        self.serializer.set_status(data, target, args, skip)


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
