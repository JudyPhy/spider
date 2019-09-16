from common import common
import datetime


def __getRest(prev_race_date, cur_race_date):
    prev_year = int(prev_race_date[: (len(prev_race_date) - 4)])
    prev_month = int(prev_race_date[(len(prev_race_date) - 4): (len(prev_race_date) - 2)])
    prev_day = int(prev_race_date[(len(prev_race_date) - 2):])
    cur_year = int(cur_race_date[: (len(cur_race_date) - 4)])
    cur_month = int(cur_race_date[(len(cur_race_date) - 4): (len(cur_race_date) - 2)])
    cur_day = int(cur_race_date[(len(cur_race_date) - 2):])
    prev_time = datetime.datetime(prev_year, prev_month, prev_day)
    cur_time = datetime.datetime(cur_year, cur_month, cur_day)
    deltaDays = (cur_time - prev_time).days
    return deltaDays


def GetHorseRest(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_rest_dict = {}  # race_date_No & {horse_code & rest}
    temp_horse_race_date_prev = {}  # horse_code & prev_date
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_rest_dict.keys():
            horse_rest_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_date = race_date_No[:len(race_date_No) - 2]
                    if horse_code not in temp_horse_race_date_prev.keys():
                        temp_horse_race_date_prev[horse_code] = cur_date
                    # before
                    horse_rest_dict[race_date_No][horse_code] = __getRest(temp_horse_race_date_prev[horse_code], cur_date)
                    # after
                    temp_horse_race_date_prev[horse_code] = cur_date
    return horse_rest_dict

