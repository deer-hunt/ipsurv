import re

from ipsurv.core.entity import ValueData, StoreBase
from ipsurv.serializer.serializer import Serializer
from ipsurv.util.sys_util import AppException


class LineSerializer(Serializer):
    def transform(self, data):
        super().transform(data)

        self.transform_status(data)

    def transform_status(self, data):
        # type: (ValueData) -> None

        if data.get('in_range') is not None:
            data.update('in_range', lambda v: 'RANGE_OK' if v else 'RANGE_NG')

        if data.get('icmp') is not None:
            data.update('icmp', lambda v: 'ICMP_OK' if v else 'ICMP_NG')

        if data.get('tcp') is not None:
            data.update('tcp', lambda v: 'TCP_OK' if v else 'TCP_NG')

        if data.get('udp') is not None:
            data.update('udp', lambda v: 'UDP_OK' if v else 'UDP_NG')

        if data.get('http') is not None:
            data.update('http', lambda v: 'HTTP_OK' if v else 'HTTP_NG')

        if data.get('http_h2') is not None:
            data.update('http_h2', lambda v: 'HTTP2' if v == 1 else 'HTTP1' if v == 0 else 'UNKNOWN')

    def filter_value(self, v):
        if v is not None:
            if isinstance(v, StoreBase):
                return v
            elif isinstance(v, bool):
                v = self._get_bool_status(v)

            v = str(v)

            if self.alt_delimiter and not self.enclose:
                delimiter = re.escape(self.delimiter)
                v = re.sub(delimiter, self.alt_delimiter, v)
        else:
            v = ''

        return self._append_enclose(v)

    def _append_enclose(self, v):
        enclose = self.enclose

        v = re.sub(re.escape(enclose), enclose + enclose, v)

        return enclose + v + enclose

    def _get_bool_status(self, v):
        return 'OK' if v else 'NG'

    def build_row(self, data):
        values = data.get_data()

        try:
            line = self.format.format(**values)
        except Exception:
            raise AppException('Format error.')

        return line

    def build_error(self, error):
        line = 'ERROR' + self.delimiter + error

        return line

    def output(self, v):
        print(v)

    def transform_key_labels(self, data, mode):
        # type: (ValueData, int) -> None

        values = data.get_data()

        item = {}

        for k, v in values.items():
            k = self.get_label(k, mode)
            item[k] = v

        data.set_data(item)

    def output_message(self, msg):
        self.output(msg)

    def output_item(self, data):
        values = data.get_data()

        for name, value in values.items():
            self.output(name + self.delimiter + str(value))

        self.output('')
