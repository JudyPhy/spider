from common import common


def __getAct(race_date_No, horse_code, history_raceCard_rows):
    if (race_date_No in history_raceCard_rows.keys()) and (horse_code in history_raceCard_rows[race_date_No].keys()):
        return history_raceCard_rows[race_date_No][horse_code]['wt']
    print(race_date_No, horse_code, "can't find act in history_raceCard_rows")
    return '-'


def __getActTrend(horse_code, act, history_raceResults_rows, history_raceCard_rows):
    sort_race_date_No = sorted(list(history_raceResults_rows.keys()))
    sort_race_date_No.reverse()
    for race_date_No in sort_race_date_No:
        dict = history_raceResults_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_act = __getAct(race_date_No, horse_code, history_raceCard_rows)
            if plc not in common.words:
                return act - int(cur_act)
    return 0


def GetActTrend(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows):
    act_trend_dict = {}  # race_date_No & {horse_No & act_trend}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in act_trend_dict.keys():
            act_trend_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            act = int(row['wt'])
            act_trend_dict[race_date_No][horse_No] = __getActTrend(horse_code, act, history_raceResults_rows, history_raceCard_rows)
    return act_trend_dict


