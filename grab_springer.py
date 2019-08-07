# coding:utf-8
import os

import pandas as pd

from file_normalization import check_file_url
from grab_util import grab_from_url_content


def grab_springer_info(file_url, dst_url, doi_column):
    df = pd.ExcelFile(file_url)

    with pd.ExcelWriter(dst_url, engine='openpyxl') as writer:
        for sheet in df.sheet_names:
            print sheet
            df = pd.read_excel(file_url, sheet_name=sheet)

            downloads = []
            citations = []

            for doi in df[doi_column]:

                downloads_number = 0
                citations_number = 0
                if isinstance(doi, unicode):
                    res = grab_from_url_content('https://link.springer.com/article/' + doi)
                    downloads_anchor = '<span class="article-metrics__views">'
                    citations_anchor = '<span id="citations-count-number" class="test-metric-count c-button-circle gtm-citations-count">'

                    # downloads
                    start_index = res.find(downloads_anchor)
                    if start_index > 0:
                        start_index += len(downloads_anchor)
                        end_index = res.find('</span>', start_index, start_index + 100)
                        downloads_number_temp = res[start_index: end_index]

                        if downloads_number_temp is not '':
                            downloads_number = downloads_number_temp

                    # citations
                    start_index = res.find(citations_anchor)
                    if start_index > 0:
                        start_index += len(citations_anchor)
                        end_index = res.find('</span>', start_index, start_index + 100)
                        citations_number_temp = res[start_index: end_index]

                        if citations_number_temp is not '':
                            citations_number = citations_number_temp

                downloads.append(downloads_number)
                citations.append(citations_number)

            df['downloads'] = downloads
            df['citationsx'] = citations
            df.to_excel(writer, sheet_name=sheet, index=False)
    return


def grab_springer_all(folder, dst_folder, doi_column):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        grab_springer_info(file_url, dst_url, doi_column)

    return
# grab_springer_info('data/outputs/or64_elsevier.xlsx', 'data/outputs/or64_elsevier_y.xlsx', 'DOI')