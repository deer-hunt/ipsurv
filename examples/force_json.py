from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData

from ipsurv.ip_surv_cmd import IpSurvCmd

'''
Force json.

Specification:
- Customizing Pipeline class.

Command:
# cat examples.txt|python3 force_json.py
'''


class MyPipeline(Pipeline):
    def pre_configure(self, args, env_args, env_conf):
        args.json = 2


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
