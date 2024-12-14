from abc import ABC

from ipsurv.configs import Config, Constant
from ipsurv.core.entity import Target, TargetGroup, ValueData
from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.serializer.serializer import Serializer


class Pipeline(ABC):
    """
    Description:
    https://deer-hunt.github.io/ipsurv/pages/program_architecture_classes.html#pipeline
    """
    def __init__(self):
        self.config = None  # type: Config
        self.serializer = None  # type: Serializer

    def initialize(self, config, serializer):
        """
        :param config:
        :type config: Config
        :param serializer:
        :type serializer: Serializer
        """

        self.config = config
        self.serializer = serializer

    def init_configure(self, arguments, env_args):
        """
        :param arguments:
        :type arguments: dict
        :param env_args:
        :type env_args: dict
        """
        pass

    def pre_configure(self, args, env_args, env_conf):
        """
        :param args:
        :type args: argparse.Namespace
        :param env_args:
        :type env_args: dict
        :param env_conf:
        :type env_conf: dict
        """
        pass

    def post_configure(self, args, env_args, env_conf):
        """
        :param args:
        :type args: argparse.Namespace
        :param env_args:
        :type env_args: dict
        :param env_conf:
        :type env_conf: dict
        """
        pass

    def detect_survey_mode(self, mode):
        """
        :param mode:
        :type mode: int
        """
        self.serializer.set_survey_mode(mode)

        return mode

    def begin_process(self, mode, args, rows):
        """
        :param mode:
        :type mode: int
        :param args:
        :type args: argparse.Namespace
        :param rows:
        :type rows: list
        """

        self.serializer.output_begin(mode, args, rows)

    def pre_target_parse(self, data, original):
        """
        :param data:
        :type data: ValueData
        :param original:
        :type original: str
        """

        return original

    def pre_target_identify(self, data, target):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        """

        return True

    def pre_output_headers(self, data):
        """
        :param data:
        :type data: ValueData
        """

        pass

    def pre_collect(self, data, target, args):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :param args:
        :type args: argparse.Namespace
        """

        pass

    def find_group(self, data, target):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :rtype: TargetGroup
        """

        return None

    def get_group_identify(self, data, target):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :rtype: int
        """

        return target.identifier_int

    def create_group(self, data, target, group_type, cidr):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :param group_type:
        :type group_type: int
        :param cidr:
        :type cidr: str
        :rtype: TargetGroup
        """

        return None

    def pre_request(self, data, name, collector):
        """
        :param data:
        :type data: ValueData
        :param name:
        :type name: str
        :param collector:
        :type collector: DataCollector
        """

        pass

    def post_request(self, data, name, collector, success, response):
        """
        :param data:
        :type data: ValueData
        :param name:
        :type name: str
        :param collector:
        :type collector: DataCollector
        :param success:
        :type success: bool
        :param response:
        :type response: dict
        """

        pass

    def post_collect(self, data, target, args, skip):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :param args:
        :type args: argparse.Namespace
        :param skip:
        :type skip: bool
        """

        self.serializer.set_status(data, target, args, skip)

    def build(self, data, target):
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        """

        return self.serializer.build(data, target)

    def build_error(self, error):
        return self.serializer.build_error(error)

    def output_result(self, v):
        self.serializer.output_result(v)

    def output_result_self(self, data):
        """
        :param data:
        :type data: ValueData
        """

        self.serializer.transform_key_labels(data, Constant.STR_PASCAL)

        self.serializer.output_item(data)

    def complete_process(self, mode, args, rows):
        """
        :param mode:
        :type mode: int
        :param args:
        :type args: argparse.Namespace
        :param rows:
        :type rows: list
        """

        self.serializer.output_complete(mode, args, rows)
