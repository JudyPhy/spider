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
    exKey = ['id', 'race_id', 'pla_odds', 'plc', 'win_odds', 'odd_trend', 'odd_wave']
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


def test():
    rows = getScrubTableRows('tt_race_card_history')    # arrange, detailed, horse, race, record, game
    print(rows[0].keys())
    print(len(rows))
    n = 0
    array = []
    for row in rows:
        # if row['site'] not in array:
        #     array.append(row['site'])
        if '20190612' == row['race_date']:
            print(row)
            n += 1
    print('n=', n)

    # rows_old = getScrubTableRows('b_race_dividend')
    # m = 0
    # for row in rows_old:
    #     if '2019' in row['race_date']:    # and row['race_No'] == 5
    #         m += 1
    #         # print(row)
    #         if row['race_date'] not in array:
    #             array.append(row['race_date'])
    # print('m=', m)
    print('array:', array)

# compareHistoryAndToday('table_dragon_history_model4_6_12', 'today_table_dragon_model4_20190612')
test()
