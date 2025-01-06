import os

from ipscap.util.raw_socket_entity import IPHeader
import logging


class DumpFile:
    def __init__(self):
        self.dirname = None

    def initialize(self, dirname):
        self.dirname = dirname

        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def write(self, ip_header, protocol_header, append_header):
        filename = self.get_filename(ip_header, protocol_header)
        path = self.dirname + '/' + filename

        logging.log(logging.INFO, 'DUMPFILE_PATH: ' + path)

        with open(path, 'ab') as file:
            if append_header:
                file.write(ip_header.header_data)
                file.write(protocol_header.header_data)

            file.write(protocol_header.payload_data)

        return path

    def get_filename(self, ip_header, protocol_header, ext='.dat'):
        protocol_code = IPHeader.get_protocol_code(ip_header.protocol).lower()

        if ip_header.direction == IPHeader.DIRECTION_SEND:
            port = protocol_header.src_port
            filename = protocol_code + '_' + ip_header.src_ip + '_' + str(protocol_header.src_port) + '_' + ip_header.dest_ip + '_' + str(protocol_header.dest_port)
        else:
            port = protocol_header.dest_port
            filename = protocol_code + '_' + ip_header.dest_ip + '_' + str(protocol_header.dest_port) + '_' + ip_header.src_ip + '_' + str(protocol_header.src_port)

        if port < 32768 and port != -1:
            filename = 'server_' + filename

        filename += '_' + ip_header.direction_code.lower() + ext

        return filename

    def get_path(self):
        full_path = os.path.abspath(self.dirname)

        return full_path.rstrip('/') + '/'

    def get_file_num(self):
        full_path = self.get_path()

        files = next(os.walk(full_path))[2]

        return len(files)
