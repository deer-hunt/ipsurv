from abc import ABC, abstractmethod

from ipsurv.configs import Constant
from ipsurv.core.entity import Target
from ipsurv.core.entity import ValueData

import re


class Serializer(ABC):
    def __init__(self, args):
        self.format = args.fixed_format
        self.delimiter = args.fixed_delimiter
        self.alt_delimiter = args.alt_delimiter
        self.enclose = args.fixed_enclose

        self.survey_mode = None

    def set_survey_mode(self, survey_mode):
        self.survey_mode = survey_mode

    def set_delimiter(self, delimiter):
        self.delimiter = delimiter

    def output_begin(self, mode, args, rows):
        pass

    def create_labels(self, columns, mode):
        labels = {}

        for v in columns:
            labels[v] = self.get_label(v, mode)

        return labels

    def get_label(self, v, mode):
        if mode == Constant.STR_LOWER:
            return v
        elif mode == Constant.STR_PASCAL:
            ts = v.split('_')
            return ts[0].capitalize() + ''.join(w.capitalize() for w in ts[1:])

        return v.upper()

    def set_status(self, data, target, args, skip):
        # type: (ValueData, Target, object, bool) -> None
        if target.status == Constant.STATUS_EXIST:
            if not skip:
                if len(data.get('requests')) > 0:
                    status = 'OK' if data.get('success') else 'NG'
                else:
                    status = '-'
            else:
                status = 'SKIP'

            if args.group:
                group_status = 'FOUND' if data.get('group_found') else 'NEW'
            else:
                group_status = '-'
        else:
            status = target.status
            group_status = '-'

        data.set('status', status)
        data.set('group_status', group_status)

    def build(self, data, target):
        # type: (ValueData, Target) -> object

        if not data.header and target.identified:
            self.transform(data)

        data.map(self.filter_value)

        return self.build_row(data)

    def transform(self, data):
        # type: (ValueData) -> None

        data.update('ip_type', lambda v: 'PRIVATE' if v == Constant.IP_TYPE_PRIVATE else 'PUBLIC')

    def filter_value(self, v):
        return v

    @abstractmethod
    def build_row(self, data):  # pragma: no cover
        # type: (ValueData) -> object
        return None

    @abstractmethod
    def build_error(self, error):  # pragma: no cover
        return None

    def output_result(self, v):
        self.output(v)

    def output(self, v):
        print(v)

    def output_complete(self, mode, args, rows):
        pass

    def transform_key_labels(self, data, mode):
        pass

    def output_message(self, msg):
        pass

    def output_item(self, data):
        # type: (ValueData) -> None
        pass
