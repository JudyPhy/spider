from common import common


def __getDct(race_date_No, horse_code, history_raceCard_rows):
    if (race_date_No in history_raceCard_rows.keys()) and (horse_code in history_raceCard_rows[race_date_No].keys()):
        return history_raceCard_rows[race_date_No][horse_code]['horse_wt_dec']
    print(race_date_No, horse_code, "can't find dct in history_raceCard_rows")
    return '-'


def __getDctTrend(horse_code, dct, history_raceResults_rows, history_raceCard_rows):
    sort_race_date_No = sorted(list(history_raceResults_rows.keys()))
    sort_race_date_No.reverse()
    for race_date_No in sort_race_date_No:
        dict = history_raceResults_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_dct = __getDct(race_date_No, horse_code, history_raceCard_rows)
            if plc not in common.words:
                return int(dct) - int(cur_dct)
    return 0


def GetDctTrend(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows):
    dct_trend_dict = {}  # race_date_No & {horse_No & dct_trend}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in dct_trend_dict.keys():
            dct_trend_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            dct = row['horse_wt_dec']
            dct_trend_dict[race_date_No][horse_No] = __getDctTrend(horse_code, dct, history_raceResults_rows, history_raceCard_rows)
    return dct_trend_dict


