import pytest

from ipsurv.requester.ip_info import IpInfoRequester
from ipsurv.requester.rdap import RdapRequester, CountryDetector
from ipsurv.requester.dns_resolver import DnsResolveRequester
from ipsurv.requester.http import HttpRequester
from ipsurv.requester.server_reactivity import ServerReactivity
import http.client
import socket
import re


class TestRequester:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_create_http_connection(self):
        requester = IpInfoRequester()

        con = requester._create_http_connection('8.8.8.8')
        assert type(con).__name__ == 'HTTPSConnection'

        con = requester._create_http_connection('8.8.8.8', False)
        assert type(con).__name__ == 'HTTPConnection'


class TestIpInfoRequester:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self):
        requester = IpInfoRequester()

        success, response = requester.request('8.8.8.8')

        assert success is True
        assert response['ip'] == '8.8.8.8'
        assert response['country'] == 'US'
        assert response['timezone'] == 'America/Los_Angeles'

    def test_request_fail(self):
        requester = IpInfoRequester()

        with pytest.raises(http.client.HTTPException):
            success, response = requester.request('499.499.499.499')

    def test_timeout(self):
        requester = IpInfoRequester(timeout=0.005)

        with pytest.raises(socket.timeout):
            success, response = requester.request('53.112.1.0')


class TestIpRdapRequester:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector)

        success, response = requester.request('8.8.8.8')

        assert success is True
        assert response['port43'] == 'whois.arin.net'
        assert response['country'] == 'US'

    def test_detect_server_from_ip(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector)

        server = requester.detect_server_from_ip('213.1.1.1')

        assert server is not None

    def test_get_octet2_by_ip(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector)

        v = requester.detect_server_from_ip('192.168.1.1')

        assert v == 'https://rdap.arin.net/registry/'

    def test_get_id_from_server(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector)

        v = requester.get_id_from_server('https://rdap.arin.net/registry/')

        assert v == 1

    def test_request_fail(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector)

        with pytest.raises(http.client.HTTPException):
            success, response = requester.request('499.499.499.499')

    def test_timeout(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector, timeout=0.001)

        with pytest.raises(Exception):
            success, response = requester.request('53.10.1.0')

    def test_request_http(self):
        country_detector = CountryDetector()
        requester = RdapRequester(country_detector)

        res, body = requester.request_http('http://google.com/')

        assert res is not None


class TestCountryDetector:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_detect(self):
        country_detector = CountryDetector()

        code = country_detector.detect_by_address('119 Washington Square N, New York, NY 20011, USA 1100')
        assert code == 'US'

        code = country_detector.detect_by_address('119 Washington Square N, New York, NY 20011, US,')
        assert code == 'US'

        code = country_detector.detect_by_address('119 Washington Square N, New York, NY 20011, U.S.,')
        assert code == 'US'

        code = country_detector.detect_by_address('U.S., 219 Washington Square N, New York, NY 30011')
        assert code == 'US'

        code = country_detector.detect_by_address("Washington, 1475 Kind Plaza Ld, United States")
        assert code == 'US'

        code = country_detector.detect_by_address('142 ABC 6-ro, Sejong-si, 8932, Republic of Korea.')
        assert code == 'KR'

        code = country_detector.detect_by_address('Seoul support Center 1136 Sejong-daero, Jung-gu Seoul 804520, Korea')
        assert code == 'KR'

        code = country_detector.detect_by_address('Seoul support Center 1136 Sejong-daero, Jung-gu Seoul 804520, South Korea')
        assert code == 'KR'

        code = country_detector.detect_by_address("PO Box 86827 98721 Pyongyang Democratic People's Republic of Korea")
        assert code == 'KP'

        code = country_detector.detect_by_address("Jongno-gu, Republic of Korea")
        assert code == 'KR'

        code = country_detector.detect_by_address("Case postale 8330 CH-11218 Le Grand-A, Geneva, Switzerland")
        assert code == 'CH'

        code = country_detector.detect_by_address("Roosevelt Road, Taipei, 1870319 Taiwan")
        assert code == 'TW'

        code = country_detector.detect_by_address("Badu Rd., Zhongshan Dist., Taipei City 19704, Taiwan (R.O.C.)")
        assert code == 'TW'

        code = country_detector.detect_by_address('28-12-36 Uchi-Kanda;Chiyoda-ku;Tokyo 101-0047;japan')
        assert code == 'JP'

        code = country_detector.detect_by_address("Shad / Famine\n1875 rue d'Ague\n982100 Billancourt\nFr")
        assert code == 'FR'


class TestDnsResolveRequester:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request_resolve(self):
        requester = DnsResolveRequester()

        success, response = requester.request_resolve('google.com')

        assert re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', response['ip'])

        with pytest.raises(Exception):
            success, response = requester.request_resolve('dummy')

    def test_resolve_ip(self):
        requester = DnsResolveRequester()

        ip = requester.resolve_ip('google.com')

        assert re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)

    def test_request_reverse(self):
        requester = DnsResolveRequester()

        success, response = requester.request_reverse('8.8.8.8')

        assert response['hostname'] == 'dns.google'

    def test_request_dnstxt(self):
        requester = DnsResolveRequester()

        success, response = requester.request_dnstxt('8.8.8.8')

        assert response['country'] == 'US'
        assert response['cidr'] == '8.8.8.0/24'

    def test_get_resolver(self):
        requester = DnsResolveRequester()

        assert type(requester.get_resolver()).__name__ == 'Resolver'

        requester = DnsResolveRequester({})

        assert type(requester.get_resolver()) == dict


class TestHttpRequester:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_request(self):
        requester = HttpRequester()

        success, response = requester.request('wikipedia.org')

        assert success is True
        assert response['http_status'] == 200
        assert response['http_size'] > 256

        with pytest.raises(Exception):
            requester.request('wikipedia-not-found.xyz')

    def test_request_http(self):
        requester = HttpRequester()

        requester.set_headers({})

        res, body = requester.request_http('https://www.wikipedia.org')

        assert res.status == 200
        assert len(body) > 256

    def test_request_alpn_h2request_http(self):
        requester = HttpRequester()

        r = requester.request_alpn_h2('https://www.wikipedia.org')

        assert r == 1

        assert requester.request_alpn_h2('https://www.wikipedia-not-found.xyz') == -1

    def test_create_url(self):
        requester = HttpRequester()

        url = requester._create_url('//www.wikipedia.org')
        assert re.search(r'http:', url)

        url = requester._create_url('www.wikipedia.org')
        assert re.search(r'http:', url)

        url = requester._create_url('http://www.wikipedia.org')
        assert re.search(r'http:', url)


class TestServerReactivity:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.requester = ServerReactivity()

    def test_request_icmp(self, monkeypatch):
        monkeypatch.setattr('subprocess.check_output', lambda v, universal_newlines=True: 0)
        success = self.requester.request_icmp('wikipedia.org')

        assert success is True

    def test_request_tcp(self):
        success = self.requester.request_tcpport('wikipedia.org', 80)

        assert success is True

        success = self.requester.request_tcpport('wikipedia.org', 443)

        assert success is True

    def test_request_udp(self):
        success = self.requester.request_udpport('8.8.8.8', 53)

        assert success is True

    def test_request_fail(self):
        requester = ServerReactivity(timeout=0.001)

        with pytest.raises(Exception):
            requester.request_icmp('6.1.1.1')

        with pytest.raises(socket.timeout):
            requester.request_tcpport('wikipedia.org', 81)

        with pytest.raises(socket.timeout):
            requester.request_udpport('8.8.8.8', 52)
