###     赛前going上所有马的平均速度     ###
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


def getGoingAveSpeed(history_rows):
    # 按比赛日期排序
    race_rows = {}  # new_race_id & [row, row, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in race_rows.keys():
            race_rows[new_race_id] = []
        race_rows[new_race_id].append(row)
    race_id_sorted_list = sorted(race_rows.keys())
    # 计算going上的平均速度
    going_date_dict = {}   # horse_code & {going & [all_distance, all_time]}
    going_speed_dict = {}  # new_race_id & {horse_code & go_speed}
    for race_id in race_id_sorted_list:
        curRaceRows = race_rows[race_id]
        if race_id not in going_speed_dict.keys():
            going_speed_dict[race_id] = {}
        for row in curRaceRows:
            horse_code = row['horse_code']
            going = row['going'].strip().upper()
            if going == '':
                going = 'GOOD'

            # 赛前
            if horse_code in going_date_dict.keys():
                if going in going_date_dict[horse_code].keys():
                    if going_date_dict[horse_code][going][1] == 0:
                        going_speed_dict[race_id][horse_code] = 0
                    else:
                        going_speed_dict[race_id][horse_code] = going_date_dict[horse_code][going][0] / going_date_dict[horse_code][going][1]
                else:
                    going_speed_dict[race_id][horse_code] = 0
            else:
                going_speed_dict[race_id][horse_code] = 0

            # 赛后累加
            if horse_code not in going_date_dict.keys():
                going_date_dict[horse_code] = {}
            if going not in going_date_dict[horse_code].keys():
                going_date_dict[horse_code][going] = [0, 0]
                if row['plc'] not in common.words:
                    going_date_dict[horse_code][going][0] += int(row['distance'])
                    going_date_dict[horse_code][going][1] += __getRaceSeconds(row['finish_time'])
    return going_speed_dict





