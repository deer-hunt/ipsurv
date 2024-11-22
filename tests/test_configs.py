import pytest

from ipsurv.configs import Constant, Config


class TestConstant:
    def test_vars(self):
        assert Constant.APP_NAME == 'ipsurv'
        assert hasattr(Constant, 'APP_DESCRIPTION')
        assert hasattr(Constant, 'APP_BOTTOM_DESC')
        assert hasattr(Constant, 'ENV_ARGS_VAR')
        assert hasattr(Constant, 'ENV_CONF_VAR')
        assert hasattr(Constant, 'DELIMITER_DEFAULT')


class TestConfig:
    def test_vars(self):
        assert hasattr(Config, 'PRE_ARGUMENTS')
        assert hasattr(Config, 'APP_ARGUMENTS')
        assert hasattr(Config, 'ENV_CONFS')
        assert hasattr(Config, 'FORMAT_PROFILES')
        assert hasattr(Config, 'FORMAT_PARAMS')
        assert hasattr(Config, 'MASTER_DATA')
        assert hasattr(Config, 'COLLECTORS')
        assert hasattr(Config, 'HEAD_MSG_SELF')
