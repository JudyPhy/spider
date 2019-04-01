from common import common


def getActTrend(raceCard_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    act_trend_dict = {}  # race_date_No & {horse_code & act_trend}
    temp_act = {}   # horse_code & prev_act
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in act_trend_dict.keys():
            act_trend_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            act = int(row['wt'])

            # 赛前
            if (horse_code not in temp_act.keys()):
                act_trend_dict[race_date_No][horse_code] = 0
            else:
                act_trend_dict[race_date_No][horse_code] = act - temp_act[horse_code]

            # 赛后
            temp_act[horse_code] = act

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, row['horse_wt_dec'])
            #     print(temp_act[horse_code])
            #     print(act_trend_dict[race_date_No][horse_code])
    return act_trend_dict


