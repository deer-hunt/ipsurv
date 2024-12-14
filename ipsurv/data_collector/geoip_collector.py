from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.util.sys_util import System
import logging


class GeoIpCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.geoip.GeoIpRequester
    :param args:
    :type args: argparse.Namespace

    Description:
    https://deer-hunt.github.io/ipsurv/pages/using_geoip2.html
    """

    COUNTRY_COLS = ['continent', 'continent_name', 'country', 'country_name']
    CITY_COLS = ['continent', 'continent_name', 'country', 'country_name', 'subdivision', 'subdivision_name', 'city', 'city_name', 'timezone', 'geo']
    ASN_COLS = ['asn', 'org']

    def __init__(self, requester, args):
        super().__init__(requester, args)

    def initialize(self, args):
        geoip_conf = args.conf.get('geoip')

        path = None
        files = None

        if isinstance(geoip_conf, dict):
            path = geoip_conf.get('path')
            ts = geoip_conf.get('files')
            files = ts if isinstance(ts, dict) else None

        self.requester.initialize(path, files)

        if self.requester.geoip2 is not None:
            if System.is_logging():
                logging.log(logging.INFO, 'GEOIP:ENABLED')
                logging.log(logging.INFO, 'GEOIP_DATA_PATH:' + self.requester.data_path)
                logging.log(logging.INFO, 'GEOIP_DATA_FILES:' + str(self.requester.data_files))
        else:
            logging.log(logging.INFO, 'GEOIP:DISABLED')

    def get_name(self):
        return 'GEOIP'

    def request_data(self, target, requires):
        ip = target.ip

        error_city = None
        error_country = None
        response = {'types': []}

        only_city_cols = set(self.CITY_COLS) - set(self.COUNTRY_COLS)
        require_only_city = True if requires is not None and only_city_cols & set(requires) else False

        if requires is None or set(self.CITY_COLS) & set(requires):
            error_city = self._request_city(ip, response)

        if requires is None or set(self.COUNTRY_COLS) & set(requires) and not response.get('country'):
            error_country = self._request_country(ip, response)

        if require_only_city and error_city:
            raise error_city
        elif error_country:
            raise error_country

        if requires is None or set(self.ASN_COLS) & set(requires):
            self._request_asn(ip, response)

        return True, response

    def _request_city(self, ip, response):
        error = None

        try:
            response['types'].append('city')

            res = self.requester.request_city(ip)

            response.update(res)
        except Exception as e:
            error = e

        return error

    def _request_country(self, ip, response):
        error = None

        try:
            response['types'].append('country')

            res = self.requester.request_country(ip)

            response.update(res)
        except Exception as e:
            error = e

        return error

    def _request_asn(self, ip, response):
        response['types'].append('asn')

        res = self.requester.request_asn(ip)

        response.update(res)

    def get_requires(self):
        return ['continent', 'continent_name', 'country', 'country_name', 'city', 'city_name', 'geo', 'org', 'asn', 'timezone']

    def build_data(self, target, data, success, response, response_time):
        data.set('geoip_time', response_time)

        self.put(data, response, 'continent')
        self.put(data, response, 'continent_name')
        self.put(data, response, 'subdivision')
        self.put(data, response, 'subdivision_name')
        self.put(data, response, 'country')
        self.put(data, response, 'country_name')
        self.put(data, response, 'city')
        self.put(data, response, 'city_name')
        self.put(data, response, 'organization', 'org')
        self.put(data, response, 'asn')
        self.put(data, response, 'timezone')

        if response.get('latitude') is not None and response.get('longitude') is not None:
            geo = str(response.get('latitude')) + ',' + str(response.get('longitude'))
            data.set('geo', geo)

        self._append_error(data, response)
