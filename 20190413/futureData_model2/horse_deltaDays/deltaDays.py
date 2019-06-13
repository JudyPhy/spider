###  从历史数据中获得马匹开始参赛时间，与比赛当天时间比对计算相差时长  ###
from config.myconfig import singleton_cfg
from db.database import singleton_Scrub_DB
import datetime
from common import common

RESULTS_TABLE = 'f_race_results_{0}'


def __calculateRaceBeginDates(horse_code_list):
    race_begin_date = {}  # horse_code & begin_date

    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select horse_code,race_date from {}'''.format(tableName))
            all_rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all_rows:
                code = row['horse_code'].strip()
                array_date = row['race_date'].split('/')
                race_date = int(array_date[2] + array_date[1] + array_date[0])
                if code in horse_code_list:
                    if code not in race_begin_date.keys():
                        race_begin_date[code] = race_date
                    else:
                        if race_date < race_begin_date[code]:
                            race_begin_date[code] = race_date
        else:
            common.log('deltaDays: table[' + tableName + '] not exist')
    return race_begin_date


def __getDeltaDays(begin_date, race_date):
    str_start_date = str(begin_date)
    year_from = int(str_start_date[:len(str_start_date) - 4])
    month_from = int(str_start_date[len(str_start_date) - 4 : len(str_start_date) - 2])
    day_from = int(str_start_date[len(str_start_date) - 2:])

    str_race_date = str(race_date)
    year_to = int(str_race_date[:len(str_race_date) - 4])
    month_to = int(str_race_date[len(str_race_date) - 4: len(str_race_date) - 2])
    day_to = int(str_race_date[len(str_race_date) - 2:])

    d_start = datetime.date(year_from, month_from, day_from)
    d_end = datetime.date(year_to, month_to, day_to)
    sumDay = d_end - d_start
    return sumDay.days


def getTodayDeltaDaysDict(today_rows):
    horse_code_list = []
    for row in today_rows:
        if row['horse_code'] not in horse_code_list:
            horse_code_list.append(row['horse_code'])
    # 从历史数据表获取各匹马开始参赛日期
    dict_begin_date = __calculateRaceBeginDates(horse_code_list)  # horse_code & begin_date

    # 遍历今日比赛马匹，计算得到马匹比赛时长
    deltaDaysDict = {}  # horse_code & deltaDays
    for row in today_rows:
        horse_code = row['horse_code']
        if horse_code not in dict_begin_date.keys():
            deltaDays = 0
        else:
            deltaDays = __getDeltaDays(dict_begin_date[horse_code], row['race_date'])
        deltaDaysDict[horse_code] = deltaDays
    return deltaDaysDict

