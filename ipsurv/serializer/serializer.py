from abc import ABC, abstractmethod

from ipsurv.configs import Constant
from ipsurv.core.entity import Target
from ipsurv.core.entity import ValueData


class Serializer(ABC):
    """
    Description:
    https://deer-hunt.github.io/ipsurv/pages/program_architecture_classes.html#serializer
    """

    def __init__(self, args):
        self.format = args.fixed_format
        self.delimiter = args.fixed_delimiter
        self.alt_delimiter = args.alt_delimiter
        self.enclose = args.fixed_enclose

        self.survey_mode = None

    def set_survey_mode(self, survey_mode):
        """
        :param survey_mode:
        :type survey_mode: int
        """

        self.survey_mode = survey_mode

    def set_delimiter(self, delimiter):
        """
        :param delimiter:
        :type delimiter: str
        """

        self.delimiter = delimiter

    def output_begin(self, mode, args, rows):
        """
        :param data:
        :type data: ValueData
        :param original:
        :type original: str
        """

        pass

    def create_labels(self, columns, mode):
        """
        :param columns:
        :type columns: dict
        :param mode:
        :type mode: int
        :rtype: dict
        """

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
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :param args:
        :type args: argparse.Namespace
        :param skip:
        :type skip: bool
        """

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
        """
        :param data:
        :type data: ValueData
        :param target:
        :type target: Target
        :rtype: object
        """

        if not data.header and target.identified:
            self.transform(data)

        data.map(self.filter_value)

        return self.build_row(data)

    def transform(self, data):
        """
        :param data:
        :type data: ValueData
        """

        data.update('ip_type', lambda v: 'PRIVATE' if v == Constant.IP_TYPE_PRIVATE else 'PUBLIC')

    def filter_value(self, v):
        return v

    @abstractmethod
    def build_row(self, data):  # pragma: no cover
        """
        :param data:
        :type data: ValueData
        :rtype: object
        """

        return None

    @abstractmethod
    def build_error(self, error):  # pragma: no cover
        return None

    def output_result(self, v):
        self.output(v)

    def output(self, v):
        print(v, flush=True)

    def output_complete(self, mode, args, rows):
        """
        :param mode:
        :type mode: int
        :param args:
        :type args: argparse.Namespace
        :param rows:
        :type rows: list
        """

        pass

    def transform_key_labels(self, data, mode):
        """
        :param data:
        :type data: ValueData
        :param mode:
        :type mode: int
        """

        pass

    def output_message(self, msg):
        pass

    def output_item(self, data):
        """
        :param data:
        :type data: ValueData
        """

        pass
