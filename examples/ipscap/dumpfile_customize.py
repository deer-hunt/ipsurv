from ipscap.core.object_factory import ObjectFactory
from ipscap.core.pipeline import Pipeline
from ipscap.ipscap_cmd import IpsCapCmd

import re

'''
Dumpfile customize.

Command:
# python3 dumpfile_customize.py --exclude_ssh
'''


class MyPipeline(Pipeline):
    def get_filename(self, ip_header, protocol_header, filename):
        filename = 'sample_' + filename

        return filename


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    cmd = IpsCapCmd(factory)

    cmd.run()
