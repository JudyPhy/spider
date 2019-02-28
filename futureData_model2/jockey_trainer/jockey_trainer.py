###  取当天比赛前的所有历史数据，计算jockey和trainer合作次数  ###
from db.database import singleton_Scrub_DB
from common import common
import datetime
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


def __calculateJockeyTrainerRaceCount(jt_list, today_race_date):
    jt_raceCount_Dict = {}  # jt & [all_count, all_count_before3]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select race_date,jockey,trainer,plc from {}'''.format(tableName))
            all_rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all_rows:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_race_date:
                    array_jockey = row['jockey'].split('(')
                    array_trainer = row['trainer'].split('(')
                    jt = array_jockey[0].strip() + '__' + array_trainer[0].strip()
                    if jt in jt_list:
                        if jt not in jt_raceCount_Dict.keys():
                            jt_raceCount_Dict[jt] = [0, 0]
                        if row['plc'] not in common.words:
                            jt_raceCount_Dict[jt][0] += 1
                            plc = int(row['plc'].replace('DH', ''))
                            if plc >= 1 and plc <= 3:
                                jt_raceCount_Dict[jt][1] += 1
        else:
            common.log('jockey_trainer: Table[' + tableName + '] not exist.')
    return jt_raceCount_Dict


def getTodayJockeyTrainerDict(today_rows):
    jt_list = []
    today_race_date = int(singleton_cfg.getRaceDate())
    for row in today_rows:
        array_jockey = row['jockey'].split('(')
        array_trainer = row['trainer'].split('(')
        jt = array_jockey[0].strip() + '__' + array_trainer[0].strip()
        if jt not in jt_list:
            jt_list.append(jt)
    jt_raceCount_dict = __calculateJockeyTrainerRaceCount(jt_list, today_race_date)   # jt & [all_count, all_count_before3]
    # print('\njt_raceCount_dict:', jt_raceCount_dict)
    return jt_raceCount_dict

