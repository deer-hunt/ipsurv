from ipsurv.requester.geoip import GeoIpRequester

'''
Using requester directly.

Specification:
- Using GeoIpRequester class.

Command:
python3 geoip_requester_directly.py
'''


if __name__ == '__main__':
    ip = '8.8.8.8'

    geoip = GeoIpRequester()

    # Auto detect data path.
    geoip.initialize()

    response = geoip.request_city(ip)
    print('request_city:')
    print(response, "\n")

    response = geoip.request_country(ip)
    print('request_country:')
    print(response, "\n")

    response = geoip.request_asn(ip)
    print('request_asn:')
    print(response, "\n")

    # Specify data path.
    geoip = GeoIpRequester()

    geoip.initialize('/usr/local/share/GeoIP/', {'country': 'GeoLite2-Country.mmdb', 'city': 'GeoLite2-City.mmdb', 'asn': 'GeoLite2-ASN.mmdb'})

    response = geoip.request_city(ip)
    print('request_city:')
    print(response, "\n")

    response = geoip.request_country(ip)
    print('request_country:')
    print(response, "\n")

    response = geoip.request_asn(ip)
    print('request_asn:')
    print(response, "\n")
