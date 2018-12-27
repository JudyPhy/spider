###  取当天比赛前的所有历史数据，计算马匹参赛场次  ###
from db.database import singleton_Results_DB
from common import common
from config.myconfig import singleton_cfg

HISTORY_RESULTS_FROM_TABLE = singleton_cfg.getHistoryRaceTable()


def __getHistoryRaceDatas(today_date):
    all_rows = []
    if singleton_Results_DB.table_exists(HISTORY_RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute(
            '''select race_date,race_id,horse_code,plc from {} where race_date<%s'''.format(HISTORY_RESULTS_FROM_TABLE), today_date)
        all_rows = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
    else:
        common.log('horse_starts: Table[' + HISTORY_RESULTS_FROM_TABLE + '] not exist.')
    return all_rows


def __calculateHorseStar(horse_code_list, today_date):
    start_dict = {}  # horse_code & {No1:count, No2:count, No3:count, No4:count, All:count}
    history_race_rows = __getHistoryRaceDatas(today_date)
    for row in history_race_rows:
        horse_code = row['horse_code']
        if horse_code in horse_code_list:
            if horse_code not in start_dict.keys():
                start_dict[horse_code] = {}
                start_dict[horse_code]['No1'] = 0
                start_dict[horse_code]['No2'] = 0
                start_dict[horse_code]['No3'] = 0
                start_dict[horse_code]['No4'] = 0
                start_dict[horse_code]['All'] = 0
            if row['plc'] not in common.words:
                plc = int(row['plc'].replace('DH', ''))
                if plc == 1:
                    start_dict[horse_code]['No1'] += 1
                elif plc == 2:
                    start_dict[horse_code]['No2'] += 1
                elif plc == 3:
                    start_dict[horse_code]['No3'] += 1
                elif plc == 4:
                    start_dict[horse_code]['No4'] += 1
                start_dict[horse_code]['All'] += 1
    return start_dict


def getTodayHorseStartsDict(today_rows):
    horse_code_list = []
    today_date = today_rows[0]['race_date']
    for row in today_rows:
        if row['horse_code'] not in horse_code_list:
            horse_code_list.append(row['horse_code'])
    dict_race_start = __calculateHorseStar(horse_code_list, today_date)  # horse_code & {No1:count, No2:count, No3:count, No4:count, All:count}
    return dict_race_start
