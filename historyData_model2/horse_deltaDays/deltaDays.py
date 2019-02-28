###  计算马匹比赛时长  ###
from common import common
import datetime


def __calculateRaceBeginDate(race_rows):
    race_begin_date = {}  # horse_code & begin_date
    for row in race_rows:
        code = row['horse_code'].strip()
        if code not in race_begin_date.keys():
            race_begin_date[code] = row['race_date']
        else:
            if row['race_date'] < race_begin_date[code]:
                race_begin_date[code] = row['race_date']
    return race_begin_date


def __getDeltaDays(start_date, end_date):
    str_start_date = str(start_date)
    year_from = int(str_start_date[:len(str_start_date) - 4])
    month_from = int(str_start_date[len(str_start_date) - 4 : len(str_start_date) - 2])
    day_from = int(str_start_date[len(str_start_date) - 2:])

    str_end_date = str(end_date)
    year_to = int(str_end_date[:len(str_end_date) - 4])
    month_to = int(str_end_date[len(str_end_date) - 4: len(str_end_date) - 2])
    day_to = int(str_end_date[len(str_end_date) - 2:])

    d_start = datetime.date(year_from, month_from, day_from)
    d_end = datetime.date(year_to, month_to, day_to)
    sumDay = d_end - d_start
    return sumDay.days


def getDeltaDaysDict(history_rows):
    deltaDaysDict = {}  # new_race_id & {horse_code & deltaDays}
    dict_start_date = __calculateRaceBeginDate(history_rows)  # horse_code & begin_date
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        horse_code = row['horse_code']
        if new_race_id not in deltaDaysDict.keys():
            deltaDaysDict[new_race_id] = {}
        if horse_code not in dict_start_date.keys():
            deltaDays = 0
        else:
            deltaDays = __getDeltaDays(dict_start_date[horse_code], row['race_date'])
        deltaDaysDict[new_race_id][horse_code] = deltaDays
    return deltaDaysDict