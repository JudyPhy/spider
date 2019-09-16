from db.db import singleton_ScrubDb
from db.db import singleton_ResultsDb
from config.myconfig import singleton_cfg
import datetime
from common import common

IMMD_TABLE = 'dd_odds_immd'

RACE_RESULTS_TABLE = 'ff_race_results'

RACE_CARD_HISTORY_TABLE = 'tt_race_card_history'

RACE_CARD_FUTURE_TABLE = 'tt_race_card_future'

DISPLAY_SECTIONAL_TIME_TABLE = 'gg_display_sectional_time'


def RequestImmdRows(race_date):
    immd_rows = {}   # race_No & {horse_No & [rows]}
    if singleton_ScrubDb.table_exists(IMMD_TABLE):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date=%s'.format(IMMD_TABLE), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_No = row['race_No']
            if race_No not in immd_rows.keys():
                immd_rows[race_No] = {}
            horse_No = row['horse_No']
            if horse_No not in immd_rows[race_No].keys():
                immd_rows[race_No][horse_No] = []
            immd_rows[race_No][horse_No].append(row)
    return immd_rows


def RequestLastestRows(race_date):
    immd_rows = RequestImmdRows(race_date)
    lastest_rows = {}  # race_No & {horse_No & row}
    for race_No, dict in immd_rows.items():
        if race_No not in lastest_rows.keys():
            lastest_rows[race_No] = {}
        for horse_No, rows in dict.items():
            for row in rows:
                if horse_No not in lastest_rows[race_No].keys():
                    lastest_rows[race_No][horse_No] = row
                else:
                    prev_update_time = common.toDateTime(lastest_rows[race_No][horse_No]['update_time'])
                    cur_update_time = common.toDateTime(row['update_time'])
                    if cur_update_time > prev_update_time:
                        lastest_rows[race_No][horse_No] = row
    return lastest_rows


def RequestTodayTableRows():
    today_table_rows = {}  # update_table & {race_No & {horse_No & row}}
    update_table_list = singleton_cfg.getUpdateTableList()
    for update_table in update_table_list:
        if singleton_ResultsDb.table_exists(update_table):
            if update_table not in today_table_rows.keys():
                today_table_rows[update_table] = {}
            singleton_ResultsDb.cursor.execute('select * from {}'.format(update_table))
            rows = singleton_ResultsDb.cursor.fetchall()
            singleton_ResultsDb.connect.commit()
            for row in rows:
                race_No = row['race_no']
                if race_No not in today_table_rows[update_table].keys():
                    today_table_rows[update_table][race_No] = {}
                horse_No = row['horse_no']
                today_table_rows[update_table][race_No][horse_No] = row
        else:
            print('today table[', update_table, '] not exist')
    return today_table_rows


def RequestRaceResultsRows(race_date):
    race_results_rows = {}   # race_date_No & {horse_code & row}
    if singleton_ScrubDb.table_exists(RACE_RESULTS_TABLE):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date<%s and race_date>="20140101"'.format(RACE_RESULTS_TABLE), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
            if race_date_No not in race_results_rows.keys():
                race_results_rows[race_date_No] = {}
            horse_code = row['horse_code']
            race_results_rows[race_date_No][horse_code] = row
    return race_results_rows


def RequestRaceCardHistoryRows(race_date):
    race_card_rows = {}   # race_date_No & {horse_code & row}
    if singleton_ScrubDb.table_exists(RACE_CARD_HISTORY_TABLE):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date<%s'.format(RACE_CARD_HISTORY_TABLE), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
            if race_date_No not in race_card_rows.keys():
                race_card_rows[race_date_No] = {}
            horse_code = row['horse_code']
            race_card_rows[race_date_No][horse_code] = row
    return race_card_rows


def RequestDisplaySectionalTimeRows(race_date):
    sectional_time_rows = {}   # race_date_No & {horse_code & row}
    if singleton_ScrubDb.table_exists(DISPLAY_SECTIONAL_TIME_TABLE):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date<%s'.format(DISPLAY_SECTIONAL_TIME_TABLE), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
            if race_date_No not in sectional_time_rows.keys():
                sectional_time_rows[race_date_No] = {}
            horse_code = row['horse_code']
            sectional_time_rows[race_date_No][horse_code] = row
    return sectional_time_rows


def RequestTodayRaceStartTime(race_date):
    today_year = int(race_date[: (len(race_date) - 4)])
    today_month = int(race_date[(len(race_date) - 4): (len(race_date) - 2)])
    today_day = int(race_date[(len(race_date) - 2):])
    start_time_dict = {}  # race_date_No & [start_time, before10_time, before20_time]
    if singleton_ScrubDb.table_exists(RACE_CARD_FUTURE_TABLE):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date=%s'.format(RACE_CARD_FUTURE_TABLE), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_date_No = race_date + common.toDoubleDigitStr(row['race_No'])
            array_start_time = row['race_time'].split(':')
            cur_start_time_hour = int(array_start_time[0])
            cur_start_time_min = int(array_start_time[1])
            cur_start_time = datetime.datetime(today_year, today_month, today_day, cur_start_time_hour, cur_start_time_min, 0)
            if race_date_No not in start_time_dict.keys():
                before10 = cur_start_time - datetime.timedelta(minutes=10)
                before20 = cur_start_time - datetime.timedelta(minutes=20)
                start_time_dict[race_date_No] = [cur_start_time, before10, before20]
            else:
                prev_start_time = start_time_dict[race_date_No][0]
                if (cur_start_time - prev_start_time).total_seconds() < 0:
                    start_time_dict[race_date_No][0] = cur_start_time
    return start_time_dict

