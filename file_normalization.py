# coding:utf-8


import codecs
import os
import pandas as pd


def check_file_url(fpath):
    """
    check the file path, if not exists, create the path.
    :param fpath: the path url string
    :return: the origin path string
    """
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # create the destination path
    return fpath


def correct_csv_encode(url, origin_encoding='utf-16le', dst_encoding='utf-8'):
    with codecs.open(url, "r", encoding=origin_encoding) as f:
        file_data = f.read()
        decoded_str = file_data.encode(dst_encoding)
        if decoded_str.startswith(codecs.BOM_UTF8):
            decoded_str = decoded_str.replace(codecs.BOM_UTF8, '')
        file_data = decoded_str
    with open(url, "w") as f:
        f.write(file_data)


def correct_csv_tab(url, dst_url):
    with codecs.open(url, "r", encoding='utf-8') as f:
        file_data = f.readline()
        print file_data
        if file_data.endswith('\r'):
            print 'x'
            file_data = file_data.replace('\r', '\t\r')
        elif file_data.endswith('\r\n'):
            print 'y'
            file_data = file_data.replace('\r\n', '\t\r\n')
        elif file_data.endswith('\n'):
            print 'z'
            file_data = file_data.replace('\n', '\t\n')
        file_data += f.read()
    with codecs.open(url, "w", encoding='utf-8') as f:
        f.write(file_data)

    df = pd.read_csv(url, sep='\t')
    print df.head()
    df.to_excel(str(dst_url).replace('.csv', '.xlsx').replace('.CSV', '.xlsx'), encoding='utf-8', index=False, engine='openpyxl')


def correct_all_files(folder, dst_folder):
    check_file_url(dst_folder)

    file_list = os.listdir(folder)
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        correct_csv_encode(file_url)
        correct_csv_tab(file_url, str(dst_folder + file_))
