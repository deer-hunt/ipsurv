import pytest
import os

if os.name == 'posix':
    from ipscap.util.raw_socket_entity import IPHeader, TCPHeader
    from ipscap.service.transfer_store import TransferStore

    class TestTransferStore:
        @pytest.fixture
        def ip_header(self, mocker):
            ip_header = mocker.Mock(spec=IPHeader)
            ip_header.direction = IPHeader.DIRECTION_SEND
            ip_header.protocol = IPHeader.PROTOCOL_TCP
            ip_header.src_ip = '192.168.1.2'
            ip_header.dest_ip = '192.168.1.1'
            return ip_header

        @pytest.fixture
        def protocol_header(self, mocker):
            protocol_header = mocker.Mock()
            protocol_header.src_port = 12345
            protocol_header.dest_port = 80
            protocol_header.payload_length = 100
            protocol_header.get_sanitized_data.return_value = 'data'
            return protocol_header

        @pytest.fixture
        def transfer_store(self):
            return TransferStore()

        def test_add_transfer(self, transfer_store, ip_header, protocol_header):
            passage_num = transfer_store.add(ip_header, protocol_header)
            assert passage_num == 1

            key = (IPHeader.PROTOCOL_TCP, '192.168.1.2', 12345, '192.168.1.1', 80)

            assert key in transfer_store.transfers

        def test_totalize(self, transfer_store, ip_header, protocol_header):
            transfer_store.add(ip_header, protocol_header)
            transfers = transfer_store.totalize(None)

            assert len(transfers) == 1

        def test_totalize_groups(self, transfer_store, ip_header, protocol_header):
            transfer_store.add(ip_header, protocol_header)

            sorted_transfers = dict(sorted(transfer_store.transfers.items()))
            transfers = transfer_store.totalize_groups(sorted_transfers, 1)

            assert len(transfers) == 1

        def test_totalize_direction(self, transfer_store, ip_header, protocol_header):
            transfer_store.add(ip_header, protocol_header)
            sorted_transfers = dict(sorted(transfer_store.transfers.items()))
            key = next(iter(sorted_transfers))
            transfer = sorted_transfers[key]
            rtransfer = {IPHeader.DIRECTION_SEND: {'count': 0, 'unique': 0, 'size': 0}, IPHeader.DIRECTION_RECEIVE: {'count': 0, 'unique': 0, 'size': 0}, 'group_count': 0}
            transfer_store.totalize_direction(rtransfer, transfer, IPHeader.DIRECTION_SEND)

            assert rtransfer[IPHeader.DIRECTION_SEND]['count'] == 1
