from ipsurv.core.pipeline import Pipeline
from ipsurv.core.object_factory import ObjectFactory

from ipsurv.ip_surv_cmd import IpSurvCmd

'''
Adding original option. And Change option's default value.

Specification:
- Customizing Pipeline class.

Command:
# cat examples.txt|python3 add_original_option.py
'''


class MyPipeline(Pipeline):
    def init_configure(self, arguments, env):
        arguments['my_option'] = {'default': 0, 'type': int, 'help': 'My original option. '}
        arguments['timeout']['default'] = '1.0'
        arguments['sequence']['default'] = True

        env['headers'] = 2
        env['json'] = 2


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
