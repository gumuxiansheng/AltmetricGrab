# coding:utf-8
import os

import pandas as pd

from file_normalization import check_file_url
from grab_util import grab_from_url_json

apiKey = '7f59af901d2d86f78a1fd60c1bf9426a'


def grab_scopus_eid(file_url, dst_url, doi_column):
    df = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in df.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)
            eids = list()

            for doi in df[doi_column]:
                eid = ''
                if isinstance(doi, unicode):
                    url = "https://api.elsevier.com/content/search/scopus?query=doi(%s)&apiKey=%s" % (doi, apiKey)
                    res = grab_from_url_json(url, headers={'Accept': 'application/json'})
                    if res is not None:
                        if 'search-results' in res and 'entry' in res['search-results'] and len(
                                res['search-results']['entry']) > 0:
                            print res['search-results']['entry']
                            entry = res['search-results']['entry'][0]
                            if 'eid' in entry:
                                eid = entry['eid']

                eids.append(eid)
            df['eid'] = eids

            df.to_excel(writer, sheet_name=sheet, index=False)
    return


def grab_mendeley_views(file_url, dst_url, eid_column, end_year=30000, end_month=12):
    df = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in df.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)
            views_list = []
            citations_list = []

            for eid in df[eid_column]:
                views = 0
                citations = 0
                if isinstance(eid, unicode):
                    url = 'https://www.mendeley.com/stats/articles/timeline/' + eid
                    print url
                    res = grab_from_url_json(url, headers={'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                                           'accept-encoding': 'gzip, deflate, br',
                                                           'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
                                                           'cache-control': 'max-age=0',
                                                           'cookie': '__cfduid=d39abdb2dd2db28e2dc87090bc01940471552616801; _pendo_visitorId.63e37363-87d4-41d6-430e-06d0a2dfe6dc=26904907488095089043874038443321464321; aa_usr=%7B%22accessType%22%3A%22ae%3AREG%3AU_P%3AGUEST%3A%22%2C%22accountId%22%3A%22ae%3A293744%22%2C%22accountName%22%3A%22ae%3AMendeley%20Guests%22%2C%22userId%22%3A%22ae%3A34829421%22%7D; _pendo_accountId.63e37363-87d4-41d6-430e-06d0a2dfe6dc=ae%3A293744; _pendo_meta.63e37363-87d4-41d6-430e-06d0a2dfe6dc=2263585050; _at=MSwxNTYxNjE0MTE0NDQ1LDUyODM1ODEwMSwzMzg3LGFsbCwsLDg5OTBjZThlOTAzNTAzNDI0YjBiNzYyNjU2MDYzM2U3MjY2OGd4cnFhLDkxN2ExZTBhLWJiOGMtMzU2NS04MWIwLTAyYjY3MTZjYjJkZCxoNlQ3Wno0N2x3UlphTFRrRE5QWmlsai1udjg; web_session=7e191aca-d4ea-466b-95fe-1ac265566e4d; utt=c5d61aecf1a5c617cad58b7a5edf841774a5d04-IT; msso=4%3A4c1d7ba4-f1d7-4b1e-ada2-1b3d098e280f; node_session=eyJpZCI6IjJkNTgwMzBhLTYzMWQtNDRiYS1iYzAxLWViM2MwYWYxNGE0MyIsInN0YXRlIjoiZWQ4Mjk1ZGZkZDljM2VkZWU0MGU1ZGVkMDA4OGE4ZDgiLCJyZWZlcnJlclVybCI6Imh0dHA6Ly93d3cubWVuZGVsZXkuY29tL3N0YXRzL2FydGljbGVzL3RpbWVsaW5lLzItczIuMC04NDg3NzgxNjc4MyIsImlzU29mdFNpZ25JbiI6ZmFsc2UsInByb21wdCI6ImxvZ2luIiwiYW5hbHl0aWNzSW5mbyI6bnVsbCwiaW5kdklkZW50aXR5IjoiUkVHIiwiaW5jbHVkZVByb21wdGVkU3RhdHVzIjpudWxsfQ==; node_session.sig=Mp4VH9Z9WYIRdOn_qsjlwuxGbR8; acw=412f999c872fe14e076a5ac841c0e5afc9a0gxrqa%7C%24%7CF5CB1AB37B06B90EEA530C0B6F146354A9E602A26D39CD1530CC9846BC13A30E5E8E26C5F066FBC4183FF302082A8D430F09C6CA9E0485BD62776E7F424B0CB4F0B571C956AE28B38657AD137B42AAB4',
                                                           'sec-fetch-mode': 'navigate',
                                                           'sec-fetch-site': 'cross-site',
                                                           'upgrade-insecure-requests': '1',
                                                           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.10 Safari/537.36'})
                    for item in res:
                        if item['year'] > end_year or (item['year'] == end_year and item['month'] > end_month):
                            continue

                        print item
                        views += item['views']
                        citations += item['citations']

                views_list.append(views)
                citations_list.append(citations)

            print views_list
            print citations_list
            df['views'] = views_list
            df['citations'] = citations_list

            df.to_excel(writer, sheet_name=sheet, index=False)
    return


def grab_scopus_eid_all(folder, dst_folder, doi_column):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    finished_list = os.listdir(dst_folder)
    for file_ in file_list:
        if file_ in finished_list:
            continue
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        grab_scopus_eid(file_url, dst_url, doi_column)

    return


def grab_mendeley_views_all(folder, dst_folder, eid_column):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        grab_mendeley_views(file_url, dst_url, eid_column)

    return
# grab_mendeley_views('data/outputs/or64_elsevier.xlsx', 'data/outputs/or64_elsevier_x.xlsx', 'eid', end_year=2018)
# ge.grab_scopus_eid_all(u'data/outputs/能源化工元源数据文件/'.encode('utf-8'), u'data/outputs/能源化工元源数据文件_elsevier/'.encode('utf-8'), 'DI')
# ge.grab_mendeley_views_all(u'data/outputs/能源化工元源数据文件_elsevier/'.encode('utf-8'), u'data/outputs/能源化工元源数据文件_elsevier/'.encode('utf-8'), 'eid')