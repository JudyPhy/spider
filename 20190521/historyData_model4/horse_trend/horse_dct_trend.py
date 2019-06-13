from common import common


def GetHorseDctTrend(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_dct_trend_dict = {}  # race_date_No & {horse_code & dct_trend}
    temp_horse_dct_prev = {}   # horse_code & prev_dct
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_dct_trend_dict.keys():
            horse_dct_trend_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_dct_prev.keys():
                        temp_horse_dct_prev[horse_code] = -1
                    cur_dct = int(row['horse_wt_dec'])
                    # before
                    if temp_horse_dct_prev[horse_code] == -1:
                        horse_dct_trend_dict[race_date_No][horse_code] = 0
                    else:
                        horse_dct_trend_dict[race_date_No][horse_code] = cur_dct - temp_horse_dct_prev[horse_code]
                    # after
                    temp_horse_dct_prev[horse_code] = cur_dct
    return horse_dct_trend_dict


