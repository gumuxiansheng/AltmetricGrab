# coding:utf-8

import pandas as pd

from grab_util import grab_from_url_json


def grab_detail_plumx(file_url, dst_url, doi_column):
    dft = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in dft.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)

            # USAGE
            abstruct_views = list()
            full_text_views = list()
            link_click_count = list()
            link_outs = list()

            # CAPTURE
            exports_saves = list()
            reader_count_mendeley = list()
            reader_count_citeulike = list()

            # CITATION
            cited_by_count_scopus = list()
            cited_by_count_crossref = list()
            cited_by_count_pubmed = list()

            # SOCIAL MEDIA
            twitter = list()
            facebook = list()

            # MENTION
            news = list()
            blogs = list()
            reference_count_wikipedia = list()
            comment_count_reddit = list()
            mention_qa_site_mentions = list()

            a_list = [abstruct_views, full_text_views, link_click_count, link_outs, exports_saves,
                      reader_count_mendeley, reader_count_citeulike, cited_by_count_scopus,
                      cited_by_count_crossref, cited_by_count_pubmed, twitter, facebook, news, blogs,
                      reference_count_wikipedia, comment_count_reddit, mention_qa_site_mentions]
            b_list = ['abstruct_views', 'full_text_views', 'link_click_count', 'link_outs', 'exports_saves',
                      'reader_count_mendeley', 'reader_count_citeulike', 'cited_by_count_scopus',
                      'cited_by_count_crossref', 'cited_by_count_pubmed', 'twitter', 'facebook', 'news', 'blogs',
                      'reference_count_wikipedia', 'comment_count_reddit', 'mention_qa_site_mentions']

            for doi in df[doi_column]:

                if isinstance(doi, unicode):
                    print doi

                    abstruct_views_count, full_text_views_count, link_click_count_count, link_outs_count, \
                    exports_saves_count, reader_count_mendeley_count, reader_count_citeulike_count, \
                    cited_by_count_scopus_count, cited_by_count_crossref_count, \
                    cited_by_count_pubmed_count, twitter_count, facebook_count, news_count, blogs_count, \
                    reference_count_wikipedia_count, comment_count_reddit_count, mention_qa_site_mentions_count \
                        = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

                    res = grab_from_url_json('https://plu.mx/api/v1/artifact/doi/' + str(doi))
                    if res is not None:
                        if 'sort_count' in res:
                            sort_count = res['sort_count']

                            # USAGE
                            if 'usage' in sort_count:
                                print('USAGE')
                                counts = sort_count['usage']['count_types']
                                for item in counts:
                                    if item['name'] == 'ABSTRACT_VIEWS':
                                        abstruct_views_count = item['total']
                                    elif item['name'] == 'FULL_TEXT_VIEWS':
                                        full_text_views_count = item['total']
                                    elif item['name'] == 'LINK_CLICK_COUNT':
                                        link_click_count_count = item['total']
                                    elif item['name'] == 'LINK_OUTS':
                                        link_outs_count = item['total']

                            # CAPTURE
                            if 'capture' in sort_count:
                                print('CAPTURE')
                                counts = sort_count['capture']['count_types']
                                for item in counts:
                                    if item['name'] == 'EXPORTS_SAVES':
                                        exports_saves_count += item['total']
                                    elif item['name'] == 'READER_COUNT':
                                        for source in item['sources']:
                                            if source['name'] == 'Mendeley':
                                                reader_count_mendeley_count += source['total']
                                            elif source['name'] == 'CiteULike':
                                                reader_count_citeulike_count += source['total']

                            # CITATION
                            if 'citation' in sort_count:
                                print('CITATION')
                                counts = sort_count['citation']['count_types']
                                for item in counts:
                                    if item['name'] == 'Scopus':
                                        cited_by_count_scopus_count = item['total']
                                    elif item['name'] == 'CrossRef':
                                        cited_by_count_crossref_count = item['total']
                                    elif item['name'] == 'PubMed':
                                        cited_by_count_pubmed_count = item['total']

                            # SOCIAL MEDIA
                            if 'social_media' in sort_count:
                                print('SOCIAL MEDIA')
                                counts = sort_count['social_media']['count_types']
                                for item in counts:
                                    if item['name'] == 'TWEET_COUNT':
                                        twitter_count = item['total']
                                    elif item['name'] == 'FACEBOOK_COUNT':
                                        facebook_count = item['total']

                            # MENTION
                            if 'mention' in sort_count:
                                print('MENTION')
                                counts = sort_count['mention']['count_types']
                                for item in counts:
                                    if item['name'] == 'NEWS_COUNT':
                                        news_count = item['total']
                                    elif item['name'] == 'ALL_BLOG_COUNT':
                                        blogs_count = item['total']
                                    elif item['name'] == 'REFERENCE_COUNT':
                                        for source in item['sources']:
                                            if source['name'] == 'Wikipedia':
                                                reference_count_wikipedia_count += source['total']
                                    elif item['name'] == 'COMMENT_COUNT':
                                        for source in item['sources']:
                                            if source['name'] == 'Reddit':
                                                comment_count_reddit_count += source['total']
                                    elif item['name'] == 'QA_SITE_MENTIONS':
                                        mention_qa_site_mentions_count = item['total']

                    c_list = [abstruct_views_count, full_text_views_count, link_click_count_count, link_outs_count,
                              exports_saves_count, reader_count_mendeley_count, reader_count_citeulike_count,
                              cited_by_count_scopus_count, cited_by_count_crossref_count,
                              cited_by_count_pubmed_count, twitter_count, facebook_count, news_count, blogs_count,
                              reference_count_wikipedia_count, comment_count_reddit_count,
                              mention_qa_site_mentions_count]

                    for i in range(0, len(a_list)):
                        a_list[i].append(c_list[i])
                else:
                    for i in range(0, len(a_list)):
                        a_list[i].append(0)

            for i in range(0, len(a_list)):
                print len(a_list[i])
                df[b_list[i]] = a_list[i]

            df.to_excel(writer, sheet_name=sheet, index=False)
    return


# grab_detail_plumx('data/source/or64_1.xls', 'data/outputs/or64_plumx.xlsx', 'DOI')