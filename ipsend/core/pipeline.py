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

    def complete(self):
        pass
