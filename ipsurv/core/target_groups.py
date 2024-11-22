import bisect
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import TargetGroup
from ipsurv.util.network_util import IpUtil


class TargetGroups:
    def __init__(self, args, pipeline):
        self.groups = []
        self.group_indexes = []

        self.pipeline = pipeline  # type: Pipeline

        self.ignore = True if args.group is None and not args.skip_duplicate else False

    def find_group(self, data, target):
        if self.ignore:
            return None

        group = self.pipeline.find_group(data, target)

        if group is None:
            identifier_int = self.pipeline.get_group_identify(data, target)

            group = self._find_indexes(identifier_int)

        if group is not None:
            data.set('group', group.value)
            data.set('group_int', group.begin_int)
            data.set('group_found', True)

        return group

    def put_group(self, data, target, group_type, cidr):
        if self.ignore:
            return None

        group = self.pipeline.create_group(data, target, group_type, cidr)

        if group is None:
            group = self._create_group_by_identifier(target, group_type, cidr)

        if group is not None:
            data.set('group', group.value)
            data.set('group_int', group.begin_int)
            data.set('group_found', True)

            self._add_indexes(group)

        return group

    def _create_group_by_identifier(self, target, group_type, cidr):
        end_int = None

        if group_type == 'network':
            if cidr is None:
                return None

            begin_int, end_int = IpUtil.get_network_range(cidr)
        elif group_type is None:
            begin_int = end_int = target.identifier_int
        else:
            begin_int, end_int = IpUtil.get_network_range(target.identifier + '/' + str(group_type))

        group = None

        if begin_int:
            value = IpUtil.get_ip_from_int(begin_int)
            group = TargetGroup(begin_int, end_int, value)

        return group

    def _find_indexes(self, identifier_int):
        found = None

        index = bisect.bisect_left(self.group_indexes, identifier_int)

        if index >= 0 and len(self.groups) > index:
            bucket = self.groups[index]

            (begin_int, end_int, group) = bucket

            if end_int is not None:
                if begin_int <= identifier_int and identifier_int <= end_int:
                    found = bucket
            else:
                if begin_int == identifier_int:
                    found = bucket

        group = None

        if found:
            (begin_int, end_int, value) = found

            group = TargetGroup(begin_int, end_int, value)

        return group

    def _add_indexes(self, group):
        group_int = group.end_int if group.end_int is not None else group.begin_int

        index = bisect.bisect_left(self.group_indexes, group_int)

        bucket = (group.begin_int, group.end_int, group.value)

        self.groups.insert(index, bucket)
        self.group_indexes.insert(index, group_int)
