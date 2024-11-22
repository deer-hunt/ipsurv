import pytest

from ipsurv.core.entity import Target, HeaderTarget, TargetGroup
from ipsurv.core.entity import ValueData, ValueDataFactory
import re


class TestTarget:
    def test(self, mocker):
        target = Target('test_target')
        target.identifier = 'identifier'

        assert target.raw == 'test_target'
        assert str(target) == 'identifier'


class TestHeaderTarget:
    def test(self, mocker):
        target = HeaderTarget('test_target')
        target.identifier = 'identifier'

        assert target.xyz == 'xyz'
        assert str(target) == 'target'

    def test_dump(self, mocker, capfd):
        target = HeaderTarget('test_target')
        target.identifier = 'identifier'

        target.dump()

        captured = capfd.readouterr()

        assert re.search(r'identifier', captured.out)


class TestTargetGroup:
    def test(self, mocker):
        target = TargetGroup(1, 2, 'abc')

        assert target.begin_int == 1
        assert target.value == 'abc'

        assert target.get_values()['begin_int'] == 1

    def test_dump(self, mocker, capfd):
        target = TargetGroup(1, 2, 'abc')
        target.dump()

        captured = capfd.readouterr()

        assert re.search(r'begin_int', captured.out)


class TestValueData:
    def test(self, mocker):
        data = ValueData({'a': 1, 'b': 2, 'c': 3, 'e': 99})

        data.update('c', lambda v: v + 1)
        data.set('d', 4)
        data.delete('e')

        assert data.get('a') == 1
        assert data.get('b') == 2
        assert data.get('c') == 4
        assert data.get('d') == 4
        assert data.get('e') is None

        data.set_header(True)

        assert data.header is True

    def test_map(self, mocker):
        data = ValueData({'a': 1, 'b': 2, 'c': 3, 'e': 99})

        data.map(lambda v: v + 1)

        assert data.get('a') == 2

    def test_data(self, mocker):
        data = ValueData({})

        data.set_data({'a': 1, 'b': 2, 'c': 3, 'e': 99})

        assert data.get('a') == 1
        assert data.get('b') == 2
        assert data.get('c') == 3

    def test_get_values(self, mocker):
        data = ValueData({'a': 1, 'b': 2, 'c': 3})

        values = data.get_values()

        assert values['a'] == 1

    def test_dump(self, mocker, capfd):
        data = ValueData({'a': 1234})
        data.dump()

        captured = capfd.readouterr()

        assert re.search(r'1234', captured.out)


class TestValueDataFactory:
    def test(self, mocker):
        factory = ValueDataFactory({'a': 1, 'b': 2, 'c': 3, 'd': 5}, ['a', 'b', 'c', 'e'])

        data = factory.create()

        assert data.get('a') == 1
        assert data.get('b') == 2
        assert data.get('c') == 3
        assert data.get('e') is None

    def test_build(self, mocker):
        factory = ValueDataFactory({'a': 1, 'b': 2, 'c': 3, 'd': 5}, ['a', 'b', 'c', 'e'])

        assert type(factory.build({})) == ValueData
