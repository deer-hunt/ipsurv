from abc import ABC

from ipsurv.configure.args_builder import ArgsBuilder
from ipsurv.configs import Config
from ipsurv.core.entity import ValueDataFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.target_parser import TargetParser
from ipsurv.data_collector.basic_collectors import RdapCollector, DnsTxtCollector, IpInfoCollector, DnsReverseCollector
from ipsurv.data_collector.reactivity_collectors import ICMPCollector, TCPCollector, UDPCollector, HttpCollector
from ipsurv.data_collector.geoip_collector import GeoIpCollector
from ipsurv.data_collector.self_collector import SelfCollector
from ipsurv.requester.dns_resolver import DnsResolveRequester
from ipsurv.requester.http import HttpRequester
from ipsurv.requester.ip_info import IpInfoRequester
from ipsurv.requester.rdap import CountryDetector, RdapRequester
from ipsurv.requester.geoip import GeoIpRequester
from ipsurv.requester.server_reactivity import ServerReactivity
from ipsurv.serializer.json_serializer import JsonSerializer
from ipsurv.serializer.line_serializer import LineSerializer
from ipsurv.serializer.line_serializer import Serializer


class ObjectFactory(ABC):
    """
    Description:
    https://deer-hunt.github.io/ipsurv/pages/program_architecture_classes.html#objectfactory
    """
    def get_config(self):
        """
        :rtype: Config
        """
        return Config

    def create_pipeline(self):
        """
        :rtype: Pipeline
        """
        return Pipeline()

    def create_value_data_factory(self, args, config):
        """
        :param args:
        :type args: argparse.Namespace
        :param config:
        :type config: Config
        :rtype: ValueDataFactory
        """
        return ValueDataFactory(config.MASTER_DATA, args.fixed_format_params)

    def create_args_builder(self, config, pipeline):
        """
        :param config:
        :type config: Config
        :param pipeline:
        :type pipeline: Pipeline
        :rtype: ArgsBuilder
        """
        return ArgsBuilder(config, pipeline)

    def create_target_parser(self, args, pipeline, dns_resolver):
        """
        :param args:
        :type args: argparse.Namespace
        :param pipeline:
        :type pipeline: Pipeline
        :param dns_resolver:
        :type dns_resolver: DnsResolveRequester
        :rtype: TargetParser
        """
        return TargetParser(args, pipeline, dns_resolver)

    def create_dns_resolver(self, args):
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: DnsResolveRequester
        """
        return DnsResolveRequester(timeout=args.fixed_timeout['dns'])

    def create_collectors(self, args, dns_resolver):
        """
        :param args:
        :type args: argparse.Namespace
        :param dns_resolver:
        :type dns_resolver: DnsResolveRequester
        :rtype: dict
        """
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

        if 'geoip' in _collectors:
            collectors['geoip'] = self.create_geoip_collector(args)

        return collectors

    def create_rdap_collector(self, args):
        """
        :param args:
        :type args: argparse.Namespace
       :rtype: RdapCollector
        """
        country_detector = CountryDetector()

        return RdapCollector(RdapRequester(country_detector, timeout=args.fixed_timeout['http']), args)

    def create_dnstxt_collector(self, dns_resolver, args):
        """
        :param dns_resolver:
        :type dns_resolver: DnsResolveRequester
        :param args:
        :type args: argparse.Namespace
        :rtype: DnsTxtCollector
        """
        return DnsTxtCollector(dns_resolver, args)

    def create_ipinfo_collector(self, args):
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: IpInfoCollector
        """
        return IpInfoCollector(IpInfoRequester(timeout=args.fixed_timeout['http'], token=args.conf.get('ipinfo_token')), args)

    def create_geoip_collector(self, args):
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: GeoIpCollector
        """
        return GeoIpCollector(GeoIpRequester(), args)

    def create_self_collector(self, args, dns_resolver, server_reactivity):
        """
        :param args:
        :type args: argparse.Namespace
        :param dns_resolver:
        :type dns_resolver: DnsResolveRequester
        :param server_reactivity:
        :type server_reactivity: ServerReactivity
        :rtype: SelfCollector
        """
        return SelfCollector(IpInfoRequester(timeout=args.fixed_timeout['http']), dns_resolver, server_reactivity, args)

    def create_dns_reverse_collector(self, dns_resolver, args):
        """
        :param dns_resolver:
        :type dns_resolver: DnsResolveRequester
        :param args:
        :type args: argparse.Namespace
        :rtype: SelfCollector
        """
        return DnsReverseCollector(dns_resolver, args)

    def create_reactivities(self, args):
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: list
        """

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
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: ServerReactivity
        """

        return ServerReactivity(timeout=args.fixed_timeout['reactivity'])

    def create_http(self, args):
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: HttpRequester
        """
        return HttpRequester(timeout=args.fixed_timeout['reactivity'])

    def create_icmp_collector(self, requester, args):
        """
        :param server_reactivity:
        :type server_reactivity: ServerReactivity
        :param args:
        :type args: argparse.Namespace
        :rtype: ICMPCollector
        """
        return ICMPCollector(requester, args)

    def create_tcp_collector(self, requester, args):
        """
        :param server_reactivity:
        :type server_reactivity: ServerReactivity
        :param args:
        :type args: argparse.Namespace
        :rtype: TCPCollector
        """
        return TCPCollector(requester, args)

    def create_udp_collector(self, requester, args):
        """
        :param server_reactivity:
        :type server_reactivity: ServerReactivity
        :param args:
        :type args: argparse.Namespace
        :rtype: UDPCollector
        """
        return UDPCollector(requester, args)

    def create_http_collector(self, requester, args):
        """
        :param server_reactivity:
        :type server_reactivity: ServerReactivity
        :param args:
        :type args: argparse.Namespace
        :rtype: HttpCollector
        """
        return HttpCollector(requester, args)

    def create_serializer(self, args):
        """
        :param args:
        :type args: argparse.Namespace
        :rtype: Serializer
        """

        if not args.json:
            serializer = LineSerializer(args)
        else:
            serializer = JsonSerializer(args)

        return serializer
