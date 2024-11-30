import ipaddress
import threading
import socket


class IpUtil:
    @classmethod
    def get_ip_address(cls, ip):
        return ipaddress.ip_address(ip)

    @classmethod
    def get_ip_int(cls, ip):
        ip = ipaddress.ip_address(ip)
        ip_int = int(ip)

        return ip_int

    @classmethod
    def get_ip_from_int(cls, ip_int):
        ip = ipaddress.ip_address(ip_int)

        return str(ip)

    @classmethod
    def get_ip_network(cls, cidr):
        return ipaddress.ip_network(cidr, strict=False)

    # ex: 192.168.1.0/24
    @classmethod
    def get_network_range(cls, cidr):
        network = ipaddress.ip_network(cidr, strict=False)

        first_ip = network.network_address + 1
        last_ip = network.broadcast_address - 1

        return int(first_ip), int(last_ip)


class DnsUtil:
    @classmethod
    def getaddrinfo(cls, hostname, port=None, timeout=8.0):
        thread = ResolveThread(hostname, port)

        cls._run(thread, timeout)

        return thread.sockaddr

    @classmethod
    def resolve(cls, host, port=None, timeout=None):
        sockaddr = DnsUtil.getaddrinfo(host, port, timeout)

        return sockaddr[0]

    @classmethod
    def reverse(cls, ip, timeout=8.0):
        thread = ReverseThread(ip)

        cls._run(thread, timeout)

        return thread.hostname

    @classmethod
    def _run(cls, thread, timeout):
        thread.start()

        thread.join(timeout)

        if thread.is_alive():
            raise socket.timeout('Socket timeout error.')
        elif thread.e:
            raise thread.e


class ResolveThread(threading.Thread):
    def __init__(self, hostname, port=None):
        super().__init__()

        self.hostname = hostname
        self.port = port

        self.sockaddr = None

        self.e = None
        self.daemon = True

    def run(self):
        try:
            sockaddrs = socket.getaddrinfo(self.hostname, self.port)

            self.sockaddr = sockaddrs[0][4]
        except socket.error as e:
            self.e = e


class ReverseThread(threading.Thread):
    def __init__(self, ip):
        super().__init__()

        self.ip = ip

        self.hostname = None

        self.e = None
        self.daemon = True

    def run(self):
        try:
            vals = socket.gethostbyaddr(self.ip)

            self.hostname = vals[0]
        except socket.error as e:
            self.e = e
