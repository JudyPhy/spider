###  取当天比赛前的所有历史数据，计算horse和jockey合作次数  ###
from db.database import singleton_Scrub_DB
from common import common
import datetime
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


def __calculateHorseJockeyRaceCount(hj_list, today_race_date):
    hj_raceCount_Dict = {}  # hj & [all_count, all_count_before3]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select race_date,horse_code,jockey,plc from {}'''.format(tableName))
            all_rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all_rows:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_race_date:
                    array_jockey = row['jockey'].split('(')
                    hj = row['horse_code'].strip() + '__' + array_jockey[0].strip()
                    if hj in hj_list:
                        if hj not in hj_raceCount_Dict.keys():
                            hj_raceCount_Dict[hj] = [0, 0]
                        if row['plc'] not in common.words:
                            hj_raceCount_Dict[hj][0] += 1
                            plc = int(row['plc'].replace('DH', ''))
                            if plc >= 1 and plc <= 3:
                                hj_raceCount_Dict[hj][1] += 1
        else:
            common.log('horse_jockey: Table[' + tableName + '] not exist.')
    return hj_raceCount_Dict


def getTodayHorseJockeyDict(today_rows):
    hj_list = []
    today_race_date = int(singleton_cfg.getRaceDate())
    for row in today_rows:
        array_jockey = row['jockey'].split('(')
        hj = row['horse_code'].strip() + '__' + array_jockey[0].strip()
        if hj not in hj_list:
            hj_list.append(hj)
    hj_raceCount_dict = __calculateHorseJockeyRaceCount(hj_list, today_race_date)   # hj & [all_count, all_count_before3]

    # for hj, array in hj_raceCount_dict.items():
    #     if 'C299' in hj:
    #         print('\nhj_raceCount_dict:', hj, array)
    return hj_raceCount_dict

