import pytest
import sys

if sys.platform.startswith('win'):
    pytest.mark.skip('Skipping Windows')

from ipscap.core.pipeline import Pipeline


class TestPipeline:
    @pytest.fixture
    def mock_config(self, mocker):
        return mocker.Mock()

    @pytest.fixture(autouse=True)
    def setup(self):
        self.pipeline = Pipeline()
        self.pipeline.initialize(None)

    def test_initialize(self):
        self.pipeline.initialize(None)
        assert self.pipeline.config is None

    def test_init_configure(self):
        assert self.pipeline.init_configure({}) is None

    def test_pass_eth_ips(self):
        assert self.pipeline.pass_eth_ips(None) is None

    def test_pre_recieve_loop(self):
        assert self.pipeline.pre_recieve_loop(None, None) is None

    def test_pass_eth_header(self):
        assert self.pipeline.pass_eth_header(None, None) is None

    def test_pass_ip_header(self):
        assert self.pipeline.pass_ip_header(None, None) is None

    def test_pass_header_parser(self):
        assert self.pipeline.pass_header_parser(None, None) is None

    def test_pass_protocol_header(self):
        assert self.pipeline.pass_protocol_header(None, None) is None

    def test_verify_capture(self):
        assert self.pipeline.verify_capture(None, None, None, True) is True

    def test_process_captured_transfer(self):
        assert self.pipeline.process_captured_transfer(None, None, 1) is None

    def test_complete(self):
        assert self.pipeline.complete(None) is None
