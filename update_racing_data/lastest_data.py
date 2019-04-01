from db.db import singleton_ScrubDb
import datetime
from config.myconfig import singleton_cfg

ODDS_TABLE = 'pla_win_odds_{0}'


def __toDateTime(time_str):  # time_str: %Y-%m-%d %H:%M:%S
    return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')


def getLastestRows():
    race_date = singleton_cfg.getRaceDate()
    temp_row_dict = {}   # race_no & {horse_no & [row, update_time]}
    tableName = ODDS_TABLE.replace('{0}', race_date[: len(race_date) - 4])
    if singleton_ScrubDb.table_exists(tableName):
        singleton_ScrubDb.cursor.execute('select * from {} where race_date=%s'.format(tableName), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        singleton_ScrubDb.connect.commit()
        for row in rows:
            race_no = row['race_no']
            if race_no not in temp_row_dict.keys():
                temp_row_dict[race_no] = {}
            horse_no = row['horse_no']
            if horse_no not in temp_row_dict[race_no].keys():
                if row['win_update_time'] != '':
                    temp_row_dict[race_no][horse_no] = [row, row['win_update_time']]
                else:
                    temp_row_dict[race_no][horse_no] = [row, row['pla_update_time']]

            prev_update_time = __toDateTime(temp_row_dict[race_no][horse_no][1])
            if (row['win_update_time'] != '') and (__toDateTime(row['win_update_time']) > prev_update_time):
                temp_row_dict[race_no][horse_no] = [row, row['win_update_time']]

            prev_update_time = __toDateTime(temp_row_dict[race_no][horse_no][1])
            if (row['pla_update_time'] != '') and (__toDateTime(row['pla_update_time']) > prev_update_time):
                temp_row_dict[race_no][horse_no] = [row, row['pla_update_time']]

    lastest_dict = {}  # race_no & {horse_no & row}
    for race_no, dict in temp_row_dict.items():
        if race_no not in lastest_dict.keys():
            lastest_dict[race_no] = {}
        for horse_no, row_time in dict.items():
            lastest_dict[race_no][horse_no] = row_time[0]

    # count = 0
    # for race_no, dict in lastest_dict.items():
    #     count += len(dict)
    # print(race_date, 'odds rows count=', count)

    return lastest_dict


