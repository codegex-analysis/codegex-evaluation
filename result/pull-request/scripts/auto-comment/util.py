import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def get_requests(url, headers):
    session = requests.Session()
    retry = Retry(connect=20, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.get(url, headers=headers)
    return response


def post_requests(url, params, headers, proxies):
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    response = session.post(url=url, data=json.dumps(params), headers=headers, proxies=proxies)
    return response



