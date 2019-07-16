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
    exKey = ['id', 'race_id', 'pla_odds', 'plc', 'win_odds', 'odd_trend', 'finish_time', 'lbw', 'odd_wave']
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
    rows = getScrubTableRows('tt_race_card_future')    # arrange, detailed, horse, race, record, game
    print(rows[0].keys())
    print(len(rows))
    n = 0
    array = []
    model_4 = {}    # race_date_No & {horse_coce & odds_wave}
    for row in rows:
        # if row['cls'] not in array:
        #     array.append(row['cls'])
        if '20190710' == row['race_date'] and row['race_No'] == 4 and row['horse_No'] == '7':
            print(row)
            n += 1
        # race_date_No = str(row['race_date']) + common.toDoubleDigitStr(row['race_no'])
        # if race_date_No not in model_4.keys():
        #     model_4[race_date_No] = {}
        # horse_code = row['horse_code']
        # odds_wave = row['odd_wave']
        # model_4[race_date_No][horse_code] = odds_wave
    print('n=', n)

    # rows_old = getResultsTableRows('table_dragon_history_model5')
    # m = 0
    # model_5 = {}  # race_date_No & {horse_coce & odds_wave}
    # for row in rows_old:
    #     race_date_No = str(row['race_date']) + common.toDoubleDigitStr(row['race_no'])
    #     if race_date_No not in model_5.keys():
    #         model_5[race_date_No] = {}
    #     horse_code = row['horse_code']
    #     odds_wave = row['odd_wave']
    #     model_5[race_date_No][horse_code] = odds_wave
    # # print('m=', m)
    # # print('array:', array)
    # # print('array_len:', len(array))
    #
    # for race_date_No, dict in model_4.items():
    #     for horse_code, odds_wave in dict.items():
    #         if (race_date_No in model_5.keys()) and (horse_code in model_5[race_date_No].keys()):
    #             if odds_wave != model_5[race_date_No][horse_code]:
    #                 print('not equl:', race_date_No, horse_code, odds_wave, model_5[race_date_No][horse_code])
    #         else:
    #             print('less:', race_date_No, horse_code)


compareHistoryAndToday('table_dragon_history_model5', 'today_table_dragon_model5_20190710_test')
# test()

