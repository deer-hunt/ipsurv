import logging
import socket
import ssl
import threading

from ipsend.configs import Constant
from ipsurv.util.sys_util import AppException


class Socket:
    def __init__(self):
        self._sock = None
        self._data_input = None
        self._data_output = None
        self._mode = None
        self._timeout = -1

    @staticmethod
    def get_error(e):
        error = None

        if isinstance(e, socket.timeout):
            error = 'Connection timeout.'
        elif isinstance(e, socket.gaierror):
            error = 'Connection error.'
        elif isinstance(e, socket.herror) or isinstance(e, socket.error):
            error = 'Socket error.'

        return error

    def initialize(self, data_input, data_output, mode, timeout):
        pass

    def create(self, hostname, port=0):
        pass

    def connected(self):
        return (self._sock)

    def send(self, data):
        pass

    def receive(self, bufsize=Constant.RECV_BUF_SIZE):
        pass

    def close(self):
        if self._sock:
            self._sock.close()

            self._sock = None
            self._hostname = None
            self._port = None

    def __del__(self):
        self.close()


class RichSocket(Socket):
    def __init__(self):
        super().__init__()

    def initialize(self, data_input, data_output, mode, timeout):
        self._data_input = data_input
        self._data_output = data_output
        self._mode = mode
        self._timeout = timeout
        self._ssl_context = None

    def set_ssl_context(self, ssl_context):
        self._ssl_context = ssl_context

    def create(self, hostname, port=0):
        if self._mode != Constant.MODE_UDP:
            self._sock = self.create_tcp_socket(hostname, port)
        else:
            self._sock = self.create_udp_socket()

        self._hostname = hostname
        self._port = port

    def create_tcp_socket(self, hostname, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.settimeout(self._timeout)

        sock.connect((hostname, port))

        if self._mode == Constant.MODE_SSL:
            if not self._ssl_context:
                context = ssl.create_default_context()
            else:
                context = ssl.SSLContext(self._ssl_context)

            sock = context.wrap_socket(sock, server_hostname=hostname)

        return sock

    def create_udp_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.settimeout(self._timeout)

        return sock

    def send(self, data):
        byte_data = self._data_input.get_data(data)

        if self._mode:
            self._sock.sendall(byte_data)
        else:
            self._sock.sendto(byte_data, (self._hostname, self._port))

    def receive(self, bufsize=Constant.RECV_BUF_SIZE):
        while True:
            if self._mode:
                data = self._sock.recv(bufsize)
            else:
                data, _ = self._sock.recvfrom(bufsize)

            if not data:
                break

            self._data_output.output_binary(data)

        self.close()


class RawSocket(Socket):
    def __init__(self):
        super().__init__()

        self._mode = None

    def initialize(self, data_input, data_output, mode, timeout):
        self._data_input = data_input
        self._data_output = data_output
        self._mode = mode
        self._timeout = timeout

    def connected(self):
        return (self._sock)

    def create(self, hostname, port=0):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, self.get_proto(self._mode))

            self._sock.settimeout(self._timeout)
        except PermissionError:
            raise AppException('Permission error. Please run as "root" user.')

        self._hostname = hostname

    def get_proto(self, mode):
        if mode in [Constant.MODE_IP_HEADER, Constant.MODE_IP_PAYLOAD]:
            proto = socket.IPPROTO_RAW
        elif mode in [Constant.MODE_TCP_HEADER, Constant.MODE_TCP_PAYLOAD]:
            proto = socket.IPPROTO_TCP
        elif mode == [Constant.MODE_UDP_HEADER, Constant.MODE_UDP_PAYLOAD]:
            proto = socket.IPPROTO_UDP
        elif mode == [Constant.MODE_ICMP_HEADER, Constant.MODE_ICMP_PAYLOAD]:
            proto = socket.IPPROTO_ICMP
        else:
            raise Exception('Unknown mode.')

        return proto

    def send(self, data):
        byte_data = self._data_input.get_data(data)

        self._sock.sendto(byte_data, (self._hostname, 0))

    def receive(self, bufsize=Constant.RECV_BUF_SIZE):
        while True:
            data, _ = self._sock.recvfrom(bufsize)

            self._data_output.output_binary(data)

        self.close()


class SocketThread(threading.Thread):
    def __init__(self, sock, view_helper):
        super().__init__()

        self.daemon = True

        self.sock = sock
        self.view_helper = view_helper

    def run(self):
        try:
            self.sock.receive()
        except Exception as e:
            self.sock.close()

            self.view_helper.output_error(e)

            logging.log(logging.ERROR, str(e), exc_info=True)
