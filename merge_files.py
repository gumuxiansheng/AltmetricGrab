import os

import pandas as pd

from file_normalization import check_file_url


def merge_altmetric_plumx(alt_file_url, plu_file_url, dst_url, alt_columns, plu_columns, merge_on):
    read_alt_cols = merge_on[:]
    read_alt_cols.extend(alt_columns)
    read_plu_cols = merge_on[:]
    read_plu_cols.extend(plu_columns)

    altmetric_df = pd.read_excel(alt_file_url, usecols=read_alt_cols)
    plumx_df = pd.read_excel(plu_file_url, usecols=read_plu_cols)

    for col in alt_columns:
        altmetric_df = altmetric_df.rename(columns={col: col + '_alt'})

    for col in plu_columns:
        plumx_df = plumx_df.rename(columns={col: col + '_plu'})

    df_save = pd.merge(altmetric_df, plumx_df, how='inner', on=merge_on)

    # print df_save

    df_save.to_excel(dst_url, index=False)
    return


# merge_on=['SO', 'DI'] alt_columns=['twitter', 'facebook', 'wikipedia', 'redditors', 'f1000']
# plu_columns=['twitter', 'facebook', 'comment_count_reddit']
# mf.merge_altmetric_plumx('data/outputs/OR_altmetric/1.xlsx', 'data/outputs/OR_Plumx/1.xlsx', 'data/outputs/OR_merge/1.xlsx', alt_columns=['twitter', 'facebook', 'wikipedia', 'redditors', 'f1000'], plu_columns=['twitter', 'facebook', 'comment_count_reddit'], merge_on=['SO', 'DI'])


def merge_altmetric_plumx_all(alt_folder, plu_folder, dst_folder):
    check_file_url(dst_folder)
    file_list = os.listdir(alt_folder)
    for file_ in file_list:
        print file_
        if not str(file_).endswith('xlsx'):
            continue
        alt_file_url = (alt_folder if str(alt_folder).endswith(os.path.sep) else (alt_folder + os.path.sep)) + file_
        plu_file_url = (plu_folder if str(plu_folder).endswith(os.path.sep) else (plu_folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        merge_altmetric_plumx(alt_file_url, plu_file_url, dst_url,
                              alt_columns=['twitter', 'facebook', 'wikipedia', 'redditors', 'f1000'],
                              plu_columns=['twitter', 'facebook', 'reference_count_wikipedia', 'comment_count_reddit'],
                              merge_on=['SO', 'DI'])

    return


def append_altmetric_plumx_all(folder):
    file_list = os.listdir(folder)
    df_save = pd.DataFrame()
    file_list.sort()
    for file_ in file_list:
        print file_
        if not str(file_).endswith('xlsx'):
            continue
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        df = pd.read_excel(file_url)
        df_save = df_save.append(df)

    df_save = df_save.drop_duplicates()
    df_save.to_excel((folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + 'all.xlsx',
                     index=False)

    return
