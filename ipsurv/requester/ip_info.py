import json
import logging
import re

from ipsurv.requester.requester import Requester


class IpInfoRequester(Requester):
    """
    :param timeout:
    :type timeout: float
    :param token:
    :type token: str

    Description:
    https://deer-hunt.github.io/ipsurv/pages/program_architecture_classes.html#requester
    """

    def __init__(self, timeout=None, token=None):
        super().__init__(timeout)

        self.host = 'ipinfo.io'
        self.token = token

        self.headers = {
            'User-Agent': 'Requester',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    def set_headers(self, headers):
        self.headers = headers

    def request(self, ip):
        res, body = self.request_ip(ip)

        success = False
        response = {}

        if res.status == 200:
            response = json.loads(body)

            response = self._fill_data(response)

            success = True
        else:
            raise self._http_exception(res, body)

        return success, response

    def _fill_data(self, response):
        if response.get('org') is not None:
            match = re.search(r'^(AS\d+)\s(.+)$', response.get('org'))
            response['asn'] = match.group(1)
            response['org'] = match.group(2)

        return response

    def request_ip(self, ip):
        if not ip:
            path = '/json?'
        else:
            path = '/' + ip + '/json?'

        if self.token:
            path += 'token=' + self.token

        url = 'https://' + self.host + path
        logging.info('IPINFO_URL:' + url)

        conn = self._create_http_connection(self.host)

        try:
            conn.request('GET', path, headers=self.headers)

            res = conn.getresponse()

            body = res.read()
        except Exception as e:
            raise e
        finally:
            conn.close()

        return res, body
