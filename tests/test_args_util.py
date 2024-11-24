import pytest

from ipsurv.util.args_util import ArgsHelper, StdinLoader
import re
import io


class TestArgValidator:
    def test_init_logging(self):
        assert ArgsHelper.init_logging(1, None) is None
        assert ArgsHelper.init_logging(2, None) is None


class TestStdinLoader:
    def test_read_stdin(self, monkeypatch):
        monkeypatch.setattr('select.select', lambda a, b, c, d: ("1\n4\n", None, None))
        monkeypatch.setattr('sys.stdin', io.StringIO("1\n4\n"))
        monkeypatch.setattr('sys.stdin.fileno', lambda: 0)

        lines = StdinLoader.read_stdin()

        assert len(lines) == 2

    def test_load_env(self, monkeypatch):
        monkeypatch.setenv("TEST1", '{"abc": 1}')

        env = StdinLoader.load_env('TEST1')

        assert env['abc'] == 1

        monkeypatch.setenv("TEST1", '{"abc": 1')

        env = StdinLoader.load_env('TEST1')

        assert len(env) == 0
