from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData

from ipsurv.ip_surv_cmd import IpSurvCmd

import re

'''
Injecting original class.

Specification:
- Customizing Pipeline class object.

Command:
# cat examples.txt|python3 inject_original_class.py
'''


# Original class
class ClassObject():
    def show(self):
        print('This is EntityObject')


class InjectionObject():
    def show(self):
        print('This is InjectionObject')


class MyPipeline(Pipeline):
    def __init__(self, injection_object):
        super().__init__()

        self.class_object = ClassObject()
        self.injection_object = injection_object

    def complete_process(self, mode, args, rows):
        print('')
        print('Test:')

        self.class_object.show()
        self.injection_object.show()


class MyObjectFactory(ObjectFactory):
    def __init__(self, injection_object):
        self.injection_object = injection_object

    def create_pipeline(self):
        return MyPipeline(self.injection_object)


if __name__ == '__main__':
    injection_object = InjectionObject()

    factory = MyObjectFactory(injection_object)

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
