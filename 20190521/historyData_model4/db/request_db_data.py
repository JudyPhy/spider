from db.database import singleton_Scrub_DB
from common import common
import datetime


def RequestSortedHistoryRaceCardRows(race_date):
    history_race_card_rows = {}  # race_date_No & {horse_code * row}
    now = datetime.datetime.now()
    if singleton_Scrub_DB.table_exists(common.RECE_CARD_TABLE):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date>=20140000 and race_date<%s'.format(common.RECE_CARD_TABLE), race_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            horse_name = row['horse']
            if '(Withdrawn)' not in horse_name:
                cur_race_date = row['race_date']
                race_No = row['race_No']
                race_date_No = cur_race_date + common.toDoubleDigitStr(race_No)
                if race_date_No not in history_race_card_rows.keys():
                    history_race_card_rows[race_date_No] = {}
                horse_code = row['horse_code']
                history_race_card_rows[race_date_No][horse_code] = row
    else:
        print('dragon: Table[', common.RECE_CARD_TABLE, '] not exist.')

    sort_history_race_card_rows = {}  # race_date_No & {horse_code & row}
    sort_race_date_No_list = sorted(history_race_card_rows.keys())
    for race_date_No in sort_race_date_No_list:
        if race_date_No not in sort_history_race_card_rows.keys():
            sort_history_race_card_rows[race_date_No] = history_race_card_rows[race_date_No]
    return sort_history_race_card_rows


def RequestFutureRaceCardRows(race_date):
    today_race_card_rows = {}   # race_date_No & {horse_No * row}
    future_table = common.FUTURE_RECE_CARD_TABLE
    if singleton_Scrub_DB.table_exists(future_table):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date=%s'.format(future_table), race_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            horse_name = row['horse']
            if '(Withdrawn)' not in horse_name:
                race_No = row['race_No']
                race_date_No = race_date + common.toDoubleDigitStr(race_No)
                if race_date_No not in today_race_card_rows.keys():
                    today_race_card_rows[race_date_No] = {}
                horse_No = row['horse_No']
                today_race_card_rows[race_date_No][horse_No] = row
            else:
                print('exit race horse:', row)
    else:
        print('dragon: Table[', future_table, '] not exist.')
    print('today race count=', len(today_race_card_rows))
    return today_race_card_rows


def RequestSortedHistoryRaceResultsRows(race_date):
    history_race_results_rows = {}    # race_date_No & {horse_code & row}
    tableName = common.RESULTS_TABLE
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date>="20140000" and race_date<%s'.format(tableName), race_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            plc = row['plc']
            if plc not in common.words:
                cur_race_date = row['race_date']
                race_No = row['race_No']
                race_date_No = cur_race_date + common.toDoubleDigitStr(race_No)
                if race_date_No not in history_race_results_rows.keys():
                    history_race_results_rows[race_date_No] = {}
                horse_code = row['horse_code'].strip()
                history_race_results_rows[race_date_No][horse_code] = row
    else:
        print('dragon: Table[', tableName, '] not exist.')

    sort_history_race_results_rows = {}  # race_date_No & {horse_code & row}
    sort_race_date_No_list = sorted(history_race_results_rows.keys())
    for race_date_No in sort_race_date_No_list:
        if race_date_No not in sort_history_race_results_rows.keys():
            sort_history_race_results_rows[race_date_No] = history_race_results_rows[race_date_No]
    return sort_history_race_results_rows


def __toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def RequestImmdLatestRows(race_date):
    temp_row_dict = {}   # race_No & {horse_No & [row, update_time]}
    tableName = common.ODDS_TABLE.replace('{0}', race_date[: len(race_date) - 4])
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date=%s'.format(tableName), race_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            race_no = row['race_no']
            if race_no not in temp_row_dict.keys():
                temp_row_dict[race_no] = {}
            horse_no = row['horse_no']
            cur_row_update_time = row['win_update_time']
            if cur_row_update_time == '':
                cur_row_update_time = row['pla_update_time']
            if horse_no not in temp_row_dict[race_no].keys():
                temp_row_dict[race_no][horse_no] = [row, cur_row_update_time]

            prev_update_time = __toDateTime(temp_row_dict[race_no][horse_no][1])
            if __toDateTime(cur_row_update_time) > prev_update_time:
                temp_row_dict[race_no][horse_no] = [row, cur_row_update_time]

    lastest_dict = {}  # race_date_No & {horse_No & row}
    for race_No, dict in temp_row_dict.items():
        race_date_No = race_date + common.toDoubleDigitStr(race_No)
        if race_date_No not in lastest_dict.keys():
            lastest_dict[race_date_No] = {}
        for horse_no, row_time in dict.items():
            lastest_dict[race_date_No][horse_no] = row_time[0]
    return lastest_dict


def RequestHorsePedigreeRows():
    horse_pedigree_rows = {}  # horse_code & row
    if singleton_Scrub_DB.table_exists(common.PEDIGREE_TABLE):
        singleton_Scrub_DB.cursor.execute('select * from {}'.format(common.PEDIGREE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            horse_code = row['code'].strip()
            if horse_code not in horse_pedigree_rows.keys():
                horse_pedigree_rows[horse_code] = row
            else:
                print('horse[', horse_code, '] in pedigree table repeat.')
    return horse_pedigree_rows


def RequestHistoryDisplaySectionalTimeRows(race_date):
    display_sectional_time_rows = {}  # race_date_No & {horse_code & row}
    tableName = common.HORSE_SECTIONAL_TIME_TABLE
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {} where race_date<%s'.format(tableName), race_date)
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
            if race_date_No not in display_sectional_time_rows.keys():
                display_sectional_time_rows[race_date_No] = {}
            horse_code = row['horse_code'].strip()
            display_sectional_time_rows[race_date_No][horse_code] = row
    return display_sectional_time_rows


def RequestSectionalOdds():
    odds_sectional_rows = {}    # race_date_No & {horse_No & row}
    tableName = common.ODDS_SECTIONAL_TABLE
    if singleton_Scrub_DB.table_exists(tableName):
        singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            race_date = row['race_date']
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            if race_date_No not in odds_sectional_rows.keys():
                odds_sectional_rows[race_date_No] = {}
            horse_No = row['horse_No']
            odds_sectional_rows[race_date_No][horse_No] = row
    return odds_sectional_rows

