import json
import logging
import re
from urllib.parse import urlparse

from ipsurv.requester.requester import Requester


class CountryDetector:
    COUNTRIES = {
        'afghanistan': 'AF', 'albania': 'AL', 'algeria': 'DZ', 'angola': 'AO', 'argentina': 'AR', 'armenia': 'AM', 'australia': 'AU', 'austria': 'AT',
        'azerbaijan': 'AZ', 'bahrain': 'BH', 'bangladesh': 'BD', 'belarus': 'BY', 'belgium': 'BE', 'benin': 'BJ', 'bhutan': 'BT', 'bolivia': 'BO',
        'bosnia and herzegovina': 'BA', 'botswana': 'BW', 'brazil': 'BR', 'bulgaria': 'BG', 'burkina faso': 'BF', 'burundi': 'BI', 'cambodia': 'KH', 'cameroon': 'CM',
        'canada': 'CA', 'chad': 'TD', 'chile': 'CL', 'colombia': 'CO', 'congo': 'CG',
        'costa rica': 'CR', 'croatia': 'HR', 'cuba': 'CU', 'cyprus': 'CY', 'czech': 'CZ', "côte d'ivoire": 'CI', 'denmark': 'DK', 'djibouti': 'DJ', 'dominica': 'DM',
        'ecuador': 'EC', 'egypt': 'EG', 'el salvador': 'SV', 'equatorial guinea': 'GQ', 'eritrea': 'ER', 'estonia': 'EE', 'ethiopia': 'ET',
        'fiji': 'FJ', 'finland': 'FI', 'france': 'FR', 'gabon': 'GA', 'gambia': 'GM', 'georgia': 'GE', 'germany': 'DE', 'ghana': 'GH', 'greece': 'GR', 'greenland': 'GL',
        'guam': 'GU', 'guatemala': 'GT', 'guinea': 'GN', 'guinea-bissau': 'GW', 'guyana': 'GY', 'haiti': 'HT', 'honduras': 'HN', 'hong kong': 'HK', 'hungary': 'HU',
        'iceland': 'IS', 'india': 'IN', 'indonesia': 'ID', 'iran': 'IR', 'iraq': 'IQ', 'ireland': 'IE', 'israel': 'IL', 'italy': 'IT', 'jamaica': 'JM', 'japan': 'JP',
        'jordan': 'JO', 'kazakhstan': 'KZ', 'kenya': 'KE', 'korea': 'KR', 'south korea': 'KR', 'kuwait': 'KW',
        'kyrgyzstan': 'KG', 'latvia': 'LV', 'lebanon': 'LB', 'lesotho': 'LS', 'liberia': 'LR', 'libya': 'LY', 'lithuania': 'LT',
        'macao': 'MO', 'madagascar': 'MG', 'malawi': 'MW', 'malaysia': 'MY', 'maldives': 'MV', 'mali': 'ML',
        'malta': 'MT', 'mauritania': 'MR', 'mauritius': 'MU', 'mexico': 'MX', 'micronesia': 'FM', 'moldova': 'MD', 'monaco': 'MC',
        'mongolia': 'MN', 'montenegro': 'ME', 'morocco': 'MA', 'mozambique': 'MZ', 'myanmar': 'MM', 'namibia': 'NA', 'nepal': 'NP', 'netherlands': 'NL',
        'new zealand': 'NZ', 'nicaragua': 'NI', 'niger': 'NE', 'nigeria': 'NG', 'norway': 'NO', 'oman': 'OM', 'pakistan': 'PK', 'palestine': 'PS', 'panama': 'PA',
        'papua new guinea': 'PG', 'paraguay': 'PY', 'peru': 'PE', 'philippines': 'PH', 'poland': 'PL', 'portugal': 'PT', 'puerto rico': 'PR', 'qatar': 'QA', 'romania': 'RO',
        'russia': 'RU', 'rwanda': 'RW', 'saudi arabia': 'SA', 'senegal': 'SN', 'serbia': 'RS', 'sierra leone': 'SL', 'singapore': 'SG', 'slovakia': 'SK', 'slovenia': 'SI',
        'solomon islands': 'SB', 'somalia': 'SO', 'south africa': 'ZA', 'south sudan': 'SS', 'spain': 'ES', 'sri lanka': 'LK', 'sudan': 'SD', 'swaziland': 'SZ',
        'sweden': 'SE', 'switzerland': 'CH', 'swiss confederation': 'CH', 'syria': 'SY', 'taiwan': 'TW', 'tajikistan': 'TJ', 'tanzania': 'TZ',
        'thailand': 'TH', 'togo': 'TG', 'tunisia': 'TN', 'turkey': 'TR', 'turkmenistan': 'TM', 'uganda': 'UG', 'ukraine': 'UA',
        'uruguay': 'UY', 'uzbekistan': 'UZ', 'venezuela': 'VE',
        'viet nam': 'VN', 'yemen': 'YE', 'zambia': 'ZM', 'zimbabwe': 'ZW',

        'china': 'CN', 'pr china': 'CN',
        'united states': 'US', 'usa': 'US', 'u.s.a': 'US', 'u.s': 'US', 'united states of america': 'US',
        'united kingdom': 'GB', 'england': 'GB', 'great britain': 'GB', 'u.k': 'GB',
        'united arab emirates': 'AE', 'uae': 'AE'
    }

    COUNTRIES_REGEX = {
        'BO': r'bolivia',
        'CF': r'central african',
        'CD': r"(republic\s+[\w\s',.-]{5,10}\s+congo|congo[,\s]+[\w\s',.-]{10,20}\s+republic)",
        'CN': r"(republic\s+[\w\s',.-]{2,5}\s+china|china[,\s]+[\w\s',.-]{2,5}\s+republic)",
        'CZ': r'czech',
        'DO': r'dominican',
        'FM': r'micronesia',
        'HK': r'hksar',
        'IR': r'iran',
        'KP': r"(democratic\s+[\w\s',.-]{2,25}\s+korea|korea[,\s]+[\w\s',.-]{2,25}\s+democratic)",
        'KR': r"(republic\s+[\w\s',.-]{2,5}\s+korea|korea[,\s]+[\w\s',.-]{2,5}\s+republic)",
        'LA': r"lao\s+[\w\s',.-]{2,10}\s+democratic",
        'MD': r'moldova',
        'PS': r'palestine',
        'RU': r'(russian|russia)',
        'SY': r'syrian',
        'TW': r'taiwan',
        'TZ': r'tanzania',
        'US': r'(usa|united states)',
        'VE': r'(venezuela|bolivarian)'
    }

    def detect_by_address(self, v):
        v = re.sub(r'^[\s,/]+|[\s,/]+$', '', v)
        v = re.sub(r'[ \t]+', ' ', v)

        lines = re.split(r'[\r\n,;]', v)

        code = self.detect_by_country(lines[-1])

        if code is None:
            code = self.detect_by_country(lines[0])

        return code

    def detect_by_country(self, word):
        word = word.strip(' .')
        v = word.lower()

        code = None

        if v in self.COUNTRIES:
            code = self.COUNTRIES[v]
        else:
            c = word.upper()

            codes = list(self.COUNTRIES.values())

            if c in codes:
                code = c

        if code is None:
            for cd, regex in self.COUNTRIES_REGEX.items():
                if re.search(r'(^|[\s,])' + regex + r'($|[\s,])', v, flags=re.I):
                    code = cd
                    break

        return code


