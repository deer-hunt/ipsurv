from abc import ABC

from ipsurv.configs import Config, Constant
from ipsurv.core.entity import Target, TargetGroup, ValueData
from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.serializer.serializer import Serializer


class Pipeline(ABC):
    def __init__(self):
        self.config = None  # type: Config
        self.serializer = None  # type: Serializer

    def initialize(self, config, serializer):
        self.config = config
        self.serializer = serializer

    def init_configure(self, arguments, env_args):
        # type: (dict, dict) -> None
        pass

    def pre_configure(self, args, env_args, env_conf):
        # type: (object, dict, dict) -> None
        pass

    def post_configure(self, args, env_args, env_conf):
        # type: (object, dict, dict) -> None
        pass

    def detect_survey_mode(self, mode):
        self.serializer.set_survey_mode(mode)

        return mode

    def begin_process(self, mode, args, rows):
        self.serializer.output_begin(mode, args, rows)

    def pre_target_parse(self, data, original):
        # type: (ValueData, str) -> str
        return original

    def pre_target_identify(self, data, target):
        # type: (ValueData, Target) -> bool

        return True

    def pre_output_headers(self, data):
        # type: (ValueData) -> None

        pass

    def pre_collect(self, data, target, args):
        # type: (ValueData, Target, object) -> None
        pass

    def find_group(self, data, target):
        # type: (ValueData, Target) -> TargetGroup

        return None

    def get_group_identify(self, data, target):
        # type: (ValueData, Target) -> int
        return target.identifier_int

    def create_group(self, data, target, group_type, cidr):
        # type: (ValueData, Target, str, str) -> TargetGroup

        return None

    def pre_request(self, data, name, collector):
        # type: (ValueData, str, DataCollector) -> None
        pass

    def post_request(self, data, name, collector, success, response):
        # type: (ValueData, str, DataCollector, bool, dict) -> None
        pass

    def post_collect(self, data, target, args, skip):
        # type: (ValueData, Target, object, bool) -> None
        self.serializer.set_status(data, target, args, skip)

    def build(self, data, target):
        # type: (ValueData, Target) -> object

        return self.serializer.build(data, target)

    def build_error(self, error):
        return self.serializer.build_error(error)

    def output_result(self, v):
        self.serializer.output_result(v)

    def output_result_self(self, data):
        self.serializer.transform_key_labels(data, Constant.STR_PASCAL)

        self.serializer.output_item(data)

    def complete_process(self, mode, args, rows):
        self.serializer.output_complete(mode, args, rows)
