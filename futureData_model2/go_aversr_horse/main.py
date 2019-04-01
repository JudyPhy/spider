###  取比赛前的所有历史数据，计算going上所有马的平均速度 ###
import datetime
from common import common
from db.database import singleton_Scrub_DB
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


def __getRaceSeconds(time_text):
    seconds = 0
    array_time = []
    array1 = time_text.split('.')
    for item1 in array1:
        array2 = item1.split(':')
        for item2 in array2:
            array_time.append(item2)
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds


# 获取计算速度相关的历史数据
def __getHistoryGoingRaceData(code_going_dict, today_date):
    horse_dis_dict = {}  # horse_code & [all_dis, all_time]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                'select race_date,race_id,finish_time,distance,plc,going,horse_code from {}'.format(tableName))
            rows_orig = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows_orig:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_date:
                    horse_code = row['horse_code']
                    if (row['plc'] not in common.words) and (horse_code in code_going_dict.keys()):
                        if horse_code not in horse_dis_dict.keys():
                            horse_dis_dict[horse_code] = [0, 0]
                        going = row['going'].replace(' ', '').upper()
                        if going == '':
                            going = 'GOOD'
                        distance = int(row['distance'])
                        if going == code_going_dict[horse_code]:
                            horse_dis_dict[horse_code][0] += distance
                            horse_dis_dict[horse_code][1] += __getRaceSeconds(row['finish_time'])
        else:
            common.log('go_avesr_horse: table[' + tableName + '] not exist')
    return horse_dis_dict


def getTodayGoingAveSpeed(today_rows):
    code_going_dict = {}    # horse_code & going
    for row in today_rows:
        horse_code = row['horse_code']
        going = row['going'].replace(' ', '').strip().upper()
        if going == '':
            going = 'GOOD'
        if horse_code not in code_going_dict.keys():
            code_going_dict[horse_code] = going
    today_date = int(singleton_cfg.getRaceDate())
    horse_dis_dict = __getHistoryGoingRaceData(code_going_dict, today_date) # horse_code & [all_dis, all_time]
    # print(horse_dis_dict)

    going_ave_dict = {}   # horse_code & avesr
    for code, array in horse_dis_dict.items():
        if code in horse_dis_dict.keys():
            if array[1] == 0:
                going_ave_dict[code] = 0
            else:
                going_ave_dict[code] = array[0] / array[1]
        else:
            going_ave_dict[code] = 0
    return going_ave_dict





