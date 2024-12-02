import pytest

from ipsurv.core.entity import Target, ValueData
from ipsurv.core.target_parser import TargetParser
from ipsurv.core.pipeline import Pipeline
from ipsurv.requester.dns_resolver import DnsResolveRequester
from unittest.mock import MagicMock
from ipsurv.util.network_util import IpUtil


class TestTargetParser:
    @pytest.fixture(autouse=True)
    def setup(self, args, dns_resolver):
        pipeline = Pipeline()

        self.target_parser = TargetParser(args, pipeline, dns_resolver)

    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.fixed_format_params = []
        args.fixed_timeout = {'dns': 0, 'http': 0, 'reactivity': 0}
        args.fixed_delimiter = ','
        args.fixed_collectors = []
        args.fixed_ranges = []
        args.autodetect = False

        return args

    @pytest.fixture
    def dns_resolver(self, mocker):
        dns_resolver = mocker.Mock(spec=DnsResolveRequester)

        dns_resolver.resolve_ip = MagicMock(return_value='192.168.1.200')

        return dns_resolver

    def test_parse(self, args):
        data = ValueData({})

        self.target_parser.parse(data, 'a,192.168.1.100,b', args)

        assert data.get('identifier') == '192.168.1.100'
        assert data.get('identifier_int') == 3232235876

        target = self.target_parser.parse(data, 'a,x,b', args)

        assert target.identifier == 'ILLEGAL_FORMAT'

    def test_parse_target(self, args):
        data = ValueData({})

        target = self.target_parser._parse_target(data, '192.168.1.100', args)

        assert target.raw == '192.168.1.100'

        self.target_parser.autodetect = True
        target = self.target_parser._parse_target(data, '192.168.1.100', args)

        assert target.raw == '192.168.1.100'

    def test_identify_target(self, args):
        data = ValueData({})

        target = Target('192.168.1.100')

        self.target_parser._identify_target(data, target, args)

        assert data.get('ip') == '192.168.1.100'
        assert data.get('ip_int') == 3232235876

        target = Target('')

        self.target_parser._identify_target(data, target, args)

        assert target.status == 'EMPTY'

    def test_identify_target_ip(self, args):
        data = ValueData({})

        target = Target('192.168.1.100')

        identified = self.target_parser._identify_target_ip(data, target, args)

        assert identified is True

        target = Target('http://www.wikipedia.org/')

        identified = self.target_parser._identify_target_ip(data, target, args)

        assert identified is True

        target = Target('192.168.1.10 - - [10/Nov/2024:03:15:42 +0900] "GET / HTTP/1.1" 304 - "http://xyz-sample-dummy-test.org" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"')

        identified = self.target_parser._identify_target_ip(data, target, args)

        assert identified is True
        assert target.ip == '192.168.1.10'

    def test_assign_data_target(self):
        data = ValueData({})

        target = Target()
        target.identifier = '192.168.1.100'
        target.identifier_int = 3232235876

        self.target_parser._assign_data_target(data, target)

        assert data.get('identifier') == '192.168.1.100'
        assert data.get('identifier_int') == 3232235876

    def test_detect_target_raw(self):
        target = Target()
        target.identifier = 'test'
        target.identifier_int = 2730633496

        data = ValueData({})

        self.target_parser._assign_data_target(data, target)

        assert data.get('identifier') == 'test'
        assert data.get('identifier_int') == 2730633496
        assert type(data.get('target')) == Target

    def test_split_port(self):
        v1, v2 = self.target_parser._split_port('ipsurv-domain-test-example.xyz:80')

        assert v1 == 'ipsurv-domain-test-example.xyz' and v2 == 80

        v1, v2 = self.target_parser._split_port('192.168.1.100:80')

        assert v1 == '192.168.1.100' and v2 == 80

        v1, v2 = self.target_parser._split_port('192.168.1.100')

        assert v1 == '192.168.1.100' and v2 is None

    def test_evaluate_ip_type(self):
        data = ValueData({})

        ip_address = IpUtil.get_ip_address('192.168.1.100')

        self.target_parser._evaluate_ip_type(data, ip_address)

        assert data.get('ip_type') == 1

        ip_address = IpUtil.get_ip_address('8.8.8.8')

        self.target_parser._evaluate_ip_type(data, ip_address)

        assert data.get('ip_type') == 2

    def test_evaluate_in_ranges(self):
        data = ValueData({})

        ip_address = IpUtil.get_ip_address('192.168.1.100')
        self.target_parser.ranges = ['192.168.1.1/24']

        self.target_parser._evaluate_in_ranges(data, ip_address)

        assert data.get('in_range') is True

    def test_find_url(self):
        assert self.target_parser._find_url('http://ipsurv-domain-test-example.xyz') is not None
        assert self.target_parser._find_url('https://ipsurv-domain-test-example.xyz') is not None
        assert self.target_parser._find_url('//ipsurv-domain-test-example.xyz') is not None

    def test_find_fqdn(self):
        assert self.target_parser._find_fqdn('ipsurv-domain-test-example.xyz') is not None
        assert self.target_parser._find_fqdn('test.psurv-domain-test-example.xyz') is not None

    def test_find_ip(self):
        assert self.target_parser._find_ip('192.168.1.1') is not None

    def test_create_target(self):
        assert type(self.target_parser._create_target('')) == Target
