from ipscap.util.raw_socket_entity import IPHeader


class TransferStore:
    def __init__(self):
        self.transfers = {}

    def add(self, ip_header, protocol_header):
        key = self._get_transfer_key(ip_header, protocol_header)

        if key not in self.transfers:
            self.transfers[key] = {IPHeader.DIRECTION_SEND: {'num': 0, 'unique': 0, 'size': 0},
                                   IPHeader.DIRECTION_RECEIVE: {'num': 0, 'unique': 0, 'size': 0},
                                   'cur': 0}

        transfer = self.transfers[key][ip_header.direction]
        transfer['num'] += 1
        transfer['size'] += protocol_header.payload_length

        passage_num = transfer['num']

        if len(protocol_header.get_sanitized_data()) > 0:
            cur = self.transfers[key]['cur']

            if cur != ip_header.direction:
                transfer['unique'] += 1
                self.transfers[key]['cur'] = ip_header.direction

        return (passage_num)

    def _get_transfer_key(self, ip_header, protocol_header):
        key = None

        if ip_header.direction == IPHeader.DIRECTION_SEND:
            key = (ip_header.protocol, ip_header.src_ip, protocol_header.src_port, ip_header.dest_ip, protocol_header.dest_port)
        elif ip_header.direction == IPHeader.DIRECTION_RECEIVE:
            key = (ip_header.protocol, ip_header.dest_ip, protocol_header.dest_port, ip_header.src_ip, protocol_header.src_port)

        return key

    def totalize(self, stat_group):
        sorted_transfers = dict(sorted(self.transfers.items()))

        if stat_group:
            transfers = self.totalize_groups(sorted_transfers, stat_group)
        else:
            transfers = sorted_transfers

        return transfers

    def totalize_groups(self, sorted_transfers, stat_group):
        transfers = dict()

        for key, transfer in sorted_transfers.items():
            (protocol, first_ip, first_port, second_ip, second_port) = key

            port = first_port if first_port < second_port else second_port

            if stat_group == 1:
                key = (protocol, first_ip, second_ip, port)
            else:
                key = (protocol, first_ip, second_ip, -1)

            if key not in transfers:
                transfers[key] = {IPHeader.DIRECTION_SEND: {'num': 0, 'unique': 0, 'size': 0},
                                  IPHeader.DIRECTION_RECEIVE: {'num': 0, 'unique': 0, 'size': 0},
                                  'group_count': 0}

            rtransfer = transfers[key]
            rtransfer['group_count'] += 1

            self.totalize_direction(rtransfer, transfer, IPHeader.DIRECTION_SEND)
            self.totalize_direction(rtransfer, transfer, IPHeader.DIRECTION_RECEIVE)

            transfers[key] = rtransfer

        return transfers

    def totalize_direction(self, rtransfer, transfer, direction):
        rtrans = rtransfer[direction]
        trans = transfer[direction]

        for k, v in trans.items():
            rtrans[k] += v
