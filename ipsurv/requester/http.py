import logging
import re
import socket
import ssl
import urllib.parse
import urllib.request
import urllib.error

from ipsurv.requester.requester import Requester


class HttpRequester(Requester):
    def __init__(self, timeout=None):
        super().__init__(timeout)

        self.host = None

        self.headers = {
            'User-Agent': 'Requester',
            'Accept-Language': 'en-US,en;q=0.5'
        }

    def set_headers(self, headers):
        self.headers = headers

    def request(self, url, encoding='utf-8'):
        res, body = self.request_http(url)

        success = False
        response = {}

        if res.status != 0:
            response = {
                'http_status': res.status,
                'http_size': len(body),
                'body': body.decode(encoding)
            }
            success = True
        else:
            raise self._http_exception(res, body)

        return success, response

    def request_http(self, url):
        url = self._create_url(url)

        logging.info('URL:' + url)

        req = urllib.request.Request(url)

        for name, value in self.headers.items():
            req.add_header(name, value)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                body = res.read()
        except urllib.error.URLError as e:
            res = e
            body = res.read()

        return res, body

    def request_alpn_h2(self, url, port=443):
        url = self._create_url(url)

        parsed_url = urllib.parse.urlparse(url)

        host = parsed_url.netloc

        context = ssl.create_default_context()

        context.set_alpn_protocols(['h2'])

        try:
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    negotiated_protocol = ssock.selected_alpn_protocol()
                    if negotiated_protocol == 'h2':
                        return 1
        except Exception:
            return -1

        return 0

    def _create_url(self, url):
        if not re.search(r'^https?:\/\/', url, flags=re.IGNORECASE):
            url = 'http://' + url
        elif re.search(r'^\/\/', url, flags=re.IGNORECASE):
            url = 'http:' + url

        return url
