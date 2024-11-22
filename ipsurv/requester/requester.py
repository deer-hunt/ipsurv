import logging
from abc import ABC
import http.client


class Requester(ABC):
    def __init__(self, timeout=None):
        self.timeout = timeout
        self.host = None

    def get_host(self):
        return self.host

    def _create_http_connection(self, host, https=True):
        if https:
            conn = http.client.HTTPSConnection(host, timeout=self.timeout)
        else:
            conn = http.client.HTTPConnection(host, timeout=self.timeout)

        return conn

    def _http_exception(self, res, body):
        msg = 'Failure response.(Status:' + str(res.status) + ')'

        logging.log(logging.DEBUG, msg + '\n' + str(body, 'utf-8'))

        return http.client.HTTPException(msg)
