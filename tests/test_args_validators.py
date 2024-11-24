import pytest

from ipsurv.configure.args_validators import FormatValidator, TimeoutValidator
import re


class TestFormatValidator:

    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.format = None
        args.delimiter = ','
        args.fixed_delimiter = ','
        args.sequence = True
        args.add_ip = False

        return args

    def test_validator(self, args):
        profiles = {
            'ip': ['ip', 'ip2']
        }

        params = ['success', 'sequence', 'ip', 'ip2', 'identifier', 'test']

        validator = FormatValidator(profiles, params)

        args.format = '{ip}'
        args.ident = True

        format, params = validator.validate(args)

        assert format == '{sequence},{identifier},{ip}'
        assert 'ip' in params

        args.format = '<ip>'

        format, params = validator.validate(args)

        assert format == '{sequence},{identifier},{ip},{ip2}'
        assert 'ip2' in params

        args.format = '<ip>,{test}'

        format, params = validator.validate(args)

        assert format == '{sequence},{identifier},{ip},{ip2},{test}'
        assert 'test' in params

        format, params = validator._append_head(args, '{ip}', params)

        assert 'sequence' in params

        format, params = validator._create_by_profile(args, 'ip')

        assert 'ip' in params

    def test_create_by_params(self, args):
        profiles = {
            'ip': ['ip', 'ip2']
        }

        params = ['success', 'sequence', 'ip', 'ip2', 'identifier', 'test']

        validator = FormatValidator(profiles, params)

        format = validator._create_by_params(params, args)

        assert re.search(r'ip', format)

    def test_test_format(self, args):
        validator = FormatValidator(None, None)

        assert validator._test_format('{ip}', {'ip': 123}) is None

        with pytest.raises(Exception):
            validator._test_format('{ip2}', {'ip': 123})

    def test_misc(self, args):
        profiles = {
            'ip': ['ip', 'ip2']
        }

        params = ['success', 'sequence', 'ip', 'ip2', 'identifier', 'test']

        validator = FormatValidator(profiles, params)

        args.format = '{test1},<test2>'

        with pytest.raises(Exception):
            validator.validate(args)


class TestTimeoutValidator:
    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.timeout = None

        return args

    def test_validator(self, args):
        validator = TimeoutValidator()

        args.timeout = '8.1'

        timeout = validator.validate(args)

        assert timeout['dns'] == 8.1
        assert timeout['http'] == 8.1
        assert timeout['reactivity'] == 8.1

        args.timeout = '8;5;3'

        timeout = validator.validate(args)

        assert timeout['dns'] == 8
        assert timeout['http'] == 5
        assert timeout['reactivity'] == 3

        args.timeout = '1,5,2'

        timeout = validator.validate(args)

        assert timeout['dns'] == 1
        assert timeout['http'] == 5
        assert timeout['reactivity'] == 2

        args.timeout = '8;3'

        timeout = validator.validate(args)

        assert timeout['dns'] == 8
        assert timeout['http'] == 3
        assert timeout['reactivity'] == 8
