import requests
from requests import ConnectionError, ReadTimeout


def grab_from_url_content(url, headers = {'Accept': '* / *',
               'Accept-Language': 'zh-TW, zh; q=0.9, en-US; q=0.8, en; q=0.7, zh-CN; q=0.6',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
               }, timeout=10):
    
    rescontent = ''
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
        rescontent = res.text
    except ConnectionError as ce:
        print('ConnectionError: ' + str(ce))
        return grab_from_url_content(url)
    except ReadTimeout as rte:
        print('ReadTimeout: ' + str(rte))
        return grab_from_url_content(url)

    return rescontent


def grab_from_url_json(url, headers={'Accept': '* / *',
                                     'Accept-Language': 'zh-TW, zh; q=0.9, en-US; q=0.8, en; q=0.7, zh-CN; q=0.6',
                                     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3610.2 Safari/537.36'
                                     }, timeout=10):
    try:
        res = requests.get(url, headers=headers, timeout=timeout)
    except ConnectionError as ce:
        print ('ConnectionError: ' + str(ce))
        return grab_from_url_json(url, headers)
    except ReadTimeout as rte:
        print('ReadTimeout: ' + str(rte))
        return grab_from_url_json(url, headers)
    except Exception as ex:
        print (ex)

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
        print ('xxxxxxx' + str(ce))
        return grab_post_from_url_json(url, data, json, headers)
    except Exception as ex:
        print (ex)

    try:
        resjson = res.json()
        return resjson
    except ValueError as ve:
        return None
