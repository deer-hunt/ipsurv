from ipscap.util.evaluation_parser import EvaluationParser, EvaluationParserException
import pytest
import re


class TestEvParser:
    @pytest.fixture(autouse=True)
    def setup(self):
        pass

    def test_evaluate1(self):
        ev_parser = EvaluationParser()

        ev_parser.initialize({
            'a': {'type': int},
            'b': {'type': int, 'single': True},
            'c': {'type': int},
            'd': {'type': lambda v: v.upper()},
            'e': {'type': float},
            'f': {'type': lambda v: v.upper(), 'types': lambda vals: '-'.join(vals), 'list': True},
            'g': {'type': int, 'single': True},
            'h': {'type': int},
            'z': {'type': int}
        })

        value = 'a>= 1; a<6 ; b=8; c=80,443; d=tcp; e=4.5; f=X,Y,z ; g=-1; g=-2; g=-3;h != 9 ; ;z>=5; z<7'

        ev_parser.parse(value)

        assert ev_parser.evaluate('a', 1)
        assert ev_parser.evaluate('a', 5)
        assert ev_parser.evaluate('a', 7) is False
        assert ev_parser.evaluate('c', 443)
        assert ev_parser.evaluate('d', 'TCP')
        assert ev_parser.evaluate('e', 4.5)
        assert ev_parser.evaluate('f', 'X-Y-Z')
        assert ev_parser.evaluate('g', -3)
        assert ev_parser.evaluate('h', 8)
        assert ev_parser.evaluate('z', 999) is False

    def test_method(self):
        ev_parser = EvaluationParser()

        ev_parser.initialize({
            'a': {'type': int},
            'b': {'type': int, 'single': True},
            'c': {'type': int},
        })

        value = 'a= 1,2,3 ; b=8; c=80,443;'

        ev_parser.parse(value)

        assert ev_parser.get_value('a') == [1, 2, 3]
        assert ev_parser.get_value('b') == 8
        assert ev_parser.assigned('d') is False
        assert ev_parser.is_empty() is False
        assert ev_parser.get_rule('a') is not None

        items = ev_parser.get_items()

        assert items['a'][0]['op'] == 1

    def test_error(self):
        ev_parser = EvaluationParser()

        ev_parser.initialize({
            'a': {'type': int}
        })

        with pytest.raises(EvaluationParserException):
            ev_parser.parse('e1=8')

        with pytest.raises(EvaluationParserException):
            ev_parser.parse('a>= 1 a< ; ')
