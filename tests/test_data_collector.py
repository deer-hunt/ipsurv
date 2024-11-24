import pytest

from ipsurv.data_collector.pass_data_collector import PassDataCollector, PassRequester
from ipsurv.data_collector.basic_collectors import RdapCollector, DnsTxtCollector, IpInfoCollector, DnsReverseCollector
from ipsurv.data_collector.reactivity_collectors import ICMPCollector, TCPCollector, UDPCollector, HttpCollector
from ipsurv.data_collector.self_collector import SelfCollector
from ipsurv.requester.rdap import RdapRequester, CountryDetector
from ipsurv.requester.dns_resolver import DnsResolveRequester
from ipsurv.requester.ip_info import IpInfoRequester
from ipsurv.requester.server_reactivity import ServerReactivity
from ipsurv.requester.http import HttpRequester

from ipsurv.core.entity import Target, ValueData

import time
import re
import logging
import os


@pytest.fixture
def args(mocker):
    args = mocker.Mock()
    args.fixed_timeout = {'dns': 3, 'http': 3, 'reactivity': 3}
    args.fixed_format = '{ip}'
    args.fixed_format_params = ['ip']
    args.fixed_delimiter = ','
    args.alt_delimiter = ';'
    args.fixed_enclose = ''
    args.exhaustive = False

    return args


@pytest.fixture
def data(mocker):
    data = ValueData({})

    return data


@pytest.fixture
def requester(mocker):
    requester = mocker.Mock()

    return requester


class TestDataCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, requester, args):
        collector = PassDataCollector('TEST', requester, args)

        assert collector.get_name() == 'TEST'

        assert hasattr(collector, 'initialize')

        begin_time = time.time()
        time.sleep(0.5)
        v = collector._get_measure_time(begin_time)

        assert v < 2000 and v > 0

    def test_put(self, requester, args):
        collector = PassDataCollector('TEST', requester, args)

        data = ValueData({})
        response = {'a': 1, 'b': 2, 'c': 3}

        collector.put(data, response, 'a')
        collector.put(data, response, 'b', 'b2')

        assert data.get('a') == 1
        assert data.get('b2') == 2

        response['a'] = 3

        collector.fill(data, response, 'a')

        assert data.get('a') == 1


class TestRdapDataCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args, data):
        requester = RdapRequester(CountryDetector())

        collector = RdapCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'RDAP'
        assert success is True
        assert response_time > 0
        assert response['country'] == 'US'
        assert response['port43'] == 'whois.arin.net'
        assert collector.get_cidr(response) == '8.8.8.0/24'

        assert ('country' in collector.get_requires())

    def test_request_data(self, args):
        requester = RdapRequester(CountryDetector())

        collector = RdapCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response = collector.request_data(target)

        assert success is True
        assert response['country'] == 'US'
        assert response['port43'] == 'whois.arin.net'

    def test_build_data(self, args, data):
        requester = RdapRequester(CountryDetector())
        collector = RdapCollector(requester, args)

        target = Target()

        collector.build_data(target, data, False, {'cidr': 'abc'}, 8)
        assert data.get('cidr') == 'abc'


class TestDnsTxtCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args):
        requester = DnsResolveRequester()

        collector = DnsTxtCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'DNSTXT'
        assert success is True
        assert response_time > 0
        assert response['country'] == 'US'
        assert collector.get_cidr(response) == '8.8.8.0/24'

        assert ('country' in collector.get_requires())

    def test_request_data(self, args):
        requester = DnsResolveRequester()

        collector = DnsTxtCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response = collector.request_data(target)

        assert success is True
        assert response['country'] == 'US'

    def test_build_data(self, args, data):
        requester = DnsResolveRequester()
        collector = DnsTxtCollector(requester, args)

        target = Target()

        collector.build_data(target, data, False, {'cidr': 'abc'}, 8)
        assert data.get('cidr') == 'abc'


class TestIpInfoCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args):
        requester = IpInfoRequester()

        collector = IpInfoCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target)

        assert success is True
        assert response_time > 0
        assert response['country'] == 'US'
        assert response['timezone'] == 'America/Los_Angeles'
        assert collector.get_cidr(response) is None

        assert ('country' in collector.get_requires())

    def test_request_data(self, args):
        requester = IpInfoRequester()

        collector = IpInfoCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response = collector.request_data(target)

        assert collector.get_name() == 'IPINFO'
        assert success is True
        assert response['country'] == 'US'
        assert response['timezone'] == 'America/Los_Angeles'

    def test_build_data(self, args, data):
        requester = IpInfoRequester()
        collector = IpInfoCollector(requester, args)

        target = Target()

        collector.build_data(target, data, False, {'country': 'abc'}, 8)
        assert data.get('country') == 'abc'


class TestDnsReverseCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args):
        requester = DnsResolveRequester()

        collector = DnsReverseCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'DNSREVERSE'
        assert success is True
        assert response_time >= 0
        assert response['hostname'] == 'dns.google'

        assert ('hostname' in collector.get_requires())

    def test_request_data(self, args):
        requester = DnsResolveRequester()

        collector = DnsReverseCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response = collector.request_data(target)

        assert success is True
        assert response['hostname'] == 'dns.google'

    def test_build_data(self, args, data):
        requester = DnsResolveRequester()
        collector = DnsReverseCollector(requester, args)

        target = Target()

        collector.build_data(target, data, False, {'hostname': 'abc'}, 8)
        assert data.get('hostname') == 'abc'


class TestSelfCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args):
        requester = IpInfoRequester()
        dns_resolver = DnsResolveRequester()
        server_reactivity = ServerReactivity()

        collector = SelfCollector(requester, dns_resolver, server_reactivity, args)

        target = Target()

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'SELF_INFO'
        assert collector.get_requires() == []

        assert success is True
        assert response_time > 0
        assert len(response['country']) == 2
        assert len(response['region']) >= 0

    def test_request_data(self, args):
        requester = IpInfoRequester()
        dns_resolver = DnsResolveRequester()
        server_reactivity = ServerReactivity()

        collector = SelfCollector(requester, dns_resolver, server_reactivity, args)

        target = Target()

        success, response = collector.request_data(target)

        assert success is True

    def test_build_data(self, args):
        requester = IpInfoRequester()
        dns_resolver = DnsResolveRequester()
        server_reactivity = ServerReactivity()

        collector = SelfCollector(requester, dns_resolver, server_reactivity, args)

        target = Target()
        data = ValueData({})

        collector.build_data(target, data, True, {}, 8.0)

        assert data.get('ip') is None


class TestPassDataCollector:
    @pytest.fixture(autouse=True)
    def data(self):
        data = ValueData({})

        return data

    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request_data(self, args):
        requester = PassRequester()

        success, response = requester.request(None)

        assert success is False
        assert response == {}

    def test_request(self, args, data):
        requester = PassRequester()

        collector = PassDataCollector('PASS', requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response = requester.request(target)

        assert success is False
        assert requester.get_host() is None

        success, response, response_time = collector.request(target)

        assert success is False
        assert collector.initialize() is None
        assert collector.get_name() == 'PASS'
        assert collector.get_requires() == []
        assert collector.build_data(target, data, False, {}, 8) is None
        assert success is False

        success, response = collector.request_data(target)

        assert success is False

        success, response = collector.request_data(target)

        assert success is False

    def test_request2(self, mocker, args):
        requester = mocker.Mock(spec=PassRequester)
        requester.request.return_value = True, {'a': 1}

        collector = PassDataCollector('PASS', requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'PASS'
        assert success is True
        assert response['a'] == 1


class TestICMPCollector:
    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        monkeypatch.setattr('subprocess.check_output', lambda v, universal_newlines=True: 0)

    def test_request(self, args, monkeypatch):
        requester = ServerReactivity()

        if os.name != 'posix':
            monkeypatch.setattr(ServerReactivity, 'request_icmp', lambda *args, **kwargs: True)

        collector = ICMPCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'ICMP'
        assert success is True

        assert collector.get_requires()[0] == 'icmp'

    def test_build_data(self, args):
        requester = ServerReactivity()

        collector = ICMPCollector(requester, args)

        target = Target()
        data = ValueData({})
        collector.build_data(target, data, True, {}, 8.0)

        assert data.get('icmp') is True


class TestTCPCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args):
        requester = ServerReactivity()

        collector = TCPCollector(requester, args)

        target = Target()
        target.identifier = '1.1.1.1'
        target.ip = '1.1.1.1'
        target.port = 80

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'TCP'
        assert success is True

        assert collector.get_requires()[0] == 'tcp'

    def test_build_data(self, args):
        requester = ServerReactivity()

        collector = TCPCollector(requester, args)

        target = Target()
        data = ValueData({})
        collector.build_data(target, data, True, {}, 8.0)

        assert data.get('tcp') is True


class TestUDPCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args):
        requester = ServerReactivity()

        collector = UDPCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'
        target.port = 53

        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'UDP'
        assert success is True

        assert collector.get_requires()[0] == 'udp'

    def test_build_data(self, args):
        requester = ServerReactivity()

        collector = UDPCollector(requester, args)

        target = Target()
        data = ValueData({})
        collector.build_data(target, data, True, {}, 8.0)

        assert data.get('udp') is True


class TestHttpCollector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self, args, caplog):
        requester = HttpRequester()

        collector = HttpCollector(requester, args)

        target = Target()
        target.url = 'https://www.wikipedia.org/'

        collector.http = 2
        success, response, response_time = collector.request(target)

        assert collector.get_name() == 'HTTP'
        assert success is True
        assert response['http_status'] == 200
        assert ('http_status' in collector.get_requires())

        with caplog.at_level(logging.INFO):
            collector.request(target)

        assert re.search(r'HTTP_TIME', caplog.text)

    def test_build_data(self, args):
        requester = HttpRequester()

        collector = HttpCollector(requester, args)

        target = Target()
        data = ValueData({})
        collector.build_data(target, data, True, {}, 8.0)

        assert data.get('http') is True
