# coding:utf-8

import pandas as pd
import urlparse
import math
import os

from file_normalization import check_file_url
from grab_util import grab_from_url_content, grab_from_url_json


def grab_detail_id_altmetric(file_url, dst_url, doi_column):
    df = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in df.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)
            if 'citation_id' not in df.columns:
                detail_ids = list()

                for doi in df[doi_column]:
                    detail_id = ''
                    if isinstance(doi, unicode):
                        res = grab_from_url_json('https://api.altmetric.com/v1/doi/' + doi)
                        if res is not None:
                            details_url = res['details_url']
                            if details_url is not '':
                                detail_id = urlparse.parse_qs(urlparse.urlparse(details_url).query).get('citation_id')[0]

                    detail_ids.append(detail_id)
                df['citation_id'] = detail_ids

            df.to_excel(writer, sheet_name=sheet, index=False)
    return


def grab_altmetric_total_score(file_url, dst_url, doi_column):
    df = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in df.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)
            if 'altmetric_score' not in df.columns:
                scores = []

                for doi in df[doi_column]:
                    score = 0
                    if isinstance(doi, unicode):
                        res = grab_from_url_json('https://api.altmetric.com/v1/doi/' + doi)
                        if res is not None:
                            score = res['score']

                    scores.append(score)
                df['altmetric_score'] = scores

            df.to_excel(writer, sheet_name=sheet, index=False)
    return


def grab_detail_altmetric(file_url, dst_url, citation_id_column):
    dft = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in dft.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)
            print len(df)
            news = list()
            blogs = list()
            policy = list()
            twitter = list()
            weibo = list()
            facebook = list()
            wikipedia = list()
            redditors = list()
            f1000 = list()
            video = list()
            dimensions_citation = list()
            mendeley = list()
            citeulike = list()

            a_list = [news, blogs, policy, twitter, weibo, facebook, wikipedia, redditors, f1000, video,
                      dimensions_citation, mendeley, citeulike]
            b_list = ['news', 'blogs', 'policy', 'twitter', 'weibo', 'facebook', 'wikipedia', 'redditors', 'f1000',
                      'video', 'dimensions_citation', 'mendeley', 'citeulike']

            for citation_id in df[citation_id_column]:

                if citation_id != '' and not math.isnan(citation_id):
                    citation_id = int(citation_id)
                    news_anchor = 'news</dt><dd><a href="/details/' + str(citation_id) + '/news"><strong>'
                    blogs_anchor = 'blogs</dt><dd><a href="/details/' + str(citation_id) + '/blogs"><strong>'
                    policy_anchor = 'policy</dt><dd><a href="/details/' + str(
                        citation_id) + '/policy-documents"><strong>'
                    twitter_anchor = 'twitter</dt><dd><a href="/details/' + str(citation_id) + '/twitter"><strong>'
                    weibo_anchor = 'weibo</dt><dd><a href="/details/' + str(citation_id) + '/weibo"><strong>'
                    facebook_anchor = 'facebook</dt><dd><a href="/details/' + str(citation_id) + '/facebook"><strong>'
                    wikipedia_anchor = 'wikipedia</dt><dd><a href="/details/' + str(
                        citation_id) + '/wikipedia"><strong>'
                    redditors_anchor = 'reddit</dt><dd><a href="/details/' + str(citation_id) + '/reddit"><strong>'
                    f1000_anchor = 'f1000</dt><dd><a href="/details/' + str(citation_id) + '/f1000"><strong>'
                    video_anchor = 'video</dt><dd><a href="/details/' + str(citation_id) + '/video"><strong>'
                    dimensions_citation_anchor = 'dimensions_citation</dt><dd><a href="/details/' + str(
                        citation_id) + '/citations"><strong>'
                    mendeley_anchor = 'mendeley</dt><dd><a href="/details/' + str(
                        citation_id) + '#mendeley-demographics"><strong>'
                    citeulike_anchor = 'citeulike</dt><dd><strong>'
                    c_list = [news_anchor, blogs_anchor, policy_anchor, twitter_anchor, weibo_anchor, facebook_anchor,
                              wikipedia_anchor, redditors_anchor, f1000_anchor, video_anchor,
                              dimensions_citation_anchor, mendeley_anchor, citeulike_anchor]

                    end_anchor = '</strong>'

                    res = grab_from_url_content('https://www.altmetric.com/details/' + str(citation_id))
                    if res is not None:

                        for i in range(0, len(c_list)):
                            start_index = res.find(c_list[i])
                            if start_index > 0:
                                start_index += len(c_list[i])
                                number = 0
                                end_index = res.find(end_anchor, start_index, start_index + 100)
                                number_temp = res[start_index: end_index]

                                if number_temp is not '':
                                    number = number_temp
                                a_list[i].append(int(number))
                            else:
                                a_list[i].append(0)
                    else:
                        for i in range(0, len(a_list)):
                            a_list[i].append(0)
                else:
                    for i in range(0, len(a_list)):
                        a_list[i].append(0)

            for i in range(0, len(a_list)):
                df[b_list[i]] = a_list[i]

            df.to_excel(writer, sheet_name=sheet, index=False)
    return


def grab_detail_id_altmetric_all(folder, dst_folder, doi_column):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        grab_detail_id_altmetric(file_url, dst_url, doi_column)

    return


def grab_detail_altmetric_all(folder, dst_folder, citation_id_column):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    finished_list = os.listdir(dst_folder)
    for file_ in file_list:
        if file_ in finished_list:
            continue
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        grab_detail_altmetric(file_url, dst_url, citation_id_column)

    return


def grab_altmetric_total_score_all(folder, dst_folder, doi_column):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    finished_list = os.listdir(dst_folder)
    for file_ in file_list:
        if (folder != dst_folder) and (file_ in finished_list):
            continue
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        grab_altmetric_total_score(file_url, dst_url, doi_column)

    return

# gadc.grab_detail_id_altmetric_all(u'data/outputs/数学期刊(下)/'.encode('utf-8'), u'data/outputs/数学期刊(下)/'.encode('utf-8'), 'DI')
# gadc.grab_detail_altmetric_all(u'data/outputs/数学期刊(下)/'.encode('utf-8'), u'data/outputs/数学期刊(下)_altmetric/'.encode('utf-8'), 'citation_id')