from ipsurv.data_collector.data_collector import DataCollector
from ipsurv.core.object_factory import ObjectFactory
from ipsurv.core.pipeline import Pipeline
import re

from ipsurv.ip_surv_cmd import IpSurvCmd

'''
Checking WordPress site.

Specification:
- Customizing DataCollector class.

Command:
# cat examples.txt|python3 check_wordpress_site.py

Result e.g.:
1,https://wordpress.org/,200,WP_SITE,wporg-parent-2021
2,https://blogs.microsoft.com/,200,WP_SITE,ms-blogs
3,https://www.sonymusic.com/,200,WP_SITE,sonymusic
4,https://techcrunch.com/,200,WP_SITE,tc-24
5,https://vogue.com/,200,NORMAL_SITE,
6,https://www.rollingstone.com/,200,WP_SITE,vip
7,https://www.portent.com/,200,WP_SITE,portent_portent
8,https://nove.eu/,200,WP_SITE,nove
9,https://www.sushikimura.com.sg/,200,WP_SITE,grandrestaurant
10,https://www.phocafe.co.uk/,200,WP_SITE,pho-2018
'''


class MyPipeline(Pipeline):
    def pre_configure(self, args, env_args, env_conf):
        args.format = '{http_status},{wp_status},{wp_theme}'

    def post_configure(self, args, env_args, env_conf):
        args.fixed_collectors = ['wp_collector']


class WordPressCollector(DataCollector):
    def __init__(self, requester, args):
        super().__init__(requester, args)

    def get_name(self):
        return 'WORDPRESS'

    def request_data(self, target):
        url = target.url if target.url else target.fqdn

        success, response = self.requester.request(url, 'utf-8')

        return (success, response)

    def get_requires(self):
        return ['wp_status', 'wp_theme']

    def build_data(self, target, data, success, response, response_time):
        http_status = response['http_status']
        html = response['body']

        is_wordpress = self._is_wordpress(html)

        if http_status == 200:
            wp_status = 'WP_SITE' if is_wordpress else 'NORMAL_SITE'
        else:
            wp_status = '-'

        data.set('wp_status', wp_status)

        theme = self._get_wp_theme(html)

        data.set('wp_theme', theme)

        self.put(data, response, 'http_status')

    def _is_wordpress(self, html):
        if re.search(r'\/wp-content', html):
            return True

        return False

    def _get_wp_theme(self, html):
        m = re.search(r'\/wp-content\/themes\/([^/]+)', html)

        if not m:
            return ''

        return m.group(1)


class MyObjectFactory(ObjectFactory):
    def create_pipeline(self):
        return MyPipeline()

    def create_collectors(self, args, dns_resolver):
        http_requester = self.create_http(args)

        collectors = {}

        collectors['wp_collector'] = WordPressCollector(http_requester, args)

        return collectors


if __name__ == '__main__':
    factory = MyObjectFactory()

    ip_surv_cmd = IpSurvCmd(factory)

    ip_surv_cmd.run()
