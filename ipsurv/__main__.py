from ipsurv.core.object_factory import ObjectFactory
from ipsurv.ip_surv_cmd import IpSurvCmd
from ipsurv.util.sys_util import System


def main():
    if System.get_python_ver() <= 3.2 and not System.load_module('ipaddress'):
        System.warn('"ipaddress" module is required. Please install by `pip install ipaddress`.')

    factory = ObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()


if __name__ == '__main__':
    main()
