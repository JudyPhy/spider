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


def __getHistoryDistanceRaceData(distance_list, today_date):
    distance_rows = {}  # distance & [row, row, ...]
    if singleton_Results_DB.table_exists(HISTORY_RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute(
            'select race_date,race_id,finish_time,distance,plc from {} where race_date<%s'.format(HISTORY_RESULTS_FROM_TABLE), today_date)
        rows_orig = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in rows_orig:
            distance = int(row['distance'])
            if distance in distance_list:
                if distance not in distance_rows.keys():
                    distance_rows[distance] = []
                distance_rows[distance].append(row)
    else:
        common.log('dis_avesr: table[' + HISTORY_RESULTS_FROM_TABLE + '] not exist')
    return distance_rows


# return: distance & ave_speed
def getTodayDistanceAveSpeed(today_rows):
    distance_list = []
    for row in today_rows:
        distance = int(row['distance'])
        if distance not in distance_list:
            distance_list.append(distance)
    today_date = today_rows[0]['race_date']
    distance_rows = __getHistoryDistanceRaceData(distance_list, today_date)

    dis_avesr_dict = {}   # distance & ave_speed
    for distance, rows in distance_rows.items():
        if distance not in dis_avesr_dict.keys():
            dis_avesr_dict[distance] = 0
        all_time = 0
        all_distance = 0
        for row in rows:
            if row['plc'] not in common.words:
                all_distance += distance
                all_time += __getRaceSeconds(row['finish_time'])
        if all_time != 0:
            dis_avesr_dict[distance] = all_distance / all_time
    return dis_avesr_dict





