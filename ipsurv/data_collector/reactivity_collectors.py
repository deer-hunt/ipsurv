import logging

from ipsurv.data_collector.data_collector import DataCollector


class ICMPCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.server_reactivity.ServerReactivity
    :param args:
    :type args: argparse.Namespace
    """
    def get_name(self):
        return 'ICMP'

    def request_data(self, target, requires):
        logging.log(logging.INFO, 'ICMP ping(' + target.ip + ')...')

        success = self.requester.request_icmp(target.ip, count=1)

        return success, {}

    def get_requires(self):
        return ['icmp']

    def build_data(self, target, data, success, response, response_time):
        data.set('icmp', success)
        data.set('icmp_time', response_time)

        self._append_error(data, response)


class TCPCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.server_reactivity.ServerReactivity
    :param args:
    :type args: argparse.Namespace
    """
    def __init__(self, requester, args):
        super().__init__(requester, args)

        self.default_port = args.tcp if args.tcp != 1 else 80

    def get_name(self):
        return 'TCP'

    def request_data(self, target, requires):
        port = target.port if target.port is not None else self.default_port

        logging.log(logging.INFO, 'TCP connecting(' + target.ip + ':' + str(port) + ')...')

        success = self.requester.request_tcpport(target.ip, port)

        return success, {}

    def get_requires(self):
        return ['tcp']

    def build_data(self, target, data, success, response, response_time):
        data.set('tcp', success)
        data.set('tcp_time', response_time)

        self._append_error(data, response)


class UDPCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.server_reactivity.ServerReactivity
    :param args:
    :type args: argparse.Namespace
    """
    def __init__(self, requester, args):
        super().__init__(requester, args)

        self.default_port = args.udp if args.udp != 1 else 53

    def get_name(self):
        return 'UDP'

    def request_data(self, target, requires):
        port = target.port if target.port is not None else self.default_port

        logging.log(logging.INFO, 'UDP sending(' + target.ip + ':' + str(port) + ')...')

        success = self.requester.request_udpport(target.ip, port)

        return success, {}

    def get_requires(self):
        return ['udp']

    def build_data(self, target, data, success, response, response_time):
        data.set('udp', success)
        data.set('udp_time', response_time)

        self._append_error(data, response)


class HttpCollector(DataCollector):
    """
    :param requester:
    :type requester: ipsurv.requester.server_reactivity.ServerReactivity
    :param args:
    :type args: argparse.Namespace
    """
    def __init__(self, requester, args):
        super().__init__(requester, args)

        self.http = args.http

    def get_name(self):
        return 'HTTP'

    def request_data(self, target, requires):
        url = target.url if target.url else target.fqdn if target.fqdn else target.ip

        logging.log(logging.INFO, 'HTTP requesting(' + url + ')...')

        success, response = self.requester.request(url)

        if self.http == 2:
            response['http_h2'] = self.requester.request_alpn_h2(url)

        return success, response

    def get_requires(self):
        return ['http', 'http_status', 'http_size', 'http_h2']

    def build_data(self, target, data, success, response, response_time):
        data.set('http', success)
        data.set('http_time', response_time)

        self.put(data, response, 'http_status')
        self.put(data, response, 'http_size')
        self.put(data, response, 'http_server')
        self.put(data, response, 'http_mime')

        if response.get('http_h2') is not None:
            self.put(data, response, 'http_h2')

        self._append_error(data, response)
