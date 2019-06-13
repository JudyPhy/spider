###  取当天比赛前的所有历史数据，计算马匹评分  ###
from common import common
from horse_score.one_race import OneRace
from db.database import singleton_Scrub_DB
from horse_score.one_race import singleton_HorseScore
import datetime

RESULTS_TABLE = 'f_race_results_{0}'


def __getHistoryRaceDatas(today_date):
    all_race = {}   # new_race_id & [row1, row2, ...]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select race_date,race_id,horse_code,plc from {}'''.format(tableName))
            all_rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all_rows:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_date:
                    new_race_id = int(array_date[2] + array_date[1] + array_date[0] + common.toThreeDigitStr(row['race_id']))
                    if new_race_id not in all_race.keys():
                        all_race[new_race_id] = []
                    all_race[new_race_id].append(row)
        else:
            common.log('horse_starts: Table[' + tableName + '] not exist.')
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

