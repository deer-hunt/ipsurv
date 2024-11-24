import socket
import struct
import subprocess
import platform

from ipsurv.requester.requester import Requester


class ServerReactivity(Requester):
    def __init__(self, timeout=4.0):
        super().__init__(timeout)

    def request_icmp(self, host, count=1):
        timeout = round(self.timeout)
        timeout = timeout if timeout > 0 else 1

        if platform.system() != 'Windows':
            subprocess.check_output(['ping', '-c', str(count), '-w', str(timeout), host], universal_newlines=True)
        else:
            subprocess.check_output(['ping', '-n', str(count), '-w', str(timeout), host], universal_newlines=True)

        success = True

        return success

    def request_tcpport(self, host, port):
        success = False
        conn = None

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            conn.settimeout(self.timeout)

            conn.connect((host, port))

            success = True
        except Exception as e:
            raise e
        finally:
            conn.close()

        return success

    def request_udpport(self, host, port):
        success = False
        conn = None

        try:
            conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            conn.settimeout(self.timeout)

            v = self._build_query()

            conn.sendto(v, (host, port))

            response, server = conn.recvfrom(4096)

            success = True
        except Exception as e:
            raise e
        finally:
            conn.close()

        return success

    def request_local_ip(self, ip='8.8.8.8', port=53):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((ip, port))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            return str(e)

    def _build_query(self):
        transaction_id = b'\x00\x01'
        flags = b'\x01\x00'

        questions = struct.pack('>H', 1)
        answer_rrs = struct.pack('>H', 0)
        authority_rrs = struct.pack('>H', 0)
        additional_rrs = struct.pack('>H', 0)

        data = b'\x00'

        query_type = struct.pack('>H', 1)
        query_class = struct.pack('>H', 1)

        query = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + data + query_type + query_class

        return query
