import pytest

from ipscap.core.object_factory import ObjectFactory


class TestObjectFactory:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.object_factory = ObjectFactory()

    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()

        return args

    def test_get_config(self):
        obj = self.object_factory.get_config()

        assert obj.__name__ == 'Config'

    def test_create_pipeline(self):
        obj = self.object_factory.create_pipeline()

        assert obj.__class__.__name__ == 'Pipeline'

    def test_create_args_builder(self):
        obj = self.object_factory.create_args_builder(None, None)

        assert obj.__class__.__name__ == 'ArgsBuilder'

    def test_create_eth_socket(self):
        obj = self.object_factory.create_eth_socket()
        assert obj.__class__.__name__ == 'EthSocket'

    def test_create_ip_header_parser(self):
        obj = self.object_factory.create_ip_header_parser()
        assert obj.__class__.__name__ == 'IPHeaderParser'

    def test_create_packet_filter(self, mocker):
        evaluation_parser = mocker.Mock()
        obj = self.object_factory.create_packet_filter(evaluation_parser)
        assert obj.__class__.__name__ == 'PacketFilter'

    def test_create_transfer_store(self):
        obj = self.object_factory.create_transfer_store()
        assert obj.__class__.__name__ == 'TransferStore'

    def test_create_dumpfile(self):
        obj = self.object_factory.create_dumpfile()
        assert obj.__class__.__name__ == 'DumpFile'

    def test_create_view_helper(self):
        obj = self.object_factory.create_view_helper()
        assert obj.__class__.__name__ == 'ViewHelper'

    def test_create_icmp_protocol_service(self):
        obj = self.object_factory.create_icmp_protocol_service()
        assert obj.__class__.__name__ == 'ICMPProtocolService'

    def test_create_tcp_protocol_service(self):
        obj = self.object_factory.create_tcp_protocol_service()
        assert obj.__class__.__name__ == 'TCPProtocolService'

    def test_create_udp_protocol_service(self):
        obj = self.object_factory.create_udp_protocol_service()
        assert obj.__class__.__name__ == 'UDPProtocolService'
