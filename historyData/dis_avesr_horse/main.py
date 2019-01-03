###     赛前distance上单匹马的平均速度     ###
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
    dis_date_dict = {} # horse_code & {distance & [all_distance, all_time]}
    dis_speed_dict = {}  # new_race_id & {horse_code & ave_speed}
    for race_id in race_id_sorted_list:
        curRaceRows = race_rows[race_id]
        if race_id not in dis_speed_dict.keys():
            dis_speed_dict[race_id] = {}
        for row in curRaceRows:
            horse_code = row['horse_code']
            distance = int(row['distance'])

            # 赛前
            if horse_code in dis_date_dict.keys():
                if distance in dis_date_dict[horse_code].keys():
                    if dis_date_dict[horse_code][distance][1] == 0:
                        dis_speed_dict[race_id][horse_code] = 0
                    else:
                        dis_speed_dict[race_id][horse_code] = dis_date_dict[horse_code][distance][0] / dis_date_dict[horse_code][distance][1]
                else:
                    dis_speed_dict[race_id][horse_code] = 0
            else:
                dis_speed_dict[race_id][horse_code] = 0

            # 赛后累加
            if horse_code not in dis_date_dict.keys():
                dis_date_dict[horse_code] = {}
            if distance not in dis_date_dict[horse_code].keys():
                dis_date_dict[horse_code][distance] = [0, 0]
            if row['plc'] not in common.words:
                dis_date_dict[horse_code][distance][0] += distance
                dis_date_dict[horse_code][distance][1] += __getRaceSeconds(row['finish_time'])
    return dis_speed_dict





