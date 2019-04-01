###  取当天比赛前的所有历史数据，计算速度  ###
from db.database import singleton_Scrub_DB
from common import common
import datetime
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


def __getHorseHistoryRaceDict(horse_code_list, today_race_date):
    horseRaceDict = {}  # horse_code & {new_race_id & [distance, seconds]}
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select horse_code,race_date,race_id,distance,finish_time,plc from {}'''.format(tableName))
            all_rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in all_rows:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_race_date:
                    horse_code = row['horse_code']
                    if horse_code in horse_code_list:
                        if horse_code not in horseRaceDict.keys():
                            horseRaceDict[horse_code] = {}
                        if row['plc'] not in common.words:
                            new_race_id = int(array_date[2] + array_date[1] + array_date[0] + common.toThreeDigitStr(row['race_id']))
                            if new_race_id not in horseRaceDict[horse_code].keys():
                                horseRaceDict[horse_code][new_race_id] = []
                            # race time
                            if row['finish_time'] == '':
                                race_time = 0
                            else:
                                array_finish_time = []
                                array1 = row['finish_time'].split('.')
                                for item1 in array1:
                                    array2 = item1.split(':')
                                    for item2 in array2:
                                        array_finish_time.append(item2)
                                race_time = int(array_finish_time[0]) * 60 + int(array_finish_time[1]) + int(array_finish_time[2]) / 100
                            horseRaceDict[horse_code][new_race_id] = [int(row['distance']), race_time]
        else:
            common.log('horse_speed: Table[' + tableName + '] not exist.')
    return horseRaceDict


# history_race_dict: horse_code & {new_race_id & [distance, seconds]}
def __calculateSpeed(history_race_dict):
    race_speed_dict = {}    # horse_code & [pre_speed, last_4_speed]
    for code, dict in history_race_dict.items():
        if code not in race_speed_dict.keys():
            race_speed_dict[code] = []

        sorted_race_id_list = sorted(dict.keys())
        sorted_race_id_list.reverse()
        pre_speed = 0
        last_4_speed = 0
        if len(sorted_race_id_list) > 0:
            pre_race_id = sorted_race_id_list[0]
            pre_speed = dict[pre_race_id][0]/dict[pre_race_id][1]

            sum_dis = 0
            sum_sec = 0
            count = 0
            for race_id in sorted_race_id_list:
                if count >= 4:
                    break
                sum_dis += dict[race_id][0]
                sum_sec += dict[race_id][1]
                count += 1
            last_4_speed = sum_dis / sum_sec

        race_speed_dict[code] = [pre_speed, last_4_speed]
    return race_speed_dict


def getTodayRaceHorseSpeedDict(today_rows):
    horse_code_list = []
    today_race_date = int(singleton_cfg.getRaceDate())
    for row in today_rows:
        if row['horse_code'] not in horse_code_list:
            horse_code_list.append(row['horse_code'])
    history_race_dict = __getHorseHistoryRaceDict(horse_code_list, today_race_date)  # horse_code & {new_race_id & [distance, seconds]}
    speed_dict = __calculateSpeed(history_race_dict)   # horse_code & [pre_speed, last_4_speed]
    return speed_dict

