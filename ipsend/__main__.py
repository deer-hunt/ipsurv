from ipsend.core.object_factory import ObjectFactory
from ipsend.ipsend_cmd import IpSendCmd


def main():
    factory = ObjectFactory()

    ips_cap_cmd = IpSendCmd(factory)

    ips_cap_cmd.run()


if __name__ == '__main__':
    main()
