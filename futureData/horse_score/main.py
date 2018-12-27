###  取当天比赛前的所有历史数据，计算马匹评分  ###
from common import common
from horse_score.one_race import OneRace
from db.database import singleton_Results_DB
from horse_score.one_race import singleton_HorseScore
from config.myconfig import singleton_cfg

HISTORY_RESULTS_FROM_TABLE = singleton_cfg.getHistoryRaceTable()


def __getHistoryRaceDatas(today_date):
    all_race = {}   # new_race_id & [row1, row2, ...]
    if singleton_Results_DB.table_exists(HISTORY_RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute(
            '''select race_date,race_id,horse_code,plc from {} where race_date<%s'''.format(HISTORY_RESULTS_FROM_TABLE), today_date)
        all_rows = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in all_rows:
            new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
            if new_race_id not in all_race.keys():
                all_race[new_race_id] = []
            all_race[new_race_id].append(row)
    else:
        common.log('horse_starts: Table[' + HISTORY_RESULTS_FROM_TABLE + '] not exist.')
    return all_race


def __calculateScore(k, today_date):
    history_race = __getHistoryRaceDatas(today_date)  # new_race_id & [row1, row2, ...]
    # 按比赛日期排序后，计算马匹分数
    sorted_race_id_list = sorted(history_race.keys())
    for curId in sorted_race_id_list:
        rows_curRace = history_race[curId]
        plc_curRace = {}   # horse_code & plc
        for row in rows_curRace:
            key = row['horse_code']
            if row['plc'] not in common.words:
                plc_curRace[key] = row['plc']
        OneRace(plc_curRace, k)
        pass
    return singleton_HorseScore.mapScore     # horse_code & score


def getAllHorseScoreDict(today_date):
    K = 4454
    dict_score = __calculateScore(K, today_date)  # horse_code & score
    return dict_score

