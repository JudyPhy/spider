import datetime
from common import common


def __getDeltaDays(prev_race_date, cur_race_date):
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


def getRest(horse_code, race_date, race_results_rows):
    sort_race_date_No = sorted(list(race_results_rows.keys()))
    sort_race_date_No.reverse()
    for race_date_No in sort_race_date_No:
        dict = race_results_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                cur_race_date = dict[horse_code]['race_date']
                return __getDeltaDays(cur_race_date, race_date)
    return 0


