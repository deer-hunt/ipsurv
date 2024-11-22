from abc import ABC

from ipsurv.configure.args_builder import ArgsBuilder
from ipsurv.configs import Config
from ipsurv.core.entity import ValueDataFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.target_parser import TargetParser
from ipsurv.data_collector.basic_collectors import RdapCollector, DnsTxtCollector, IpInfoCollector, DnsReverseCollector
from ipsurv.data_collector.reactivity_collectors import ICMPCollector, TCPCollector, UDPCollector, HttpCollector
from ipsurv.data_collector.self_collector import SelfCollector
from ipsurv.requester.dns_resolver import DnsResolveRequester
from ipsurv.requester.http import HttpRequester
from ipsurv.requester.ip_info import IpInfoRequester
from ipsurv.requester.rdap import CountryDetector, RdapRequester
from ipsurv.requester.server_reactivity import ServerReactivity
from ipsurv.serializer.json_serializer import JsonSerializer
from ipsurv.serializer.line_serializer import LineSerializer


class ObjectFactory(ABC):
    def get_config(self):
        return Config

    def create_pipeline(self):
        return Pipeline()

    def create_value_data_factory(self, args, config):
        return ValueDataFactory(config.MASTER_DATA, args.fixed_format_params)

    def create_args_builder(self, config, pipeline):
        return ArgsBuilder(config, pipeline)

    def create_target_parser(self, args, pipeline, dns_resolver):
        return TargetParser(args, pipeline, dns_resolver)

    def create_dns_resolver(self, args):
        return DnsResolveRequester(timeout=args.fixed_timeout['dns'])

    def create_collectors(self, args, dns_resolver):
        collectors = {}

        _collectors = args.fixed_collectors

        if 'rdap' in _collectors:
            collectors['rdap'] = self.create_rdap_collector(args)

        if 'dnstxt' in _collectors:
            collectors['dnstxt'] = self.create_dnstxt_collector(dns_resolver, args)

        if 'ipinfo' in _collectors:
            collectors['ipinfo'] = self.create_ipinfo_collector(args)

        if 'dnsreverse' in _collectors:
            collectors['dnsreverse'] = self.create_dns_reverse_collector(dns_resolver, args)

        return collectors

    def create_rdap_collector(self, args):
        country_detector = CountryDetector()

        return RdapCollector(RdapRequester(country_detector, timeout=args.fixed_timeout['http']), args)

    def create_dnstxt_collector(self, dns_resolver, args):
        return DnsTxtCollector(dns_resolver, args)

    def create_ipinfo_collector(self, args):
        return IpInfoCollector(IpInfoRequester(timeout=args.fixed_timeout['http'], token=args.conf.get('ipinfo_token')), args)

    def create_self_collector(self, args, dns_resolver, server_reactivity):
        return SelfCollector(IpInfoRequester(timeout=args.fixed_timeout['http']), dns_resolver, server_reactivity, args)

    def create_dns_reverse_collector(self, dns_resolver, args):
        return DnsReverseCollector(dns_resolver, args)

    def create_reactivities(self, args):
        server_reactivities = []

        requester = self.create_server_reactivity(args)

        if args.icmp:
            server_reactivities.append(self.create_icmp_collector(requester, args))

        if args.tcp:
            server_reactivities.append(self.create_tcp_collector(requester, args))

        if args.udp:
            server_reactivities.append(self.create_udp_collector(requester, args))

        if args.http:
            http_requester = self.create_http(args)
            server_reactivities.append(self.create_http_collector(http_requester, args))

        return server_reactivities

    def create_server_reactivity(self, args):
        return ServerReactivity(timeout=args.fixed_timeout['reactivity'])

    def create_http(self, args):
        return HttpRequester(timeout=args.fixed_timeout['reactivity'])

    def create_icmp_collector(self, requester, args):
        return ICMPCollector(requester, args)

    def create_tcp_collector(self, requester, args):
        return TCPCollector(requester, args)

    def create_udp_collector(self, requester, args):
        return UDPCollector(requester, args)

    def create_http_collector(self, requester, args):
        return HttpCollector(requester, args)

    def create_serializer(self, args):
        if not args.json:
            serializer = LineSerializer(args)
        else:
            serializer = JsonSerializer(args)

        return serializer
