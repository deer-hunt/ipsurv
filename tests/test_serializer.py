import pytest
import re

from ipsurv.serializer.serializer import Serializer
from ipsurv.serializer.line_serializer import LineSerializer
from ipsurv.serializer.json_serializer import JsonSerializer
from ipsurv.core.entity import ValueData, Target


@pytest.fixture
def args(mocker):
    args = mocker.Mock()
    args.fixed_format = '{ip}'
    args.fixed_format_params = ['ip']
    args.fixed_delimiter = ','
    args.alt_delimiter = ';'
    args.fixed_enclose = ''
    args.exhaustive = False

    return args


class TempSerializerClass(Serializer):
    def build_row(self, data):
        # type: (ValueData) -> object
        return None

    def build_error(self, error):
        return None


class TestSerializer:
    @pytest.fixture(autouse=True)
    def setup(self, args):
        self.serializer = TempSerializerClass(args)

    def test_set_survey_mode(self):
        self.serializer.set_survey_mode(1)

        assert self.serializer.survey_mode == 1

    def test_set_delimiter(self):
        self.serializer.set_delimiter(',')
        assert self.serializer.delimiter == ','

    def test_output_begin(self, args):
        assert self.serializer.output_begin(1, args, []) is None

    def test_create_labels(self):
        values = self.serializer.create_labels({'a': 1}, 1)

        assert values['a'] is not None

    def test_get_label(self):
        assert self.serializer.get_label('a', 1) == 'a'
        assert self.serializer.get_label('abc', 2) == 'Abc'

    def test_set_status(self, args):
        data = ValueData({'requests': []})
        target = Target('')

        target.identifier = 'abc'
        self.serializer.set_status(data, target, args, False)
        assert data.get('group_status') == '-'

        target.status = 'EXIST'
        self.serializer.set_status(data, target, args, True)
        assert data.get('status') == 'SKIP'

        self.serializer.set_status(data, target, args, False)
        assert data.get('status') == '-'

        args.group = False

        self.serializer.set_status(data, target, args, False)
        assert data.get('group_status') == '-'

    def test_transform(self):
        data = ValueData({'ip_type': None})
        assert self.serializer.transform(data) is None

    def test_filter_value(self):
        assert self.serializer.filter_value(123) is not None

    def test_output(self, capfd):
        self.serializer.output('test')

        captured = capfd.readouterr()

        assert re.search(r'test', captured.out)

    def test_output_result(self, capfd):
        self.serializer.output_result('test')

        captured = capfd.readouterr()

        assert re.search(r'test', captured.out)

    def test_output_complete(self, args):
        assert self.serializer.output_complete(1, args, []) is None

    def test_misc(self):
        assert self.serializer.transform_key_labels(None, None) is None
        assert self.serializer.output_message(None) is None
        assert self.serializer.output_item(None) is None


class TestLineSerializer:
    @pytest.fixture(autouse=True)
    def setup(self, args):
        self.serializer = LineSerializer(args)

    def test_transform(self):
        assert hasattr(self.serializer, 'transform')

    def test_transform_status(self):
        data = ValueData({})
        data.header = False

        data.set('icmp', True)
        data.set('tcp', True)
        data.set('udp', True)
        data.set('http', True)
        data.set('http_h2', 1)

        self.serializer.transform_status(data)

        assert data.get('icmp') == 'ICMP_OK'
        assert data.get('tcp') == 'TCP_OK'
        assert data.get('udp') == 'UDP_OK'
        assert data.get('http') == 'HTTP_OK'
        assert data.get('http_h2') == 'HTTP2'

    def test_filter_value(self):
        assert self.serializer.filter_value('test') == 'test'
        assert self.serializer.filter_value(True) == 'OK'
        assert self.serializer.filter_value('test,test') == 'test;test'
        assert self.serializer.filter_value(None) == ''

        target = Target('')
        target.identifier = 'abc'
        assert self.serializer.filter_value(target) == target

    def test_get_bool_status(self):
        assert self.serializer._get_bool_status(True) == 'OK'
        assert self.serializer._get_bool_status(False) == 'NG'

    def test_build_row(self):
        data = ValueData({'ip': 'IP'})

        assert self.serializer.build_row(data) == 'IP'

        with pytest.raises(Exception):
            self.serializer.format = '{sampe..'
            self.serializer.build_row(data)

    def test_build_error(self):
        v = self.serializer.build_error('test')

        assert v == 'ERROR,test'

    def test_output(self, capfd):
        self.serializer.output('test')

        captured = capfd.readouterr()

        assert re.search(r'^test\s*$', captured.out)

    def test_transform_key_labels(self):
        data = ValueData({'ip': 'ip'})

        self.serializer.transform_key_labels(data, 3)

        assert data.get('IP') is not None

    def test_output_message(self, capfd):
        self.serializer.output_message('test')

        captured = capfd.readouterr()

        assert re.search(r'^test\s*$', captured.out)

    def test_output_item(self, capfd):
        data = ValueData({'a': 1, 'b': 2, 'c': 3})

        self.serializer.output_item(data)

        captured = capfd.readouterr()

        assert re.search(r'a,1', captured.out)


class TestJsonSerializer:
    @pytest.fixture(autouse=True)
    def setup(self, args):
        self.serializer = JsonSerializer(args)

    def test_output_begin(self, args, capfd):
        self.serializer.output_begin(1, args, [])

        captured = capfd.readouterr()
        self.serializer.json_list = True

        assert re.search(r'\[', captured.out)

    def test_transform(self):
        data = ValueData({'ip_type': None})

        assert self.serializer.transform(data) is None

    def test_filter_value(self):
        v = self.serializer.filter_value(5)

        assert v == 5

    def test_build_row(self):
        values = self.serializer.build_row(ValueData({'ip': 'IP', 'test': 1}))

        assert values == {'ip': 'IP'}

        self.serializer.exhaustive = False
        values = self.serializer.build_row(ValueData({'ip': 'IP', 'test': 1}))

        assert values == {'ip': 'IP'}

    def test_build_error(self):
        values = self.serializer.build_error('aaa')

        assert values['error'] == 'aaa'

    def test_output_complete(self, args, capfd):
        self.serializer.output_complete(1, args, [])

        captured = capfd.readouterr()
        self.serializer.json_list = True

        assert re.search(r'\]', captured.out)

    def test_output(self, capfd):
        self.serializer.output({'a': 1})

        captured = capfd.readouterr()

        assert re.search(r'"a":\s*1', captured.out)

        self.serializer.json_list = True
        self.serializer.output({'a': 1})

        captured = capfd.readouterr()

        assert re.search(r'"a":\s*1', captured.out)

    def test_output_message(self):
        assert self.serializer.output_message(None) is None

    def test_transform_key_labels(self):
        assert self.serializer.transform_key_labels(None, 1) is None

    def test_output_item(self, capfd):
        data = ValueData({'ip': 'IP'})

        self.serializer.output_item(data)
        captured = capfd.readouterr()

        assert re.search(r'ip', captured.out)
