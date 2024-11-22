import random

from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.util.network_util import DnsUtil


class SelfCollector(DataCollector):
    def __init__(self, requester, dns_resolver, server_reactivity, args):
        super().__init__(requester, args)

        self.dns_resolver = dns_resolver
        self.server_reactivity = server_reactivity
        self.dns_timeout = args.fixed_timeout['dns']

    def get_name(self):
        return 'SELF_INFO'

    def get_requires(self):
        return []

    def request_data(self, target):
        DnsUtil.resolve(self.requester.get_host(), timeout=self.dns_timeout)

        success, response = self.requester.request(None)

        resolver = self.dns_resolver.get_resolver()

        response['local_dns'] = resolver.nameservers

        ip = random.choice(['8.8.8.8', '8.8.4.4', '1.1.1.1'])

        response['local_ip'] = self.server_reactivity.request_local_ip(ip=ip)

        return success, response

    def build_data(self, target, data, success, response, response_time):
        self.put(data, response, 'ip')
        self.put(data, response, 'hostname')
        self.put(data, response, 'country')
        self.put(data, response, 'city')
        self.put(data, response, 'region')
        self.put(data, response, 'postal')
        self.put(data, response, 'loc', 'geo')
        self.put(data, response, 'org', 'organization')
        self.put(data, response, 'timezone')
        self.put(data, response, 'local_dns')
        self.put(data, response, 'local_ip')

        self._append_error(data, response)
