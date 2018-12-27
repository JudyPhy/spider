###     赛前distance上所有马的平均速度     ###
from common import common


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


def getDistanceAveSpeed(history_rows):
    # 按比赛日期排序
    race_rows = {} # new_race_id & [row, row, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in race_rows.keys():
            race_rows[new_race_id] = []
        race_rows[new_race_id].append(row)
    race_id_sorted_list = sorted(race_rows.keys())

    # 计算distance下的平均速度
    dis_date_dict = {} # distance & [all_distance, all_time]
    dis_speed_dict = {}  # new_race_id & ave_speed
    for race_id in race_id_sorted_list:
        curRaceRows = race_rows[race_id]
        distance = int(curRaceRows[0]['distance'])

        # 赛前
        if distance in dis_date_dict.keys():
            if dis_date_dict[distance][1] == 0:
                dis_speed_dict[race_id] = 0
            else:
                dis_speed_dict[race_id] = dis_date_dict[distance][0] / dis_date_dict[distance][1]
        else:
            dis_speed_dict[race_id] = 0

        # 赛后累加
        if distance not in dis_date_dict.keys():
            dis_date_dict[distance] = [0, 0]
        all_dis = 0
        all_time = 0
        for row in curRaceRows:
            if row['plc'] not in common.words:
                all_dis += int(row['distance'])
                all_time += __getRaceSeconds(row['finish_time'])
        dis_date_dict[distance][0] += all_dis
        dis_date_dict[distance][1] += all_time
    return dis_speed_dict





