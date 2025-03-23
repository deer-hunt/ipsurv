from abc import ABC

from ipsend.configs import Config, Constant


class Pipeline(ABC):
    """

    """

    def __init__(self):
        self.config = None  # type: Config

    def initialize(self, config):
        """
        :param config:
        :type config: Config
        """

        self.config = config

    def init_configure(self, arguments):
        """
        :param arguments:
        :type arguments: dict
        """
        pass

    def create_socket(self, socket):
        pass

    def connected(self, socket):
        pass

    def pre_send(self, binary):
        return binary

    def post_receive(self, binary):
        return binary

    def complete(self):
        pass

    def get_filename(self, dest, port, filename):
        return filename

    def pre_dump_write(self, dest, port, binary, file):
        pass

    def post_writefile(self, dest, port, binary, file):
        pass
