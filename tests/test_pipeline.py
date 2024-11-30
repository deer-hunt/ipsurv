import pytest
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import Target, ValueData
from ipsurv.serializer.line_serializer import LineSerializer
from ipsurv.configs import Config
import re


class TestPipeline:
    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.fixed_format = '{ip}'
        args.fixed_format_params = ['ip']
        args.fixed_delimiter = ','
        args.alt_delimiter = ';'
        args.fixed_enclose = ''
        args.exhaustive = False

        return args

    @pytest.fixture(autouse=True)
    def target(self, args):
        target = Target()
        target.identifier_int = 123

        return target

    @pytest.fixture(autouse=True)
    def data(self):
        keys = Config.FORMAT_PARAMS
        data = ValueData(dict(zip(keys, keys)))

        return data

    @pytest.fixture(autouse=True)
    def test_setup(self, args):
        self.pipeline = Pipeline()

        self.pipeline.initialize(None, LineSerializer(args))

    def test_initialize(self):
        assert self.pipeline.initialize(None, None) is None

    def test_init_configure(self):
        assert self.pipeline.init_configure({}, {}) is None

    def test_pre_configure(self):
        assert self.pipeline.pre_configure({}, {}, {}) is None

    def test_post_configure(self):
        assert self.pipeline.post_configure({}, {}, {}) is None

    def test_detect_survey_mode(self):
        assert self.pipeline.detect_survey_mode(1) == 1

    def test_begin_process(self, args):
        assert self.pipeline.begin_process(1, args, []) is None

    def test_pre_target_parse(self):
        data = ValueData(None)
        assert self.pipeline.pre_target_parse(data, '123') == '123'

    def test_pre_target_identify(self):
        assert self.pipeline.pre_target_identify(None, None) is True

    def test_pre_output_headers(self):
        assert self.pipeline.pre_output_headers(None) is None

    def test_pre_collect(self, data, target, args):
        assert self.pipeline.pre_collect(data, target, args) is None

    def test_find_group(self):
        assert self.pipeline.find_group(None, None) is None

    def test_get_group_identify(self, target):
        assert self.pipeline.get_group_identify(None, target) == 123

    def test_create_group(self, data, target):
        assert self.pipeline.create_group(data, target, '8', '') is None

    def test_pre_request(self):
        assert self.pipeline.pre_request(None, None, None) is None

    def test_post_request(self):
        assert self.pipeline.post_request(None, None, None, None, None) is None

    def test_post_collect(self, data, target):
        assert self.pipeline.post_collect(data, target, None, False) is None

    def test_build(self, data, target):
        assert type(self.pipeline.build(data, target)) is str

    def test_build_error(self, capfd):
        v = self.pipeline.build_error('123')

        assert re.search(r'123', v)

    def test_output_result(self, capfd):
        self.pipeline.output_result('123')
        captured = capfd.readouterr()
        assert re.search(r'123', captured.out)

    def test_output_result_self(self):
        assert hasattr(self.pipeline, 'output_result_self')

    def test_complete_process(self, args, capfd):
        assert self.pipeline.complete_process(1, args, ['123']) is None
