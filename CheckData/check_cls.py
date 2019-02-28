from db.db import singleton_ScrubDB
from db.db import singleton_ResultsDB
# from db.db import singleton_otherDB
from common import common
import gx_data


error_key_list = []


# def getGXTableRows(tableName):
#     if singleton_otherDB.table_exists(tableName):
#         singleton_otherDB.cursor.execute('select * from {}'.format(tableName))
#         rows = singleton_otherDB.cursor.fetchall()
#         singleton_otherDB.connect.commit()
#         return rows
#     return []


def getResultsTableRows(tableName):
    if singleton_ResultsDB.table_exists(tableName):
        singleton_ResultsDB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_ResultsDB.cursor.fetchall()
        singleton_ResultsDB.connect.commit()
        return rows
    return []


def getScrubTableRows(tableName):
    if singleton_ScrubDB.table_exists(tableName):
        singleton_ScrubDB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
        return rows
    print('table[', tableName, '] not exist in scrub')
    return []


def compareHistoryAndToday(table_history, table_today):
    print('compare:', table_history, ' & ', table_today)
    rows_history = getResultsTableRows(table_history)
    rows_today = getResultsTableRows(table_today)
    key_list = rows_today[0].keys()
    exKey = ['id', 'race_id', 'pla_odds', 'plc', 'win_odds']
    for row_today in rows_today:
        race_date = row_today['race_date']
        race_no = row_today['race_no']
        horse_no = row_today['horse_no']
        print('\n', race_date, race_no, horse_no)
        find = False
        for row_history in rows_history:
            if (row_history['race_date'] == race_date) and (row_history['race_no'] == race_no) and (row_history['horse_no'] == horse_no):
                find = True
                for key in key_list:
                    if (key not in exKey) and (row_history[key] != row_today[key]):
                        log = True
                        if (key == 'horse_total_allRace') and (row_history[key] == row_today[key] + 1):
                            log = False
                        if (key == 'horse_star_3_allRace') and (row_history['plc'] == 4) and (row_history[key] == row_today[key] + 1):
                            log = False
                        if (key == 'horse_star_2_allRace') and (row_history['plc'] == 3) and (row_history[key] == row_today[key] + 1):
                            log = False
                        if (key == 'horse_star_1_allRace') and (row_history['plc'] == 2) and (row_history[key] == row_today[key] + 1):
                            log = False
                        if (key == 'horse_star_0_allRace') and (row_history['plc'] == 1) and (row_history[key] == row_today[key] + 1):
                            log = False
                        if (key == 'raceDays') and (row_history[key] == row_today[key] - 1):
                            log = False
                        if (key == 'go_aversr') and (abs(row_history[key] - row_today[key]) < 0.01):
                            log = False
                        if (key == 'dis_avesr') and (abs(row_history[key] - row_today[key]) < 0.01):
                            log = False
                        if log:
                            common.log(key + '=>history:' + str(row_history[key]) + ', today:' + str(row_today[key]))
        if not find:
            common.log(str(race_date) + ',race_no[' + str(race_no) + '],horse_no[' + str(horse_no) + '] find not in history data')


def compareTwoTable(table1, table2):
    rows_table1 = getResultsTableRows(table1)
    rows_table2 = getResultsTableRows(table2)
    exKeys = ['id', 'updateTime']
    # print(rows_table1[0].keys())
    diffrent_dict = {}  # key & raceInfo
    for row_2 in rows_table2:
        race_date = row_2['race_date']
        race_no = row_2['race_no']
        horse_no = row_2['horse_no']
        # print('\n', race_date, race_no, horse_no)
        find = False
        for row_1 in rows_table1:
            if (row_1['race_date'] == race_date) and (row_1['race_no'] == race_no) and (row_1['horse_no'] == horse_no):
                find = True
                keys = row_1.keys()
                for key in keys:
                    if key in exKeys:
                        continue
                    elif row_1[key] != row_2[key]:
                        if key not in diffrent_dict.keys():
                            diffrent_dict[key] = {}
                        diffrent_dict[key]['race_date'] = race_date
                        diffrent_dict[key]['race_no'] = race_no
                        diffrent_dict[key]['horse_no'] = horse_no
                        diffrent_dict[key]['table1'] = row_1[key]
                        diffrent_dict[key]['table2'] = row_2[key]
                        # print('\n', race_date, race_no, horse_no)
                        # print('not same:', race_date, race_no, horse_no, ' key:', key, ' table1:', row_1[key], ' table2:', row_2[key])
                break
        if not find:
            if 20190224 == row_2['race_date']:
                pass
            else:
                print("data can't find in[", table1, ']:', race_date, race_no, horse_no)
    print('keys:', diffrent_dict.keys())
    for key, value in diffrent_dict.items():
        print(key, value)


def test():
    rows = getResultsTableRows('today_table_dragon_model4')    # arrange, detailed, horse, race, record, game
    print(rows[0].keys())
    n = 0
    class_list = []
    for row in rows:
        # cls = row['class'].strip()
        # if cls not in class_list:
        #     class_list.append(cls)
        n += 1
    print(class_list)
    print(n)

# compareTwoTable('table_dragon_history', 'table_dragon_history_A')
# compareHistoryAndToday('table_dragon_history', 'today_table_dragon_20190227_A')
# test()


