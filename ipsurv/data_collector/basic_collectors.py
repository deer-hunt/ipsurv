import re

from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.util.network_util import DnsUtil


class RdapCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.rdap.RdapRequester
    :param args:
    :type args: argparse.Namespace
    """

    def __init__(self, requester, args):
        super().__init__(requester, args)

        self.dns_timeout = args.fixed_timeout['dns']

    def get_name(self):
        return 'RDAP'

    def request_data(self, target, requires):
        DnsUtil.resolve(self.requester.get_host(), timeout=self.dns_timeout)

        return self.requester.request(target.ip)

    def get_requires(self):
        return ['cidr', 'network_start', 'network_end', 'country', 'name', 'handle', 'org', 'address', 'port43', 'description']

    def get_cidr(self, response):
        return response.get('cidr')

    def build_data(self, target, data, success, response, response_time):
        data.set('rdap_time', response_time)

        self.put(data, response, 'cidr')
        self.put(data, response, 'startAddress', 'network_start')
        self.put(data, response, 'endAddress', 'network_end')
        self.put(data, response, 'country')
        self.put(data, response, 'country_updated')
        self.put(data, response, 'name')
        self.put(data, response, 'port43')

        if response.get('primary_entity'):
            entity = response.get('primary_entity')

            data.set('handle', entity.get('handle'))
            data.set('org', entity.get('name'))
            data.set('address', self.sanitize(entity.get('address')))

        description = ''

        if 'remarks' in response:
            remarks = response['remarks']

            if len(remarks) > 0 and 'description' in remarks[0] and len(remarks[0]['description']) > 0:
                description = self.sanitize(remarks[0]['description'][0])

        data.set('description', description)

        self._append_error(data, response)

    def sanitize(self, v):
        return re.sub(r'\s+', ' ', v)


class DnsTxtCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.dns_resolver.DnsResolveRequester
    :param args:
    :type args: argparse.Namespace
    """

    def get_name(self):
        return 'DNSTXT'

    def request_data(self, target, requires):
        return self.requester.request_dnstxt(target.ip)

    def get_requires(self):
        return ['cidr', 'network_start', 'network_end', 'country', 'rir']

    def get_cidr(self, response):
        return response.get('cidr')

    def build_data(self, target, data, success, response, response_time):
        data.set('dnstxt_time', response_time)

        self.put(data, response, 'cidr')
        self.put(data, response, 'network_start')
        self.put(data, response, 'network_end')
        self.put(data, response, 'country')
        self.put(data, response, 'rir')

        self._append_error(data, response)


class IpInfoCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.ip_info.IpInfoRequester
    :param args:
    :type args: argparse.Namespace
    """

    def __init__(self, requester, args):
        super().__init__(requester, args)

        self.dns_timeout = args.fixed_timeout['dns']

    def get_name(self):
        return 'IPINFO'

    def request_data(self, target, requires):
        DnsUtil.resolve(self.requester.get_host(), timeout=self.dns_timeout)

        return self.requester.request(target.ip)

    def get_requires(self):
        return ['ip', 'hostname', 'country', 'region_name', 'city_name', 'postal', 'geo', 'asn', 'org', 'timezone']

    def build_data(self, target, data, success, response, response_time):
        data.set('ipinfo_time', response_time)

        self.fill(data, response, 'ip')
        self.fill(data, response, 'hostname')
        self.put(data, response, 'country')
        self.put(data, response, 'city', 'city_name')
        self.put(data, response, 'region', 'region_name')
        self.put(data, response, 'postal')
        self.put(data, response, 'loc', 'geo')
        self.put(data, response, 'asn')
        self.put(data, response, 'org')
        self.put(data, response, 'timezone')

        self._append_error(data, response)


class DnsReverseCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.dns_resolver.DnsResolveRequester
    :param args:
    :type args: argparse.Namespace
    """

    def get_name(self):
        return 'DNSREVERSE'

    def request_data(self, target, requires):
        return self.requester.request_reverse(target.ip)

    def get_requires(self):
        return ['hostname']

    def build_data(self, target, data, success, response, response_time):
        data.set('dnsreverse_time', response_time)

        self.put(data, response, 'hostname')

        self._append_error(data, response)
