import logging

from ipsurv.requester.requester import Requester
import os


class GeoIpRequester(Requester):
    """
    Description:
    https://deer-hunt.github.io/ipsurv/pages/using_geoip2.html
    """

    TYPE_COUNTRY = 'country'
    TYPE_CITY = 'city'
    TYPE_ASN = 'asn'

    def __init__(self):
        super().__init__(0.0)

        self.geoip2 = self._import_geoip2()

        self.reader_country = None
        self.reader_city = None
        self.reader_asn = None

        self.data_path = None
        self.data_files = {}

    def __del__(self):
        self._delete_readers()

    def _import_geoip2(self):
        module = None

        try:
            module = __import__('geoip2.database')
        except ImportError:
            pass

        return module

    def initialize(self, data_path=None, data_files=None):
        if self.geoip2:
            self._delete_readers()

            self.data_path = self.get_data_path(data_path)
            self.data_files = self.detect_files(data_files)

    def get_data_path(self, path):
        if not path:
            paths = ['/usr/local/share/GeoIP/', '/var/lib/GeoIP/', '/opt/geoip/', '~/geoip/']

            for v in paths:
                v = os.path.expanduser(v)

                if os.path.exists(v):
                    path = v
                    break

            if not path:
                raise Exception('GeoIP data dir detection is failed.')

        path = path.strip().rstrip('/') + '/'

        return path

    def detect_files(self, files):
        files = files if files is not None else {}

        files[self.TYPE_COUNTRY] = self.detect_file(files, self.TYPE_COUNTRY, ['GeoLite2-Country.mmdb', 'GeoIP2-Country.mmdb'], )
        files[self.TYPE_CITY] = self.detect_file(files, self.TYPE_CITY, ['GeoLite2-City.mmdb', 'GeoIP2-City.mmdb'])
        files[self.TYPE_ASN] = self.detect_file(files, self.TYPE_ASN, ['GeoLite2-ASN.mmdb', 'GeoIP2-ASN.mmdb'])

        return files

    def detect_file(self, files, gtype, candidates):
        file = None

        if not files.get(gtype):
            for t in candidates:
                if os.path.exists(self.data_path + t):
                    file = t
                    break
        else:
            file = files[gtype]

        return file

    def _create_reader(self, gtype):
        if not self.geoip2:
            raise Exception('GeoIp object is not initialized.')

        path = None

        if self.data_files[gtype] is not None:
            path = self.data_path + self.data_files[gtype]

        if not path:
            raise Exception("GeoIP data file none.({})".format(gtype))

        return self._get_geoip_reader(path)

    def _get_geoip_reader(self, path):
        return self.geoip2.database.Reader(path)

    def _delete_readers(self):
        if self.reader_country:
            self.reader_country.close()
            self.reader_country = None

        if self.reader_city:
            self.reader_city.close()
            self.reader_city = None

        if self.reader_asn:
            self.reader_asn.close()
            self.reader_asn = None

    def request(self, ip):
        response = {}

        response.update(self.request_country(ip))
        response.update(self.request_city(ip))
        response.update(self.request_asn(ip))

        return response

    def request_country(self, ip):
        if not self.reader_country:
            self.reader_country = self._create_reader(self.TYPE_COUNTRY)

        country_obj = self.reader_country.country(ip)

        response = {}

        response['continent'] = country_obj.continent.code
        response['continent_name'] = country_obj.continent.name
        response['country'] = country_obj.country.iso_code
        response['country_name'] = country_obj.country.name

        return response

    def request_city(self, ip):
        if not self.reader_city:
            self.reader_city = self._create_reader(self.TYPE_CITY)

        city_obj = self.reader_city.city(ip)

        response = {}

        response['continent'] = city_obj.continent.code
        response['continent_name'] = city_obj.continent.name
        response['country'] = city_obj.country.iso_code
        response['country_name'] = city_obj.country.name
        response['subdivision'] = city_obj.subdivisions.most_specific.iso_code if hasattr(city_obj, 'subdivisions') else None
        response['subdivision_name'] = city_obj.subdivisions.most_specific.name if hasattr(city_obj, 'subdivisions') else None
        response['city'] = city_obj.city.code if hasattr(city_obj.city, 'code') else None
        response['city_name'] = city_obj.city.name if hasattr(city_obj.city, 'name') else None
        response['timezone'] = city_obj.location.time_zone
        response['latitude'] = city_obj.location.latitude
        response['longitude'] = city_obj.location.longitude

        return response

    def request_asn(self, ip):
        if not self.reader_asn:
            self.reader_asn = self._create_reader(self.TYPE_ASN)

        asn_obj = self.reader_asn.asn(ip)

        response = {}

        response['asn'] = 'AS' + str(asn_obj.autonomous_system_number)
        response['organization'] = asn_obj.autonomous_system_organization

        return response
