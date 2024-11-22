import logging
import time
from abc import ABC, abstractmethod

from ipsurv.core.entity import Target, ValueData
from ipsurv.util.sys_util import System


class DataCollector(ABC):
    def __init__(self, requester, args):
        self.requester = requester

    def initialize(self):
        pass

    @abstractmethod
    def get_name(self):  # pragma: no cover
        return ''

    def request(self, target):
        # type: (Target) -> tuple

        name = self.get_name()

        logging.info('REQUEST ' + name + '...')

        begin_time = time.time()

        success = False
        response = {}

        try:
            (success, response) = self.request_data(target)
        except Exception as e:
            error_name = name + ' ERROR'
            error = str(e)
            response['error'] = error

            if System.get_log_level() == logging.INFO:
                logging.log(logging.INFO, error_name + ':' + error)
            else:
                logging.log(logging.DEBUG, error_name, exc_info=True)

        response_time = self._get_measure_time(begin_time)

        if System.is_logging():
            System.output_data(name + '_DATA', response, logging.DEBUG)

            logging.log(logging.INFO, name + ':' + ('OK' if success else 'NG'))
            logging.log(logging.INFO, name + '_TIME(ms):' + str(response_time))

        return success, response, response_time

    @abstractmethod
    def request_data(self, target):  # pragma: no cover
        # type: (Target) -> tuple

        return None, None

    @abstractmethod
    def get_requires(self):  # pragma: no cover
        return []

    def get_cidr(self, response):
        return None

    @abstractmethod
    def build_data(self, target, data, success, response, response_time):  # pragma: no cover
        # type: (Target, ValueData, bool, dict, float) -> None

        pass

    def _append_error(self, data, response):
        error = response.get('error')

        if error:
            data.get('errors').append(error)

    def put(self, data, response, key, key2=None):
        key2 = key if key2 is None else key2

        v = response[key] if key in response else None

        data.set(key2, v)

    def fill(self, data, response, key, key2=None):
        key2 = key if key2 is None else key2

        if not data.get(key2):
            v = response[key] if key in response else None

            data.set(key2, v)

    def _get_measure_time(self, begin_time, digit=1):
        end_time = time.time()

        response_time = end_time - begin_time

        response_time = round(response_time * 1000, digit)

        return response_time
