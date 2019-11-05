import requests
from requests import ConnectionError


def grab_from_url_content(url):
    headers = {'Accept': '* / *',
               'Accept-Language': 'zh-TW, zh; q=0.9, en-US; q=0.8, en; q=0.7, zh-CN; q=0.6',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
               }
    res = requests.get(url, headers=headers)
    rescontent = res.content

    return rescontent


def grab_from_url_json(url, headers={'Accept': '* / *',
                                     'Accept-Language': 'zh-TW, zh; q=0.9, en-US; q=0.8, en; q=0.7, zh-CN; q=0.6',
                                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
                                     }):
    try:
        res = requests.get(url, headers=headers)
    except ConnectionError as ce:
        print 'xxxxxxx' + str(ce)
        res = requests.get(url, headers=headers)
    except Exception as ex:
        print ex

    try:
        resjson = res.json()
        return resjson
    except ValueError as ve:
        return None

def grab_post_from_url_json(url, data=None, json=None, headers={'Accept': '* / *',
                                     'Accept-Language': 'zh-TW, zh; q=0.9, en-US; q=0.8, en; q=0.7, zh-CN; q=0.6',
                                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
                                     }):
    try:
        res = requests.post(url, data, json, headers=headers)
    except ConnectionError as ce:
        print 'xxxxxxx' + str(ce)
        res = requests.get(url, headers=headers)
    except Exception as ex:
        print ex

    try:
        resjson = res.json()
        return resjson
    except ValueError as ve:
        return None
