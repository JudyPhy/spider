###  取比赛前的所有历史数据，计算distance上所有马的平均速度 ###
from common import common
from db.database import singleton_Scrub_DB
import datetime
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


def __getHistoryDistanceRaceData(distance_list, today_date):
    distance_rows = {}  # distance & [row, row, ...]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                'select race_date,race_id,finish_time,distance,plc from {}'.format(tableName))
            rows_orig = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows_orig:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_date:
                    distance = int(row['distance'])
                    if distance in distance_list:
                        if distance not in distance_rows.keys():
                            distance_rows[distance] = []
                        distance_rows[distance].append(row)
        else:
            common.log('dis_avesr: table[' + tableName + '] not exist')
    return distance_rows


# return: distance & ave_speed
def getTodayDistanceAveSpeed(today_rows):
    distance_list = []
    for row in today_rows:
        distance = int(row['distance'])
        if distance not in distance_list:
            distance_list.append(distance)
    today_date = int(singleton_cfg.getRaceDate())
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





