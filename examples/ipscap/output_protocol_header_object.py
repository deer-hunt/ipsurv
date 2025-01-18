from ipscap.core.object_factory import ObjectFactory
from ipscap.core.pipeline import Pipeline
from ipscap.ipscap_cmd import IpsCapCmd
import pprint
import re

'''
Output IP-header, TCP-header or UDP-header object.

Command:
# python3 output_protocol_header_object.py --exclude_ssh
'''


class MyPipeline(Pipeline):
    def process_captured_transfer(self, ip_header, protocol_header, passage_num):
        print('IPHeader:')
        pprint.pprint(vars(ip_header))
        print('\n')

        print('TCPHeader or UDPHeader:')
        pprint.pprint(vars(ip_header))
        print('\n')


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    cmd = IpsCapCmd(factory)

    cmd.run()