class RdapRequester(Requester):
    ID_ICANN = 0
    ID_ARIN = 1
    ID_APNIC = 2
    ID_RIPE = 3
    ID_LACNIC = 4
    ID_AFRINIC = 5

    RDAP_ICANN = 'https://rdap.iana.org/'
    RDAP_ARIN = 'https://rdap.arin.net/registry/'
    RDAP_APNIC = 'https://rdap.apnic.net/'
    RDAP_RIPE = 'https://rdap.db.ripe.net/'
    RDAP_LACNIC = 'https://rdap.lacnic.net/rdap/'
    RDAP_AFRINIC = 'https://rdap.afrinic.net/rdap/'

    RDAP_SERVERS = {
        0: RDAP_ICANN,
        1: RDAP_ARIN,
        2: RDAP_APNIC,
        3: RDAP_RIPE,
        4: RDAP_LACNIC,
        5: RDAP_AFRINIC
    }

    COLLATIONS = {
        1: 2, 2: 3, 5: 3, 14: 2, 25: 3, 27: 2, 31: 3, 36: 2, 37: 3, 39: 2, 41: 5, 42: 2,
        43: 2, 46: 3, 49: 2, 51: 3, 58: 2, 59: 2, 60: 2, 61: 2, 62: 3, 77: 3, 78: 3, 79: 3,
        80: 3, 81: 3, 82: 3, 83: 3, 84: 3, 85: 3, 86: 3, 87: 3, 88: 3, 89: 3, 90: 3, 91: 3,
        92: 3, 93: 3, 94: 3, 95: 3, 101: 2, 102: 5, 103: 2, 105: 5, 106: 2, 109: 3, 110: 2,
        111: 2, 112: 2, 113: 2, 114: 2, 115: 2, 116: 2, 117: 2, 118: 2, 119: 2, 120: 2,
        121: 2, 122: 2, 123: 2, 124: 2, 125: 2, 126: 2, 133: 2, 141: 3, 145: 3, 150: 2,
        151: 3, 153: 2, 154: 5, 163: 2, 171: 2, 175: 2, 176: 3, 177: 4, 178: 3, 179: 4,
        180: 2, 181: 4, 182: 2, 183: 2, 185: 3, 186: 4, 187: 4, 188: 3, 189: 4, 190: 4,
        191: 4, 193: 3, 194: 3, 195: 3, 196: 5, 197: 5, 200: 4, 201: 4, 202: 2, 203: 2,
        210: 2, 211: 2, 212: 3, 213: 3, 217: 3, 218: 2, 219: 2, 220: 2, 221: 2, 222: 2,
        223: 2
    }

    def __init__(self, country_detector, fill=True, timeout=None):
        super().__init__(timeout)

        self.host = 'rdap.arin.net'
        self.country_detector = country_detector  # type: CountryDetector
        self.fill = fill

    def detect_server_from_ip(self, ip):
        serial1 = self.get_octet1_by_ip(ip)

        server = None

        if serial1 is not None:
            if serial1 in self.COLLATIONS:
                server_id = self.COLLATIONS[serial1]

                server = self.RDAP_SERVERS[server_id]

        if server is None:
            server = self.RDAP_ARIN

        return server

    def get_octet1_by_ip(self, ip):
        match = re.search(r'^(\d{1,3})\.', ip)

        v = None

        if match is not None:
            v = int(match.group(1))

        return v

    def get_octet2_by_ip(self, ip):
        match = re.search(r'^(\d{1,3})\.(\d{1,3})', ip)

        v = None

        if match is not None:
            v = int(match.group(1)) * 1000 + int(match.group(2))

        return v

    def get_id_from_server(self, server):
        server_id = None

        for k, v in self.RDAP_SERVERS.items():
            if v == server:
                server_id = k
                break

        return server_id

    def request(self, ip, url=None):
        if url is None:
            url = self.detect_server_from_ip(ip)

        res, body = self.request_ip(url, ip)

        success = False
        response = {}

        if res.status == 200:
            response = json.loads(body)

            if self.fill:
                response = self._fill_data(response)

            success = True
        else:
            raise self._http_exception(res, body)

        return success, response

    def _fill_data(self, response):
        cidr = None

        cidrs = response.get('cidr0_cidrs')

        if cidrs:
            if len(cidrs) > 0:
                val = cidrs[0]

                cidr = val['v4prefix'] + '/' + str(val['length'])

        response['cidr'] = cidr

        primary_entity = None

        for entity in response['entities']:
            if not entity.get('vcardArray') or len(entity['vcardArray']) < 2:
                continue

            vcards = entity['vcardArray'][1]

            if vcards is None:
                continue

            entity_card = {}

            entity_card['handle'] = entity.get('handle')
            entity_card['roles'] = entity.get('roles')

            for vcard in vcards:
                if len(vcard) > 0:
                    if vcard[0] == 'fn':
                        entity_card['name'] = vcard[3]

                    if vcard[0] == 'adr':
                        entity_card['address'] = vcard[1]['label']

                        primary_entity = entity_card

                        break

            if primary_entity:
                break

        response['primary_entity'] = primary_entity

        country_updated = False

        if not response.get('country') and primary_entity:
            address = primary_entity['address'] if primary_entity['address'] is not None else None
            response['country'] = self.country_detector.detect_by_address(address)
            country_updated = True

        response['country_updated'] = country_updated

        return response

    def request_ip(self, url, ip=None):
        if ip is not None:
            url = url + 'ip/' + ip

        logging.info('RDAP_URL:' + url)

        res, body = self.request_http(url)

        return res, body

    def request_http(self, url, n=1, max_redirect=5):
        if n >= max_redirect:
            return None, None

        parsed_url = urlparse(url)
        host = parsed_url.hostname

        conn = self._create_http_connection(host)

        res = None
        body = None

        redirect = False

        try:
            conn.request('GET', parsed_url.path)

            res = conn.getresponse()

            if res.status == 200:
                body = res.read()
            elif res.status in (301, 302, 303, 307, 308):
                redirect = True
            else:
                body = res.read()
        except Exception as e:
            raise e
        finally:
            conn.close()

        if redirect:
            redirect_url = res.getheader('Location')

            res, body = self.request_http(redirect_url, n + 1)

        return res, body
