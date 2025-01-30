import os

import logging
from datetime import datetime


class DumpFile:
    def __init__(self, pipeline):
        self.dirname = None
        self.pipeline = pipeline

    def initialize(self, dirname):
        self.dirname = dirname

        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def write(self, dest, port, byte_data):
        filename = self.get_filename(dest, port)
        path = self.dirname + '/' + filename

        logging.log(logging.INFO, 'DUMPFILE_PATH: ' + path)

        with open(path, 'ab') as file:
            self.pipeline.pre_writefile(dest, port, byte_data, file)

            file.write(byte_data)

            self.pipeline.post_writefile(dest, port, byte_data, file)

        return path

    def get_filename(self, dest, port, ext='.dat'):
        now = datetime.now()

        datetm = now.strftime('%Y%m%d_%H%M_%S')

        filename = 'ipsend_' + datetm + '_' + dest + '_' + str(port) + ext

        filename = self.pipeline.get_filename(dest, port, filename)

        return filename

    def get_path(self):
        full_path = os.path.abspath(self.dirname)

        return full_path.rstrip('/') + '/'

    def get_file_num(self):
        full_path = self.get_path()

        files = next(os.walk(full_path))[2]

        return len(files)
