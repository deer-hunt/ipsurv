from ipscap.core.object_factory import ObjectFactory
from ipscap.core.pipeline import Pipeline
from ipscap.ipscap_cmd import IpsCapCmd

import re

'''
Injecting original class.

Specification:
- Customizing Pipeline class object.

Command:
# python3 inject_original_class.py --exclude_ssh
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

    def initialize(self, config):
        print('This is original message. Initialized.\n')

    def complete(self, transfers):
        print('')
        print('This is original message. Complete.\n')

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

    cmd = IpsCapCmd(factory)

    cmd.run()
