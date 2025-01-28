from ipsend.core.object_factory import ObjectFactory
from ipsend.core.pipeline import Pipeline
from ipsend.ipsend_cmd import IpSendCmd

import re

'''
Pipeline customize.

Specification:
- Customizing Pipeline class.
- Creating ObjectFactory class.

Command:
# python3 pipeline_customize.py
'''


class MyPipeline(Pipeline):
    def process_captured_transfer(self, ip_header, protocol_header, passage_num):
        print('This is original message.\n')


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    cmd = IpSendCmd(factory)

    cmd.run()
