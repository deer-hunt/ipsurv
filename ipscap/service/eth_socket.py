import fcntl
import ipaddress
import socket
import struct
from ipsurv.util.sys_util import AppException


class EthSocket:
    ETH_LEN = 14

    def __init__(self):
        self.sock = None

    def create_socket(self):
        try:
            self.sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        except PermissionError:
            raise AppException('Permission error. Please run as "root" user.')

    def get_eth_ips(self):
        ips = []

        for interface in socket.if_nameindex():
            name = interface[1]
            ips.append(self.get_eth_ip(name))

        return ips

    def get_eth_ips_int(self):
        return list(map(lambda v: int(ipaddress.ip_address(v)), self.get_eth_ips()))

    def get_eth_ip(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        addr = fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCSIFADDR
            struct.pack('256s', ifname.encode('utf-8'))
        )

        return socket.inet_ntoa(addr[20:24])

    def recvfrom(self, bufsize):
        data, addr = self.sock.recvfrom(bufsize)

        return data

    def get_eth_header(self, data):
        return data[:self.ETH_LEN]

    def is_enabled_protocol(self, eth_header):
        eth = struct.unpack('!6s6sH', eth_header)
        eth_protocol = socket.ntohs(eth[2])

        # IP Protocol number = 8: IPv4
        if eth_protocol == 8:
            return True

        return False

    def get_ip_mtu(self, data):
        return data[self.ETH_LEN:]

    def __del__(self):
        if self.sock:
            self.sock.close()
