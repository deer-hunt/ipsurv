import pytest
import time
import os

if os.name == 'posix':
    from ipscap.configs import Constant
    from ipscap.service.view_helper import ViewHelper
    from ipscap.service.dumpfile import DumpFile
    from ipscap.util.raw_socket_entity import IPHeader

    class TestViewHelper:
        @pytest.fixture
        def view_helper(self):
            return ViewHelper()

        @pytest.fixture
        def args(self, mocker):
            args = mocker.Mock()

            args.timeout = None
            args.fixed_output = Constant.OUTPUT_NONE
            args.fixed_protocols = []
            args.stat_mode = 2
            args.stat_group = False

            return args

        def test_show_head(self, capfd, view_helper, args):
            view_helper.show_head(args)

            captured = capfd.readouterr()

            assert 'packets...' in captured.out

        def test_show_dumpfile_info(self, capfd, view_helper, mocker):
            dumpfile = mocker.Mock(spec=DumpFile)
            dumpfile.get_path.return_value = '/path/to/dumpfile'
            dumpfile.get_file_num.return_value = 12

            view_helper.show_dumpfile_info(dumpfile)

            captured = capfd.readouterr()

            assert '/path/to/dumpfile' in captured.out
            assert '12' in captured.out

        def test_show_statistics(self, capfd, view_helper, args):
            transfers = {
                ('TCP', '192.168.1.2', 80, '192.168.1.100', 8080): {
                    IPHeader.DIRECTION_SEND: {'count': 10, 'unique': 5, 'size': 500},
                    IPHeader.DIRECTION_RECEIVE: {'count': 8, 'unique': 4, 'size': 400},
                }
            }

            begin_tm = time.time()
            end_tm = time.time()

            view_helper.show_statistics(transfers, begin_tm, end_tm, args)

            captured = capfd.readouterr()

            assert 'STATISTICS' in captured.out
            assert '192.168.1.2:80' in captured.out
            assert '500' in captured.out

        def test_show_stat_transfer_groups(self, capfd, view_helper, args):
            transfers = {
                ('TCP', '192.168.1.2', '192.168.1.100', 80): {
                    IPHeader.DIRECTION_SEND: {'count': 10, 'unique': 5, 'size': 500},
                    IPHeader.DIRECTION_RECEIVE: {'count': 8, 'unique': 4, 'size': 400},
                    'group_count': 1
                }
            }

            view_helper._show_stat_transfer_groups(transfers)

            captured = capfd.readouterr()

            assert 'GROUPS:' in captured.out

        def test_stopped(self, capfd, view_helper):
            view_helper.stopped()

            captured = capfd.readouterr()

            assert 'Stopped by' in captured.out

        def test_get_border(self, view_helper):
            border = view_helper.get_border(10)

            assert len(border) >= 10
