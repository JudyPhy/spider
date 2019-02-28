###  取当天比赛前的所有历史数据，计算horse和trainer合作次数  ###
from db.database import singleton_Scrub_DB
from common import common
import datetime
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


def __calculateHorseTrainerRaceCount(ht_list, today_race_date):
    ht_raceCount_Dict = {}  # ht & [all_count, all_count_before3]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select race_date,horse_code,trainer,plc from {}'''.format(tableName))
            all_rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all_rows:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_race_date:
                    array_trainer = row['trainer'].split('(')
                    ht = row['horse_code'].strip() + '__' + array_trainer[0].strip()
                    if ht in ht_list:
                        if ht not in ht_raceCount_Dict.keys():
                            ht_raceCount_Dict[ht] = [0, 0]
                        if row['plc'] not in common.words:
                            ht_raceCount_Dict[ht][0] += 1
                            plc = int(row['plc'].replace('DH', ''))
                            if plc >= 1 and plc <= 3:
                                ht_raceCount_Dict[ht][1] += 1
        else:
            common.log('horse_jockey: Table[' + tableName + '] not exist.')
    return ht_raceCount_Dict


def getTodayHorseTrainerDict(today_rows):
    ht_list = []
    today_race_date = int(singleton_cfg.getRaceDate())
    for row in today_rows:
        array_trainer = row['trainer'].split('(')
        ht = row['horse_code'].strip() + '__' + array_trainer[0].strip()
        if ht not in ht_list:
            ht_list.append(ht)
    ht_raceCount_dict = __calculateHorseTrainerRaceCount(ht_list, today_race_date)   # ht & [all_count, all_count_before3]
    return ht_raceCount_dict

