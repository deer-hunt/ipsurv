from ipsend.core.object_factory import ObjectFactory
from ipsend.core.pipeline import Pipeline
from ipsend.ipsend_cmd import IpSendCmd
import pprint
import re

'''
Command:
# python3 output_send_recv_data.py --dest=wikipedia.org --http -I
'''


class MyPipeline(Pipeline):
    def pre_send(self, byte_data):
        print(byte_data)

        return byte_data

    def post_receive(self, byte_data):
        print(byte_data)

        return byte_data


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    cmd = IpSendCmd(factory)

    cmd.run()
