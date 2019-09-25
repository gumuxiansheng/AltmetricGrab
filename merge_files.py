import os

import pandas as pd

from file_normalization import check_file_url


def read_file(file_, usecols=None):
    if str(file_).endswith('xlsx'):
        return pd.read_excel(file_, usecols=usecols)
    else:
        return pd.read_csv(file_, usecols=usecols)


def write_file(file_, dataframe):
    if str(file_).endswith('xlsx'):
        return dataframe.to_excel(file_, index=False)
    else:
        return dataframe.to_csv(file_, index=False)


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


def merge_altmetric_plumx_plos(alt_file_url, plu_file_url, plos_file_url, dst_url, alt_columns, plu_columns, plos_columns, merge_on):
    read_alt_cols = merge_on[:]
    read_alt_cols.extend(alt_columns)
    read_plu_cols = merge_on[:]
    read_plu_cols.extend(plu_columns)
    read_plos_cols = merge_on[:]
    read_plos_cols.extend(plos_columns)

    altmetric_df = read_file(alt_file_url, usecols=read_alt_cols)
    plumx_df = read_file(plu_file_url, usecols=read_plu_cols)
    plos_df = read_file(plos_file_url, usecols=read_plos_cols)

    for col in alt_columns:
        altmetric_df = altmetric_df.rename(columns={col: col + '_alt'})

    for col in plu_columns:
        plumx_df = plumx_df.rename(columns={col: col + '_plu'})

    for col in plos_columns:
        plos_df = plos_df.rename(columns={col: col + '_plo'})

    df_save = pd.merge(altmetric_df, plumx_df, how='inner', on=merge_on)
    df_save = pd.merge(df_save, plos_df, how='inner', on=merge_on)

    # print df_save

    write_file(dst_url, df_save)
    return


# merge_on=['SO', 'DI'] alt_columns=['twitter', 'facebook', 'wikipedia', 'redditors', 'f1000']
# plu_columns=['twitter', 'facebook', 'comment_count_reddit']
# plos_columns = ['soical_FACEBOOK_COUNT', 'soical_TWEET_COUNT']
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


def merge_altmetric_plumx_plos_all(alt_folder, plu_folder, plos_folder, dst_folder):
    check_file_url(dst_folder)
    file_list = os.listdir(alt_folder)
    for file_ in file_list:
        print file_
        if not (str(file_).endswith('xlsx') or str(file_).endswith('csv')):
            continue
        alt_file_url = (alt_folder if str(alt_folder).endswith(os.path.sep) else (alt_folder + os.path.sep)) + file_
        plu_file_url = (plu_folder if str(plu_folder).endswith(os.path.sep) else (plu_folder + os.path.sep)) + file_
        plos_file_url = (plos_folder if str(plos_folder).endswith(os.path.sep) else (plos_folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        merge_altmetric_plumx_plos(alt_file_url, plu_file_url, plos_file_url, dst_url,
                              alt_columns=['Alt_Tweeters', 'Alt_Facebook_Pages', 'Alt_Wikipedia_Pages ', 'Alt_Redditors'],
                              plu_columns=['soical_FACEBOOK_COUNT', 'soical_TWEET_COUNT'],
                              plos_columns=['Twitter Total', 'Wikipedia Total'],
                              merge_on=['SO', 'DI'])

    return


def append_altmetric_plumx_all(folder):
    file_list = os.listdir(folder)
    df_save = pd.DataFrame()
    file_list.sort()
    for file_ in file_list:
        print file_
        if not (str(file_).endswith('xlsx') or str(file_).endswith('csv')):
            continue
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        df = read_file(file_url)
        df_save = df_save.append(df)

    df_save = df_save.drop_duplicates()
    df_save.to_excel((folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + 'all.xlsx',
                     index=False)

    return


def merge_plumx_elsevier_springer_views(plu_file_url, els_file_url, spr_file_url, dst_url, plu_columns, els_columns,
                                        spr_columns, merge_on):
    read_plu_cols = merge_on[:]
    read_plu_cols.extend(plu_columns)
    read_els_cols = merge_on[:]
    read_els_cols.extend(els_columns)
    read_spr_cols = merge_on[:]
    read_spr_cols.extend(spr_columns)

    plumx_df = pd.read_excel(plu_file_url, usecols=read_plu_cols)
    elsevier_df = pd.read_excel(els_file_url, usecols=read_els_cols)
    springer_df = pd.read_excel(spr_file_url, usecols=read_spr_cols)

    for col in plu_columns:
        plumx_df = plumx_df.rename(columns={col: col + '_plu'})

    for col in els_columns:
        elsevier_df = elsevier_df.rename(columns={col: col + '_els'})

    for col in spr_columns:
        springer_df = springer_df.rename(columns={col: col + '_spr'})

    df_save = pd.merge(plumx_df, elsevier_df, how='inner', on=merge_on)
    df_save = pd.merge(df_save, springer_df, how='inner', on=merge_on)

    df_save.to_excel(dst_url, index=False)
    return


def merge_plumx_elsevier_springer_views_all(plu_folder, els_folder, spr_folder, dst_folder):
    check_file_url(dst_folder)
    file_list = os.listdir(plu_folder)
    for file_ in file_list:
        print file_
        if not str(file_).endswith('xlsx'):
            continue
        plu_file_url = (plu_folder if str(plu_folder).endswith(os.path.sep) else (plu_folder + os.path.sep)) + file_
        els_file_url = (els_folder if str(els_folder).endswith(os.path.sep) else (els_folder + os.path.sep)) + file_
        spr_file_url = (spr_folder if str(spr_folder).endswith(os.path.sep) else (spr_folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        merge_plumx_elsevier_springer_views(plu_file_url, els_file_url, spr_file_url, dst_url,
                                            plu_columns=['abstruct_views', 'full_text_views', 'exports_saves'],
                                            els_columns=['views', 'citations'],
                                            spr_columns=['downloads', 'citationsx'],
                                            merge_on=['SO', 'DI'])

    return
