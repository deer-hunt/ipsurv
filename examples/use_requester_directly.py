from ipsurv.requester.http import HttpRequester

'''
Using requester directly.

Specification:
- Using HttpRequester class.

Command:
python3 use_requester_directly.py
'''


if __name__ == '__main__':
    http = HttpRequester(timeout=10.0)

    url = 'https://www.wikipedia.org/'

    res, body = http.request_http(url)

    print('HTTP status:' + str(res.status))
    print('HTTP body:')
    print(body)
