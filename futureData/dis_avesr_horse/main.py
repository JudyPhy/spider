###  取比赛前的所有历史数据，计算distance上所有马的平均速度 ###
from config.myconfig import singleton_cfg
from common import common
from db.database import singleton_Results_DB

HISTORY_RESULTS_FROM_TABLE = singleton_cfg.getHistoryRaceTable()


def __getRaceSeconds(time_text):
    seconds = 0
    array_time = time_text.split('.')
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds


def __getHistoryDistanceRaceData(code_dis_dict, today_date):
    horse_dis_dict = {}  # horse_code & [all_dis, all_time]
    if singleton_Results_DB.table_exists(HISTORY_RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute(
            'select race_date,race_id,finish_time,distance,plc,horse_code from {} where race_date<%s'.format(HISTORY_RESULTS_FROM_TABLE), today_date)
        rows_orig = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in rows_orig:
            horse_code = row['horse_code']
            if (row['plc'] not in common.words) and (horse_code in code_dis_dict.keys()):
                if horse_code not in horse_dis_dict.keys():
                    horse_dis_dict[horse_code] = [0, 0]
                distance = int(row['distance'])
                if distance == code_dis_dict[horse_code]:   # 马匹在该distance上的平均速度
                    horse_dis_dict[horse_code][0] += distance
                    horse_dis_dict[horse_code][1] += __getRaceSeconds(row['finish_time'])
    else:
        common.log('dis_avesr_horse: table[' + HISTORY_RESULTS_FROM_TABLE + '] not exist')
    return horse_dis_dict


# return: horse_code & ave_speed
def getTodayDistanceAveSpeed(today_rows):
    code_dis_dict = {}  # horse_code & distance
    for row in today_rows:
        horse_code = row['horse_code']
        if horse_code not in code_dis_dict.keys():
            code_dis_dict[horse_code] = int(row['distance'])
    today_date = today_rows[0]['race_date']
    horse_dis_dict = __getHistoryDistanceRaceData(code_dis_dict, today_date)    # horse_code & [all_dis, all_time]

    dis_avesr_dict = {}   # horse_code & ave_speed
    for code, array in horse_dis_dict.items():
        if code in horse_dis_dict.keys():
            if array[1] == 0:
                dis_avesr_dict[code] = 0
            else:
                dis_avesr_dict[code] = array[0] / array[1]
        else:
            dis_avesr_dict[code] = 0
    return dis_avesr_dict





