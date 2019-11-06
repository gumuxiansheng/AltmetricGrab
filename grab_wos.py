# coding:utf-8
import json

import requests
import pandas as pd


def grab_wos_journals():
    url = "https://mjl.clarivate.com/api/jprof/public/rank-search"

    headers = {
        'authorization': "Bearer eyJraWQiOiJ0b2tlbi5wYS5rZXkuMjAxOV8wNV8xMF8wMSIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxZDA3MzEzMC1mZmE4LTExZTktYjcxOS03N2FiMzBlMWVmYzgiLCIxcDp0eXBlIjoiUEEiLCIxcDpwcmQiOiJzdGVhbSIsIjFwOmFwcCI6ImNlbnN1YiIsImlzcyI6Imh0dHBzOlwvXC9hY2Nlc3MuY2xhcml2YXRlLmNvbSIsIjFwOmZubSI6Ik1pa2UiLCIxcDp0cnVpZHMiOlsiMWQwNzMxMzAtZmZhOC0xMWU5LWI3MTktNzdhYjMwZTFlZmM4Il0sIjFwOmVtbCI6InpodXl1YW4yNzA2QHNpbmEuY29tIiwiMXA6cHJvZHVjdHMiOltdLCIxcDpsb2dpbnR5cGUiOiJTVEVBTV9MT0dJTiIsImF1ZCI6ImNlbnN1YiIsIjFwOmhvc3QiOiJodHRwczpcL1wvYWNjZXNzLmNsYXJpdmF0ZS5jb20iLCIxcDp1cmkiOiJodHRwczpcL1wvbWpsLmNsYXJpdmF0ZS5jb21cL2xvZ2luO2NyZWF0ZUFjY291bnQ9ZmFsc2U7cmVmZXJyZXI9JTJGaG9tZSIsIjFwOnBpZCI6IjEyNTMyMTgzIiwiMXA6bG5tIjoiWmh1IiwiMXA6dHB3ZCI6ZmFsc2UsIjFwOmxucyI6IjUwMCw1MDAiLCIxcDpwZW1sIjoiemh1eXVhbjI3MDZAc2luYS5jb20iLCIxcDpsbHQiOjE1NzI5NDQwOTYsImV4cCI6MTU3Mjk4NzI5NiwiaWF0IjoxNTcyOTQ0MDk2LCJqdGkiOiIxMzc4OTY2Yy1iOGMxLTQ1ZmYtYmFmYS03MzFkOGYzYjQ3ZWMifQ.G-QHbIHmPWMMQWfUoCqE8VTJwXfuXXtzDnbdW12zzYsT0X6PvM47TP98iON4Fagi-eQ68lIfjt4k3RweQWMrzDNi62NOiyYhZ2AUjSvCv-UyC3WWyLYPLwg3x08cQX2i7_ew-pRzrLNzGQOplgFjhCrVQ78zgqz0bGRSiztHljMHfeM9c2rlYf5rKIyW63IcUNDNJp9gxIAdJbe5pd7TPOgA2Vu1NGr1OASvnWcHO9z2LpYlln61kl42I_56QiAsObUjoaevEgs2XX-LKNbxJhs2ZD19XnJyG2lzJkZWiTm8bEHR4iPVatQoORPTrXvhMjdoUElP2TCvVMzYZPK3ww",
        'Content-Type': "application/json",
        'access-control-allow-origin': "*",
        'accept': "application/json, text/plain, */*",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.8 Safari/537.36",
        'x-1p-session': "668e7215-bd70-4a2e-a737-3f580f12a00c",
        'sec-fetch-site': "same-origin",
        'sec-fetch-mode': "cors",
        'referer': "https://mjl.clarivate.com/search-results",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6",
        'cookie': "sp=dea9b277-51c8-4be5-9c7f-15ecfea83d23, _ga=GA1.2.1704346315.1564798973, _vwo_uuid_v2=D6AD987C2C4B4C63D67D9311327DA523A|15fc42dccdc374aec7d9a90db2af0c9b, _vwo_uuid=D6AD987C2C4B4C63D67D9311327DA523A, REMEMBER_ME=\"066caf8b42dba42fd50a6d9285ce26337a687566757975616e406d696b657a68752e636e\", _vis_opt_s=2%7C, _vis_opt_test_cookie=1, _vwo_ds=3%3Aa_0%2Ct_0%3A0%241572835107%3A44.30133469%3A%3A%3A3_0%2C2_0%3A0, _dd_r=1, _dd=f3351ff7-f245-41e1-a833-a84e35da9413, _sp_ses.2f26=*, USERNAME=\"zhufuyuan@mikezhu.cn\", PSSID=\"H3-iiMiBCGVJoVCHLx2FEx2B5IRczx2BXVxxx2BAyJcw-18x2dA31M3qetaLIVa0lgrsEC0Qx3Dx3DL3X34ydMxxiBvx2BBIXDJ1gnQx3Dx3D-qBgNuLRjcgZrPm66fhjx2Fmwx3Dx3D-h9tQNJ9Nv4eh45yLvkdX3gx3Dx3D\", CUSTOMER_NAME=\"zhufuyuan@mikezhu.cn\", E_GROUP_NAME=\"IC2 Platform\", CUSTOMER_GROUP_ID=\"12088522\", ACCESS_METHOD=\"UNP\", _hjid=3e3c1d28-a70f-4f3d-a43a-cd6accd8d5f8, _vwo_sn=107888%3A6, _gcl_au=1.1.884212387.1572943880, _hjDonePolls=451006,451017,451016,451005,451004,451021,451019,450989,451236, _hjMinimizedPolls=451006,451017,451016,451005,451004,451021,451236, _sp_id.2f26=f72cb22d-69cd-4d2e-9477-5eddfb440d8a.1564800925.5.1572945465.1570959272.668e7215-bd70-4a2e-a737-3f580f12a00c, sp=dea9b277-51c8-4be5-9c7f-15ecfea83d23, _ga=GA1.2.1704346315.1564798973, _vwo_uuid_v2=D6AD987C2C4B4C63D67D9311327DA523A|15fc42dccdc374aec7d9a90db2af0c9b, _vwo_uuid=D6AD987C2C4B4C63D67D9311327DA523A, REMEMBER_ME=\"066caf8b42dba42fd50a6d9285ce26337a687566757975616e406d696b657a68752e636e\", _vis_opt_s=2%7C, _vis_opt_test_cookie=1, _vwo_ds=3%3Aa_0%2Ct_0%3A0%241572835107%3A44.30133469%3A%3A%3A3_0%2C2_0%3A0, _dd_r=1, _dd=f3351ff7-f245-41e1-a833-a84e35da9413, _sp_ses.2f26=*, USERNAME=\"zhufuyuan@mikezhu.cn\", PSSID=\"H3-iiMiBCGVJoVCHLx2FEx2B5IRczx2BXVxxx2BAyJcw-18x2dA31M3qetaLIVa0lgrsEC0Qx3Dx3DL3X34ydMxxiBvx2BBIXDJ1gnQx3Dx3D-qBgNuLRjcgZrPm66fhjx2Fmwx3Dx3D-h9tQNJ9Nv4eh45yLvkdX3gx3Dx3D\", CUSTOMER_NAME=\"zhufuyuan@mikezhu.cn\", E_GROUP_NAME=\"IC2 Platform\", CUSTOMER_GROUP_ID=\"12088522\", ACCESS_METHOD=\"UNP\", _hjid=3e3c1d28-a70f-4f3d-a43a-cd6accd8d5f8, _vwo_sn=107888%3A6, _gcl_au=1.1.884212387.1572943880, _hjDonePolls=451006,451017,451016,451005,451004,451021,451019,450989,451236, _hjMinimizedPolls=451006,451017,451016,451005,451004,451021,451236, _sp_id.2f26=f72cb22d-69cd-4d2e-9477-5eddfb440d8a.1564800925.5.1572945465.1570959272.668e7215-bd70-4a2e-a737-3f580f12a00c",
        'Cache-Control': "no-cache",
        'Postman-Token': "92626fe6-4eec-4529-b831-1d65957f6732,f5fa242e-1103-4684-88ba-3c81c5694910",
        'Host': "mjl.clarivate.com",
        'Content-Length': "442",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    for i in range(1, 9300 / 50 + 2):
        print (i)
        payload = "{\n\t\"searchValue\": \"\",\n\t\"pageNum\": " + str(
            i) + ",\n\t\"pageSize\": 50,\n\t\"sortOrder\": [{\n\t\t\"name\": \"RELEVANCE\",\n\t\t\"order\": \"DESC\"\n\t}],\n\t\"filters\": [{\n\t\t\"filterName\": \"COVERED_LATEST_JEDI\",\n\t\t\"matchType\": \"BOOLEAN_EXACT\",\n\t\t\"caseSensitive\": false,\n\t\t\"values\": [{\n\t\t\t\"type\": \"VALUE\",\n\t\t\t\"value\": \"true\"\n\t\t}]\n\t}, {\n\t\t\"filterName\": \"PRODUCT_CODE\",\n\t\t\"matchType\": \"TEXT_EXACT\",\n\t\t\"caseSensitive\": false,\n\t\t\"values\": [{\n\t\t\t\"type\": \"VALUE\",\n\t\t\t\"value\": \"D\"\n\t\t}]\n\t}]\n}"

        response = requests.request("POST", url, data=payload, headers=headers)
        save_file = 'Journals/scie_' + str(i) + '.json'
        save_file = open(save_file, 'w+')
        save_file.write(response.content)
        save_file.close()


def merge_journals():
    load_list = []
    for i in range(1, 9300 / 50 + 2):
        with open('Journals/scie_' + str(i) + '.json', 'r') as f:
            load_list.extend(json.load(f)['journalProfiles'])

    with open("Journals/scie_all.json", "w") as dump_f:
        dump_f.write(json.dumps(load_list))


def save_csv():
    columns = ['publicationId', 'publicationSeqNo', 'issn', 'eissn', 'publicationTitle', 'publicationTitle20',
               'publicationTitleISO', 'publicationFrequency', 'issuesPerYear', 'submissionURL',
               'openAccess', 'country', 'publicationStartYear', 'publisherName', 'publisherAddress',
               'publisherCode', 'publisherURL']
    df = pd.DataFrame(columns=columns)
    with open("Journals/scie_all.json", "r") as f:
        load_list = json.load(f)
        for i in range(len(load_list)):
            item_dict = {}
            for col in columns:
                if col in load_list[i]['journalProfile'].keys():
                    item_dict[col] = load_list[i]['journalProfile'][col]
            df = df.append(item_dict, ignore_index=True)

    df.to_csv('Journals/scie_all.csv', encoding='utf-8', index=False)
    return


def count_categories():
    categories_list = []
    with open("Journals/scie_all.json", "r") as f:
        load_list = json.load(f)
        for i in range(len(load_list)):
            for cat in load_list[i]['journalProfile']['categories']:
                if cat['categoryDescription'] not in categories_list:
                    categories_list.append(cat['categoryDescription'])

    categories_list.sort()
    with open("Journals/scie_categories.txt", "w") as f:
        f.write(json.dumps(categories_list))
    return categories_list


def flatten_categories():
    categories = count_categories()
    df = pd.DataFrame(columns=['publicationId'] + categories)
    with open("Journals/scie_all.json", "r") as f:
        load_list = json.load(f)
        for i in range(len(load_list)):
            item_dict = {'publicationId': load_list[i]['journalProfile']['publicationId']}
            for cat in load_list[i]['journalProfile']['categories']:
                item_dict[cat['categoryDescription']] = 1

            df = df.append(item_dict, ignore_index=True)
    df = df.fillna(0)
    df_o = pd.read_csv('Journals/scie_all.csv')
    df_o = df_o.merge(df, on='publicationId')

    df_o.to_csv('Journals/scie_allx.csv', encoding='utf-8', index=False)
    return
