# coding:utf-8

import pandas as pd
import urlparse
import math

from grab_util import grab_from_url_content, grab_from_url_json


def grab_detail_plumx(file_url, dst_url, doi_column):
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

            a_list = [news, blogs, policy, twitter, weibo, facebook, wikipedia, redditors, f1000, video, dimensions_citation, mendeley, citeulike]
            b_list = ['news', 'blogs', 'policy', 'twitter', 'weibo', 'facebook', 'wikipedia', 'redditors', 'f1000', 'video', 'dimensions_citation', 'mendeley', 'citeulike']

            for doi in df[doi_column]:

                if doi != '' and not math.isnan(doi):
                    doi = int(doi)
                    news_anchor = 'news</dt><dd><a href="/details/' + str(doi) + '/news"><strong>'
                    blogs_anchor = 'blogs</dt><dd><a href="/details/' + str(doi) + '/blogs"><strong>'
                    policy_anchor = 'policy</dt><dd><a href="/details/' + str(doi) + '/policy-documents"><strong>'
                    twitter_anchor = 'twitter</dt><dd><a href="/details/' + str(doi) + '/twitter"><strong>'
                    weibo_anchor = 'weibo</dt><dd><a href="/details/' + str(doi) + '/weibo"><strong>'
                    facebook_anchor = 'facebook</dt><dd><a href="/details/' + str(doi) + '/facebook"><strong>'
                    wikipedia_anchor = 'wikipedia</dt><dd><a href="/details/' + str(doi) + '/wikipedia"><strong>'
                    redditors_anchor = 'reddit</dt><dd><a href="/details/' + str(doi) + '/reddit"><strong>'
                    f1000_anchor = 'f1000</dt><dd><a href="/details/' + str(doi) + '/f1000"><strong>'
                    video_anchor = 'video</dt><dd><a href="/details/' + str(doi) + '/video"><strong>'
                    dimensions_citation_anchor = 'dimensions_citation</dt><dd><a href="/details/' + str(doi) + '/citations"><strong>'
                    mendeley_anchor = 'mendeley</dt><dd><a href="/details/' + str(doi) + '#mendeley-demographics"><strong>'
                    citeulike_anchor = 'citeulike</dt><dd><strong>'
                    c_list = [news_anchor, blogs_anchor, policy_anchor, twitter_anchor, weibo_anchor, facebook_anchor,
                              wikipedia_anchor, redditors_anchor, f1000_anchor, video_anchor,
                              dimensions_citation_anchor, mendeley_anchor, citeulike_anchor]

                    end_anchor = '</strong>'

                    res = grab_from_url_content('https://www.altmetric.com/details/' + str(doi))
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