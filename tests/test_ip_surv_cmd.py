import pytest
from unittest.mock import patch
from ipsurv.core.object_factory import ObjectFactory
from ipsurv.ip_surv_cmd import IpSurvCmd
from ipsurv.data_collector.self_collector import SelfCollector
from ipsurv.util.args_util import StdinLoader
import re
import sys
import io
import os
import logging


class TestIpSurvCmd:
    @pytest.fixture
    def ip_surv_cmd(self, mocker):
        factory = ObjectFactory()

        ip_surv_cmd = IpSurvCmd(factory)

        return ip_surv_cmd

    def test_ip_surv_cmd(self, capsys, monkeypatch, ip_surv_cmd):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py'])

        with patch('ipsurv.util.args_util.StdinLoader.read_stdin', return_value=[]):
            ip_surv_cmd.run()

            captured = capsys.readouterr()

            assert re.search(r'No target data', captured.out)

    def test_version(self, capsys, monkeypatch, ip_surv_cmd):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py', '--version'])
        monkeypatch.setattr(os, '_exit', lambda v: 0)

        with patch('ipsurv.util.args_util.StdinLoader.read_stdin', return_value=[]):
            ip_surv_cmd.run()

            captured = capsys.readouterr()

            assert re.search(r'ipsurv', captured.out)

    def test_options(self, capsys, monkeypatch, ip_surv_cmd, caplog):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py', '--headers=2', '--begin=2', '--verbose=3', '--group=8', '--icmp=1', '--skip_duplicate=1'])
        monkeypatch.setattr(os, '_exit', lambda v: 0)

        with patch('ipsurv.util.args_util.StdinLoader.read_stdin', return_value=['192.168.1.100', '192.168.1.101', '192.168.1.102', 'sample']):
            with caplog.at_level(logging.INFO):
                ip_surv_cmd.run()

                captured = capsys.readouterr()

                assert re.search(r'ILLEGAL_FORMAT', captured.out)

    def test_ips(self, capsys, monkeypatch, ip_surv_cmd):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py', '192.168.1.100'])
        monkeypatch.setattr(os, '_exit', lambda v: 0)

        with patch('ipsurv.util.args_util.StdinLoader.read_stdin', return_value=[]):
            ip_surv_cmd.run()

            captured = capsys.readouterr()

            assert re.search(r'192.168.1.100', captured.out)

    def test_self(self, capsys, monkeypatch, ip_surv_cmd):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py', 'self'])
        monkeypatch.setattr(os, '_exit', lambda v: 0)
        monkeypatch.setattr(SelfCollector, 'request_data', lambda target: True, {'ip': None})

        with patch('ipsurv.util.args_util.StdinLoader.read_stdin', return_value=[]):
            ip_surv_cmd.run()

            captured = capsys.readouterr()

            assert re.search(r'Data not found', captured.out)
