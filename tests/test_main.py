import pytest
from unittest.mock import patch
from ipsurv.__main__ import main
import re
import sys
import io
import os


class TestMain:
    def test_main(self, capsys, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py'])

        with patch('ipsurv.util.args_util.StdinLoader.read_stdin', return_value=[]):
            main()

            captured = capsys.readouterr()

            assert re.search(r'No target data', captured.out)
