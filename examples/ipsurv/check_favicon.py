from ipsurv.data_collector.pass_data_collector import PassDataCollector, PassRequester
from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
import urllib.parse
import urllib.request
import urllib.error

from ipsurv.ip_surv_cmd import IpSurvCmd

'''
Checking favicon.ico.

Specification:
- Customizing Requester class.
- Using PassRequester, PassDataCollector

Command:
# cat examples.txt|python3 check_favicon.py

Result e.g.:
https://translate.google.com/,200,OK,32988
https://www.google.com/,200,OK,5430
https://mail.google.com/,200,OK,26068
'''


class MyPipeline(Pipeline):
    def pre_configure(self, args, env_args, env_conf):
        args.format = '{http_status},{favicon},{favicon_size}'

    def post_configure(self, args, env_args, env_conf):
        args.fixed_collectors = ['favicon_collector']


class FaviconRequester(PassRequester):
    def request(self, target):
        res, body = self.request_favicon(target.fqdn)

        success = False

        if res.status == 200:
            success = True

        response = {
            'http_status': res.status,
            'favicon': success,
            'favicon_size': len(body),
        }

        return success, response

    def request_favicon(self, fqdn):
        path = '/favicon.ico'

        url = 'https://' + fqdn + path

        req = urllib.request.Request(url)

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as res:
                body = res.read()
        except urllib.error.URLError as e:
            res = e
            body = ''

        return res, body


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()

    def create_collectors(self, args, dns_resolver):
        favicon_requester = FaviconRequester(args.fixed_timeout['http'])

        collectors = {}

        collectors['favicon_collector'] = PassDataCollector('favicon', favicon_requester, args)

        return collectors


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
