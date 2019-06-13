from config.myconfig import singleton_cfg
from db.db import singleton_ResultsDb
from db.db import singleton_ScrubDb
from common import common
import datetime


def getTodayTable():
    today_dict = {}  # update_table & {race_no & {horse_no & row}}
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if update_table not in today_dict.keys():
            today_dict[update_table] = {}
        if singleton_ResultsDb.table_exists(update_table):
            singleton_ResultsDb.cursor.execute('select * from {}'.format(update_table))
            rows = singleton_ResultsDb.cursor.fetchall()
            singleton_ResultsDb.connect.commit()
            for row in rows:
                race_no = row['race_no']
                horse_no = row['horse_no']
                if race_no not in today_dict[update_table].keys():
                    today_dict[update_table][race_no] = {}
                today_dict[update_table][race_no][horse_no] = row
        else:
            print('today table[', update_table, '] not exist')

        # count = 0
        # for race_no, dict in today_dict[update_table].items():
        #     count += len(dict)
        # print('today_dict:', count)

    return today_dict


def __parseRaceStartTime(race_time):
    array_race_time = race_time.split(':')
    if len(array_race_time) == 2:
        race_start_hour = int(array_race_time[0])
        race_start_min = int(array_race_time[1])
    else:
        race_start_hour = 0
        race_start_min = 0
    return race_start_hour, race_start_min


def __getBeforeTenMinutsTime(race_date, race_start_time):
    race_start_year = int(race_date[: len(race_date) - 4])
    race_start_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
    race_start_day = int(race_date[len(race_date) - 2:])
    race_start_hour, race_start_min = __parseRaceStartTime(race_start_time)
    if race_start_min >= 10:
        race_start_min -= 10
    else:
        race_start_hour -= 1
        race_start_min = 60 + race_start_min - 10
    return datetime.datetime(race_start_year, race_start_month, race_start_day, race_start_hour, race_start_min, 0)


def getTodayRaceStartTime():
    start_time_dict = {}  # race_No & [start_time, before10_time]
    race_date = singleton_cfg.getRaceDate()
    year = race_date[: len(race_date) - 4]
    tableName = common.FUTURE_RACE_CARD_TABLE.replace('{0}', year)
    singleton_ScrubDb.cursor.execute('select * from {} where race_date=%s'.format(tableName), race_date)
    rows = singleton_ScrubDb.cursor.fetchall()
    singleton_ScrubDb.connect.commit()
    for row in rows:
        race_No = row['race_No']
        if race_No not in start_time_dict.keys():
            start_time = row['race_time']
            before10 = __getBeforeTenMinutsTime(race_date, start_time)
            start_time_dict[race_No] = [start_time, before10]
    return start_time_dict

