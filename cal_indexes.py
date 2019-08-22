import numpy as np
import pandas as pd
import os
from file_normalization import check_file_url


# h-index
def cal_h_index(work_list):
    i = 0
    for info in sorted(work_list, reverse=True):
        i += 1
        if info < i:
            return i - 1


# sub-impact
def cal_sub_impact(work_list, thresh=1000.0):
    i = 0
    sum = 0
    for info in sorted(work_list, reverse=True):
        sum += info
        i += 1
        if sum < thresh:
            return thresh / i


def cal_file(file_url, dst_url, col_names, so='SO'):
    df = pd.read_excel(file_url)

    df_save = pd.DataFrame()
    df_save['indexes'] = col_names
    print ('file ......' + file_url)
    h_indexes = []
    for col_name in col_names:
        works = list(df[col_name].values)
        h_indexes.append(cal_h_index(works))
    df_save['h_index'] = h_indexes
    df_save['SO'] = df[so][0:len(col_names)]
    df_save.to_excel(dst_url, index=False)


def cal_file_folder(folder, dst_folder, col_names):
    check_file_url(dst_folder)
    file_list = os.listdir(folder)
    finished_list = os.listdir(dst_folder)
    for file_ in file_list:
        if (folder != dst_folder) and (file_ in finished_list):
            continue
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + file_
        cal_file(file_url, dst_url, col_names)

    return


def cal_file_df(file_url, col_names, so='SO'):
    df = pd.read_excel(file_url)

    df_save = pd.DataFrame()
    df_save['SO'] = [df[so][0]]
    print ('file ......' + file_url)
    for col_name in col_names:
        works = list(df[col_name].values)
        df_save[col_name] = [cal_h_index(works)]

    return df_save


def cal_file_folder_df(folder, dst_url, col_names):
    file_list = os.listdir(folder)
    df_save = pd.DataFrame(columns=['SO'].extend(col_names))
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        df = cal_file_df(file_url, col_names)

        df_save = df_save.append(df)

    df_save.to_excel(dst_url, index=False)


def cal_file_sub_impact(file_url, threshes=None, so='SO', tc='TC'):
    if threshes is None:
        threshes = [100, 500, 1000, 2000, 3000, 4000, 5000]

    df = pd.read_excel(file_url)

    df_save = pd.DataFrame()
    df_save['SO'] = [df[so][0]]
    print ('file ......' + file_url)
    for thresh in threshes:
        works = list(df[tc].values)
        df_save[str(thresh)] = [cal_sub_impact(works, thresh)]

    return df_save


def cal_file_folder_sub_impact_df(folder, dst_url):
    file_list = os.listdir(folder)
    df_save = pd.DataFrame()
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        df = cal_file_sub_impact(file_url)

        df_save = df_save.append(df)

    df_save.to_excel(dst_url, index=False)