import pytest

from ipsurv.configure.args_builder import ArgsBuilder
from ipsurv.core.pipeline import Pipeline
from ipsurv.configs import Config
from ipsurv.core.entity import Target, ValueData

import argparse
import re
import sys
import logging


class TestArgsBuilder:
    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.format = None
        args.delimiter = ','
        args.fixed_delimiter = ','

        return args

    @pytest.fixture
    def args_builder(self, mocker):
        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        return args_builder

    def test_parse(self, args, args_builder, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py'])

        args = args_builder.parse()

        assert args.timeout == '8.0'

    def test_init_args(self, args, args_builder, capfd):
        arguments = {
            'verbose': {'default': 3, 'type': int, 'help': ''},
            'log': {'default': 'abc.log', 'type': str, 'help': ''},
        }

        args_builder.init_args(arguments)

        captured = capfd.readouterr()

        assert re.search(r'Current:\s*3.+DEBUG', captured.out)

    def test_build_args(self, args, mocker, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['ipsurv.py', '--json=1', '--timeout=5'])

        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        parent_parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parent_parser.parse_known_args()

        arguments = Config.APP_ARGUMENTS

        env_args = {}
        env_conf = {}

        args = args_builder.build_args(parent_parser, arguments, env_args, env_conf)

        assert args.format == 'default'
        assert 'original' in args.fixed_format_params
        assert 'rdap' in args.fixed_collectors
        assert args.resolve is True

    def test_prepare_arguments(self, args_builder):
        parser = argparse.ArgumentParser(add_help=False, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        args_builder._prepare_arguments(parser, Config.APP_ARGUMENTS, {})

    def test_logging(self, args_builder, caplog):
        data = ValueData({})

        with caplog.at_level(logging.INFO):
            args_builder.logging(data, {}, {})

        print(caplog.text)

        assert re.search(r'ENV', caplog.text)

    def test_fix_validate_group(self, args):
        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        assert args_builder._validate_group('network') == 'network'
        assert args_builder._validate_group('192.168.1.100') == '192.168.1.100'

        with pytest.raises(argparse.ArgumentTypeError):
            args_builder._validate_group('ABC')

    def test_fix_delimiter(self, args):
        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        args.format = ''

        args.delimiter = ';'
        v = args_builder._fix_delimiter(args)
        assert v == ';'

        args.delimiter = None

        args.format = '1,2,3,4'
        v = args_builder._fix_delimiter(args)
        assert v == ','

        args.format = '1;2;3;4'
        v = args_builder._fix_delimiter(args)
        assert v == ';'

        args.format = '1\t2\t3\t4'
        v = args_builder._fix_delimiter(args)
        assert v == '\t'

    def test_fix_enclose(self, args):
        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        args.enclose = '1'
        v = args_builder._fix_enclose(args)
        assert v == '"'

        args.enclose = '2'
        v = args_builder._fix_enclose(args)
        assert v == "'"

        args.enclose = '3'
        v = args_builder._fix_enclose(args)
        assert v == '|'

    def test_fix_collectors(self, args):
        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        args.collect = 'rdap;dnstxt;ipinfo;dnsreverse;test'

        collectors = args_builder._fix_collectors(args)

        assert 'rdap' in collectors
        assert 'ipinfo' in collectors
        assert not ('test' in collectors)

    def test_notice(self, args, capfd):
        pipeline = Pipeline()

        args_builder = ArgsBuilder(Config, pipeline)

        args.json = True
        args.delimiter = True
        args.enclose = True

        args_builder._notice(args)

        captured = capfd.readouterr()

        assert re.search(r'option is ignored', captured.out)
