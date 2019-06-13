from common import common


def __getRaceSeconds(time_text):
    seconds = 0
    array_time = []
    array1 = time_text.split('.')
    for item1 in array1:
        array2 = item1.split(':')
        for item2 in array2:
            array_time.append(item2)
    # print(time_text, array_time)
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds


def __calculateSpeed(history_rows):
    # 按比赛日期排序
    race_dict = {}  # new_race_id & [row, row, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in race_dict.keys():
            race_dict[new_race_id] = []
        race_dict[new_race_id].append(row)
    sorted_race_id_list = sorted(race_dict.keys())
    # 计算每场比赛各马匹的平均速度
    horse_speed_dict = {}  # horse_code & [[distance, seconds], [distance, seconds], ...]
    race_speed_dict = {}  # new_race_id & {horse_code & [pre_speed, last_4_speed]}
    for new_race_id in sorted_race_id_list:
        if new_race_id not in race_speed_dict.keys():
            race_speed_dict[new_race_id] = {}
        curRows = race_dict[new_race_id]
        for row in curRows:
            horse_code = row['horse_code']
            # 赛前
            if horse_code in horse_speed_dict.keys():
                # last_4_speed
                all_dis = 0
                all_time = 0
                for array in horse_speed_dict[horse_code][:4]:
                    all_dis += array[0]
                    all_time += array[1]
                if all_time == 0:
                    last_4_speed = 0
                else:
                    last_4_speed = all_dis / all_time

                # pre_speed
                if horse_speed_dict[horse_code][0][1] == 0:
                    pre_speed = 0
                else:
                    pre_speed = horse_speed_dict[horse_code][0][0] / horse_speed_dict[horse_code][0][1]

                race_speed_dict[new_race_id][horse_code] = [pre_speed, last_4_speed]
            else:
                race_speed_dict[new_race_id][horse_code] = [0, 0]

            # 赛后累加
            if row['plc'] not in common.words:
                curDis = int(row['distance'])
                curTime = __getRaceSeconds(row['finish_time'])
                if horse_code not in horse_speed_dict.keys():
                    horse_speed_dict[horse_code] = []
                horse_speed_dict[horse_code].insert(0, [curDis, curTime])
    return race_speed_dict


def getRaceHorseSpeedDict(history_rows):
    speed_dict = __calculateSpeed(history_rows)   # new_race_id & {horse_code & [pre_speed, last_4_speed]}
    return speed_dict

