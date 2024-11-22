import pytest

from ipsurv.core.object_factory import ObjectFactory


class TestObjectFactory:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_factory = ObjectFactory()

    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.fixed_format_params = []
        args.fixed_timeout = {'dns': 0, 'http': 0, 'reactivity': 0}
        args.fixed_collectors = []
        args.autodetect = False

        return args

    def test_get_config(self):
        obj = self.object_factory.get_config()

        assert obj.__name__ == 'Config'

    def test_create_pipeline(self):
        obj = self.object_factory.create_pipeline()

        assert obj.__class__.__name__ == 'Pipeline'

    def test_create_value_data_factory(self, args):
        config = self.object_factory.get_config()

        obj = self.object_factory.create_value_data_factory(args, config)

        assert obj.__class__.__name__ == 'ValueDataFactory'

    def test_create_args_builder(self):
        obj = self.object_factory.create_args_builder(None, None)

        assert obj.__class__.__name__ == 'ArgsBuilder'

    def test_create_target_parser(self, args):
        obj = self.object_factory.create_target_parser(args, None, None)

        assert obj.__class__.__name__ == 'TargetParser'

    def test_create_dns_resolver(self, args):
        obj = self.object_factory.create_dns_resolver(args)

        assert obj.__class__.__name__ == 'DnsResolveRequester'

    def test_create_collectors(self, args):
        obj = self.object_factory.create_collectors(args, None)

        assert isinstance(obj, dict)

    def test_create_rdap_collector(self, args):
        obj = self.object_factory.create_rdap_collector(args)

        assert obj.__class__.__name__ == 'RdapCollector'

    def test_create_dnstxt_collector(self, args):
        obj = self.object_factory.create_dnstxt_collector(None, args)

        assert obj.__class__.__name__ == 'DnsTxtCollector'

    def test_create_ipinfo_collector(self, args):
        obj = self.object_factory.create_ipinfo_collector(args)

        assert obj.__class__.__name__ == 'IpInfoCollector'

    def test_create_self_collector(self, args):
        obj = self.object_factory.create_self_collector(args, None, None)

        assert obj.__class__.__name__ == 'SelfCollector'

    def test_create_dns_reverse_collector(self, args):
        obj = self.object_factory.create_dns_reverse_collector(None, args)

        assert obj.__class__.__name__ == 'DnsReverseCollector'

    def test_create_reactivities(self, args):
        obj = self.object_factory.create_reactivities(args)

        assert isinstance(obj, list)

    def test_create_server_reactivity(self, args):
        obj = self.object_factory.create_server_reactivity(args)

        assert obj.__class__.__name__ == 'ServerReactivity'

    def test_create_http(self, args):
        obj = self.object_factory.create_http(args)

        assert obj.__class__.__name__ == 'HttpRequester'

    def test_create_icmp_collector(self, args):
        obj = self.object_factory.create_icmp_collector(None, args)

        assert obj.__class__.__name__ == 'ICMPCollector'

    def test_create_tcp_collector(self, args):
        obj = self.object_factory.create_tcp_collector(None, args)

        assert obj.__class__.__name__ == 'TCPCollector'

    def test_create_udp_collector(self, args):
        obj = self.object_factory.create_udp_collector(None, args)

        assert obj.__class__.__name__ == 'UDPCollector'

    def test_create_http_collector(self, args):
        obj = self.object_factory.create_http_collector(None, args)

        assert obj.__class__.__name__ == 'HttpCollector'

    def test_create_serializer_line(self, args):
        args.json = False

        obj = self.object_factory.create_serializer(args)

        assert obj.__class__.__name__ == 'LineSerializer'

    def test_create_serializer_json(self, args):
        args.json = True

        obj = self.object_factory.create_serializer(args)

        assert obj.__class__.__name__ == 'JsonSerializer'
