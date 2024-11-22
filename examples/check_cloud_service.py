from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.entity import ValueData

from ipsurv.ip_surv_cmd import IpSurvCmd

import re

'''
Checking cloud service from hostname.

Specification:
- Customizing Pipeline class.

Command:
# cat examples.txt|python3 check_cloud_service.py

Result e.g.:
*******,*.*.*.231,ec2-*-*-*-231.eu-central-1.compute.amazonaws.com,AWS
***********,*.*.*.138,*-*-*-138.deploy.static.akamaitechnologies.com,AKAMAI
******,*.*.*.111,a*********.awsglobalaccelerator.com,AWS
*********,*.*.*.38,*-*-*-38.deploy.static.akamaitechnologies.com,AKAMAI
'''


class MyPipeline(Pipeline):
    CLOUD_SERVICES = {
        'AWS': r'\.amazonaws\.com|\.cloudfront\.net|awsglobalaccelerator\.com',
        'GOOGLE': r'\.googleapis\.com|\.google\.com|\.gcloud\.com',
        'AZURE': r'\.azure\.com|\.azurewebsites\.net',
        'IBM': r'\.ibm\.com',
        'ORACLE': r'\.oraclecloud\.com',
        'AKAMAI': r'\.akamaitechnologies\.com|\.linode\.com|\.linodeobjects\.com',
        'ALIBABA': r'\.aliyuncs\.com',
        'HEROKU': r'\.heroku\.com'
    }

    def pre_configure(self, args, env_args, env_conf):
        args.format = '{ip},{hostname},{cloud}'

    def post_collect(self, data, target, args, skip):
        hostname = data.get('hostname')

        cloud = self._detect_cloud_service(hostname)

        data.set('cloud', cloud)

        self.serializer.set_status(data, target, args, skip)

    def _detect_cloud_service(self, v):
        if v:
            for service, regex in self.CLOUD_SERVICES.items():
                if re.search(r'(' + regex + ')', v):
                    return service

        return ''


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
