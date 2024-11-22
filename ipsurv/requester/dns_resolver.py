import dns.resolver
import ipaddress

from ipsurv.requester.requester import Requester
from ipsurv.util.network_util import DnsUtil


class DnsResolveRequester(Requester):
    def __init__(self, resolver=None, timeout=4.0):
        super().__init__(timeout)

        self.resolver = resolver

    def request_resolve(self, hostname):
        success = False
        response = {}

        ip = self.resolve_ip(hostname)

        if ip:
            success = True
            response = {'ip': ip}

        return success, response

    def resolve_ip(self, hostname, port=None):
        ip = DnsUtil.resolve(hostname, port, timeout=self.timeout)

        return ip

    def request_reverse(self, ip):
        hostname = DnsUtil.reverse(ip, timeout=self.timeout)

        response = {'hostname': hostname}
        success = True

        return success, response

    # "15169 | 8.8.8.0/24 | US | arin | 2023-12-28"
    def request_dnstxt(self, ip):
        server = 'origin.asn.cymru.com'

        resolver = self.get_resolver()

        resolver.lifetime = self.timeout

        reversed_ip = str(dns.reversename.from_address(ip, v4_origin=None))

        v = reversed_ip + '.' + server

        tv = resolver.query(v, 'TXT')

        vals = str(tv[0]).strip("\"'\t ").split('|')

        vals = list(map(lambda v: v.strip(), vals))

        cidr = vals[1]

        network = ipaddress.ip_network(cidr, strict=False)

        response = {
            'cidr': cidr,
            'network_start': str(network.network_address),
            'network_end': str(network.broadcast_address),
            'country': vals[2],
            'rir': vals[3],
            'date': vals[4]
        }

        success = True

        return success, response

    def get_resolver(self):
        if self.resolver is None:
            self.resolver = dns.resolver.Resolver()
            self.resolver.timeout = self.timeout

        return self.resolver
