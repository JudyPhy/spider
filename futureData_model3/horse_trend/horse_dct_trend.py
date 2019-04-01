from common import common


def getDctTrend(raceCard_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    dct_trend_dict = {}  # race_date_No & {horse_code & dct_trend}
    temp_dct = {}   # horse_code & prev_dct
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in dct_trend_dict.keys():
            dct_trend_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            dct = row['horse_wt_dec']
            if '\xa0' in dct:
                # 无效马匹
                dct = -1
            else:
                dct = int(dct)

            # 赛前
            if (horse_code not in temp_dct.keys()) or (dct == -1):
                dct_trend_dict[race_date_No][horse_code] = 0
            else:
                dct_trend_dict[race_date_No][horse_code] = dct - temp_dct[horse_code]

            # 赛后
            if dct == -1:
                # 无效马匹不记录本场比赛
                continue
            temp_dct[horse_code] = dct

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, row['horse_wt_dec'])
            #     print(temp_dct[horse_code])
            #     print(dct_trend_dict[race_date_No][horse_code])
    return dct_trend_dict


