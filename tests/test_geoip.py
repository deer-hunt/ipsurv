import pytest

from ipsurv.requester.geoip import GeoIpRequester
from ipsurv.data_collector.geoip_collector import GeoIpCollector
from ipsurv.core.entity import Target, ValueData
from unittest.mock import MagicMock

import re
import os


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


class TestGeoIpRequester:
    '''
    geoip2.database.Reader Mock.
    If you want to test the actual behavior, preparing the GeoIP data file and remove the setup method.
    '''
    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch, mocker):
        if self._use_geoip_mock():
            monkeypatch.setattr(os.path, 'exists', lambda v: True)

            mock_geoip_reader = mocker.Mock(spec='geoip2.database.Reader')

            item = mocker.Mock()
            item.country.iso_code = 'US'
            item.city.continent.code = 'NA'
            item.autonomous_system_organization = 'GOOGLE'

            mock_geoip_reader.country = mocker.Mock(return_value=item)
            mock_geoip_reader.city = mocker.Mock(return_value=item)
            mock_geoip_reader.asn = mocker.Mock(return_value=item)

            monkeypatch.setattr(GeoIpRequester, '_get_geoip_reader', lambda *vs: mock_geoip_reader)
            monkeypatch.setattr(GeoIpRequester, '_import_geoip2', lambda *vs: mocker.Mock())

    def _use_geoip_mock(self):
        if os.getenv('GITHUB_ACTIONS') is not None or 'TOX_PACKAGE' in os.environ:
            return True

        # return True

        return False

    def test_request_methods(self):
        requester = GeoIpRequester()

        requester.initialize('/usr/local/share/GeoIP/')

        assert requester.get_data_path(None) == '/usr/local/share/GeoIP/'
        assert requester.get_data_path('/tmp/work') == '/tmp/work/'

        requester._delete_readers()

        assert requester.reader_country is None

        with pytest.raises(Exception):
            requester.get_reader('dummy')

        requester._delete_readers()
        assert requester.reader_country is None

    def test_import_geoip2(self):
        requester = GeoIpRequester()
        module = requester._import_geoip2()

        assert module is not None

    def test_errors(self, monkeypatch):
        requester = GeoIpRequester()
        requester.initialize('/usr/local/share/GeoIP/')
        requester.geoip2 = None

        with pytest.raises(Exception, match='GeoIp object is not'):
            requester.request('8.8.8.8')

        if self._use_geoip_mock():
            monkeypatch.setattr(os.path, 'exists', lambda v: False)

        requester = GeoIpRequester()
        requester.initialize('/tmp/')

        with pytest.raises(Exception, match='GeoIP data file none'):
            requester.request_country('8.8.8.8')

        with pytest.raises(Exception, match='GeoIP data file none'):
            requester.request_city('8.8.8.8')

        with pytest.raises(Exception, match='GeoIP data file none'):
            requester.request_asn('8.8.8.8')

    def test_request(self):
        requester = GeoIpRequester()
        requester.initialize('/usr/local/share/GeoIP/')

        response = requester.request('8.8.8.8')

        assert response['country'] == 'US'
        assert response['organization'] == 'GOOGLE'

    def test_request_country(self):
        requester = GeoIpRequester()
        requester.initialize('/usr/local/share/GeoIP/')

        response = requester.request_country('8.8.8.8')

        assert response['country'] == 'US'

    def test_request_city(self):
        requester = GeoIpRequester()
        requester.initialize('/usr/local/share/GeoIP/')

        response = requester.request_city('8.8.8.8')

        assert response['country'] == 'US'

    def test_request_asn(self):
        requester = GeoIpRequester()
        requester.initialize('/usr/local/share/GeoIP/')

        response = requester.request_asn('8.8.8.8')

        assert response['organization'] == 'GOOGLE'


class TestGeoIpCollector:
    @pytest.fixture
    def requester(self, mocker):
        requester = mocker.Mock(spec=GeoIpRequester)
        requester.request_country = MagicMock(return_value={'country': 'US'})
        requester.request_city = MagicMock(return_value={'continent': 'NA'})
        requester.request_asn = MagicMock(return_value={'organization': 'GOOGLE'})

        return requester

    def test_general(self, args, requester):
        collector = GeoIpCollector(requester, args)

        assert collector.get_name() == 'GEOIP'

    def test_request(self, args, requester):
        collector = GeoIpCollector(requester, args)

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target, ['country'])

        assert success is True
        assert response['country'] == 'US'

        assert ('country' in collector.get_requires())

        success, response, response_time = collector.request(target, ['continent'])

        assert success is True
        assert response['continent'] == 'NA'

        target.ip = '8.8.8.8'

        success, response, response_time = collector.request(target, ['asn'])

        assert success is True
        assert response['organization'] == 'GOOGLE'

    def test_request_city(self, args, requester):
        collector = GeoIpCollector(requester, args)

        response = {'types': []}
        assert collector._request_city('8.8.8.8', response) is None

    def test_request_country(self, args, requester):
        collector = GeoIpCollector(requester, args)

        response = {'types': []}
        assert collector._request_country('8.8.8.8', response) is None

    def test_request_asn(self, args, requester):
        collector = GeoIpCollector(requester, args)

        response = {'types': []}
        assert collector._request_asn('8.8.8.8', response) is None

    #    def test_request_data(self, args):
#        pass
#
    def test_build_data(self, args, requester):
        collector = GeoIpCollector(requester, args)

        data = ValueData({})

        target = Target()
        target.identifier = '8.8.8.8'
        target.ip = '8.8.8.8'

        response = {
            'continent': None,
            'continent_name': None,
            'country': None,
            'country_name': None,
            'city': None,
            'city_name': None,
            'organization': None,
            'org': None,
            'timezone': None,
            'latitude': 0.1,
            'longitude': 0.1
        }

        collector.build_data(target, data, True, response, 10)

        assert data.get('geo') == '0.1,0.1'
