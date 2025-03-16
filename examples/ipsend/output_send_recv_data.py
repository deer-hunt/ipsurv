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
    def pre_send(self, binary):
        print(binary)

        return binary

    def post_receive(self, binary):
        print(binary)

        return binary


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    cmd = IpSendCmd(factory)

    cmd.run()
