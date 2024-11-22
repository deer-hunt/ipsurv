from collections import OrderedDict

from ipsurv.core.pipeline import Pipeline
from ipsurv.serializer.serializer import Serializer


class SurveySelf:
    def __init__(self, args, config, data_factory, collector, pipeline, serializer):
        self.config = config
        self.data_factory = data_factory
        self.collector = collector

        self.pipeline = pipeline  # type: Pipeline
        self.serializer = serializer  # type: Serializer

        serializer.set_delimiter(': ')

    def initialize(self):
        self.serializer.output_message(self.config.HEAD_MSG_SELF + '\n')

    def dispatch(self):
        data = self.data_factory.create()

        success = self._request(data)

        self._modify_orders(data)

        self._output_data(success, data)

    def _request(self, data):
        success, response, response_time = self.collector.request(None)

        self.collector.build_data(None, data, success, response, response_time)

        return success

    def _modify_orders(self, data):
        orders = ['ip', 'hostname', 'organization', 'country', 'city', 'region', 'postal', 'geo', 'timezone', 'local_ip', 'local_dns']

        values = data.get_data()

        data.set_data(OrderedDict((k, values[k]) for k in orders))

    def _output_data(self, success, data):
        if success:
            self.pipeline.output_result_self(data)
        else:
            msg = self.pipeline.build_error('Data not found or Error occurred.')

            self.pipeline.output_result(msg)
