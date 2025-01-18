import pytest
import os


if os.name == 'posix':
    from unittest.mock import patch
    from ipscap.core.object_factory import ObjectFactory
    from ipscap.ipscap_cmd import IpsCapCmd
    import re
    import sys
    import io
    import os
    import logging

    class TestIpscapCmd:
        @pytest.fixture
        def ipscap_cmd(self, mocker):
            factory = ObjectFactory()

            ipscap_cmd = IpsCapCmd(factory)

            return ipscap_cmd

        def test_version(self, capsys, monkeypatch, ipscap_cmd):
            monkeypatch.setattr(sys, 'argv', ['test.py', '--version'])
            monkeypatch.setattr(os, '_exit', lambda v: 0)

            monkeypatch.setattr(ipscap_cmd, 'dispatch', lambda v: 0)

            ipscap_cmd.run()

            captured = capsys.readouterr()

            assert re.search(r'(Permission|ipscap)', captured.out)
