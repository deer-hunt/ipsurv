from ipscap.core.object_factory import ObjectFactory
from ipscap.ipscap_cmd import IpsCapCmd
from ipsurv.util.sys_util import System
import os


def main():
    if System.get_python_ver() <= 3.2 and not System.load_module('ipaddress'):
        System.exit('"ipaddress" module is required. Please install by `pip install ipaddress`.', True)

    if System.verify_os(windows=True, macos=True):
        System.exit('`ipscap` support only Unix/Linux OS.', True)

    factory = ObjectFactory()

    ips_cap_cmd = IpsCapCmd(factory)

    ips_cap_cmd.run()


if __name__ == '__main__':
    main()
