from ipsurv.configs import Constant
from ipsurv.core.object_factory import ObjectFactory
from ipsurv.ip_surv_cmd import IpSurvCmd


def main():
    factory = ObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()


if __name__ == '__main__':
    main()
