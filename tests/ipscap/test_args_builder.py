import pytest
import sys
import os
from ipscap.util.raw_socket_entity import IPHeader


if os.name == 'posix':
    from ipscap.service.args_builder import ArgsBuilder
    from ipscap.util.evaluation_parser import EvaluationParser
    from ipscap.core.pipeline import Pipeline
    from ipscap.configs import Config

    class TestArgsBuilder:
        @pytest.fixture
        def args(self, mocker):
            args = mocker.Mock()

            args.timeout = None
            args.fixed_output = 'TEXT'
            args.stat_mode = 2
            args.stat_group = False
            args.fixed_protocols = [IPHeader.PROTOCOL_TCP]

            return args

        @pytest.fixture
        def args_builder(self):
            pipeline = Pipeline()

            return ArgsBuilder(Config, pipeline, EvaluationParser())

        def test_parse(self, args_builder, monkeypatch):
            monkeypatch.setattr(sys, 'argv', ['ipscap'])

            args, parser, ev_parser = args_builder.parse()

            assert args.verbose == 0
            assert parser is not None

        def test_create_bottom_desc(self, args_builder):
            desc = args_builder._create_bottom_desc()
            assert desc is not None

        def test_assign_shorten_option(self, args_builder, args):
            args.exclude_ssh = True
            args.condition = ''

            args_builder._assign_shorten_option(args)

            assert 'port!=' in args.condition

        def test_fix_ips(self, args_builder, args):
            args.ip = '192.168.1.1,192.168.1.2'
            fixed_ips = args_builder._fix_ips(args)

            assert fixed_ips == ['192.168.1.1', '192.168.1.2']

        def test_fix_ports(self, args_builder, args):
            args.port = '80, 443, 8080'
            fixed_ports = args_builder._fix_ports(args)

            assert fixed_ports == [80, 443, 8080]

        def test_fix_protocols(self, args_builder, args):
            args.protocol = 'TCP, UDP'

            fixed_protocols = args_builder.fix_protocols(args)

            assert 6 in fixed_protocols
            assert 17 in fixed_protocols

            with pytest.raises(Exception, match='Unknown protocol'):
                args.protocol = 'UNKNOWN'
                args_builder.fix_protocols(args)

        def test_fix_output(self, args_builder, args):
            args.output = 'TEXT'
            fixed_output = args_builder._fix_output(args)
            assert fixed_output == 'TEXT'

            args.output = 'BINARY'
            fixed_output = args_builder._fix_output(args)
            assert fixed_output == 'BINARY'

            args.output = 'INVALID'
            with pytest.raises(Exception, match='Unknown output'):
                args_builder._fix_output(args)

        def test_parse_condition(self, args, args_builder):
            args.condition = 'port=80'

            args_builder._parse_condition(args)

            assert args_builder.ev_parser.evaluate('port', 80)

        def test_has_filters(self, args_builder, args):
            args.find = 'value'
            assert args_builder._has_filters(args) is True
