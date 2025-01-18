from ipsurv.core.object_factory import ObjectFactory
from ipsurv.configs import Config

from ipsurv.ip_surv_cmd import IpSurvCmd

import re

'''
Customizing Config class.

Specification:
- Customizing Config class.
- Creating ObjectFactory class.

Command:
# cat examples.txt|python3 config_customize.py
'''


class MyObjectFactory(ObjectFactory):
    def get_config(self):
        Config.APP_ARGUMENTS['json']['default'] = 2
        Config.COLLECTORS = ['dnsreverse']

        return Config


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
