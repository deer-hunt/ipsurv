import pytest

from ipsurv.core.target_groups import TargetGroups
from ipsurv.core.entity import TargetGroup
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData, Target


class TestTargetGroups:
    @pytest.fixture(autouse=True)
    def setup(self, args):

        pipeline = Pipeline()

        self.target_groups = TargetGroups(args, pipeline)

    @pytest.fixture
    def args(self, mocker):
        args = mocker.Mock()
        args.fixed_format_params = []
        args.fixed_timeout = {'dns': 0, 'http': 0, 'reactivity': 0}
        args.fixed_collectors = []
        args.autodetect = False

        return args

    def test_put_group(self, args):
        data = ValueData({})

        target = Target()
        target.ip = '192.168.1.10'
        target.identifier = '192.168.1.10'

        group_type = '8'

        pipeline = Pipeline()

        targetGroups = TargetGroups(args, pipeline)
        group = targetGroups.put_group(data, target, group_type, None)

        assert group.value == '192.0.0.1'
        assert data.get('group') == '192.0.0.1'
        assert group.begin_int == 3221225473
        assert data.get('group_found') is True

    def test_find_group(self, args):
        data = ValueData({})

        target = Target()
        target.ip = '192.168.1.10'
        target.identifier = '192.168.1.10'

        group_type = '8'

        pipeline = Pipeline()

        targetGroups = TargetGroups(args, pipeline)
        targetGroups.put_group(data, target, group_type, None)

        target.ip = '192.168.1.100'
        target.identifier = '192.168.1.100'
        target.identifier_int = 3221291364

        group = targetGroups.find_group(data, target)

        assert group is not None

    def test_create_group_by_identifier(self, args):
        targetGroups = TargetGroups(args, Pipeline())

        target = Target()
        target.ip = '192.168.1.10'
        target.identifier = '192.168.1.10'

        group = targetGroups._create_group_by_identifier(target, '8', None)

        assert group.begin_int == 3221225473
        assert group.end_int == 3238002686

        group = targetGroups._create_group_by_identifier(target, '255.0.0.0', None)

        assert group.begin_int == 3221225473
        assert group.end_int == 3238002686

        group = targetGroups._create_group_by_identifier(target, 'network', '192.168.1.1/24')

        assert group.begin_int == 3232235777
        assert group.end_int == 3232236030

    def test_find_indexes(self, args):
        targetGroups = TargetGroups(args, Pipeline())

        targetGroups.group_indexes = [100, 200, 299, 310, 350, 400]
        targetGroups.groups = [None, None, None, (300, 310, '300'), None, None]

        group = targetGroups._find_indexes(300)

        assert group is not None

        targetGroups.group_indexes = [10, 200, 280, 305, 350, 400]
        targetGroups.groups = [None, None, None, (300, 310, '300'), None, None]

        group = targetGroups._find_indexes(300)

        assert group is not None

    def test_add_indexes(self, args):
        targetGroups = TargetGroups(args, Pipeline())

        group = TargetGroup(100, 300, '300')

        targetGroups._add_indexes(group)

        assert targetGroups.group_indexes[0] == 300
        assert len(targetGroups.groups) == 1
