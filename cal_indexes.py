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
def cal_sub_impact(work_list, thresh=0.1):
    i = 0
    sum_ = 0
    tc = sum(work_list) * thresh
    for info in sorted(work_list, reverse=True):
        sum_ += info
        i += 1
        if sum_ + 1e-5 >= tc:
            return float(tc / float(i))


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


def cal_file_sub_impact(file_url, so='SO', tc='TC'):
    threshes = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    df = pd.read_excel(file_url)

    df_save = pd.DataFrame()
    df_save['SO'] = [df[so][0]]
    for thresh in threshes:
        works = list(df[tc].values)
        df_save[str(thresh)] = [cal_sub_impact(works, thresh)]

    df_save['sub_impact'] = (df_save['0.1'] * 10 + df_save['0.2'] * 9 + df_save['0.3'] * 8 + df_save['0.4'] * 7 + \
                             df_save['0.5'] * 6 + df_save['0.6'] * 5 + df_save['0.7'] * 4 + df_save['0.8'] * 3 + \
                             df_save['0.9'] * 2 + df_save['1'] * 1) / 55
    return df_save


def cal_file_folder_sub_impact_df(folder, dst_folder, dst_f_name, tc='TC'):
    check_file_url(dst_folder)

    file_list = os.listdir(folder)
    df_save = pd.DataFrame()
    for file_ in file_list:
        print file_
        file_url = (folder if str(folder).endswith(os.path.sep) else (folder + os.path.sep)) + file_
        df = cal_file_sub_impact(file_url, tc=tc)

        df_save = df_save.append(df)

    dst_url = (dst_folder if str(dst_folder).endswith(os.path.sep) else (dst_folder + os.path.sep)) + dst_f_name
    df_save.to_excel(dst_url, index=False)
