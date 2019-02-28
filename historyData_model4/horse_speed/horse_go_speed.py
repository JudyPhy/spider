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


def __getTime(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        finish_time = results_rows[race_date_No][horse_code]['finish_time']
        if ('-' in finish_time) and (results_rows[race_date_No][horse_code]['plc'] in common.words):
            return None
        else:
            return __getRaceSeconds(finish_time)
    return -1


def __getGoing(race_date_No, horse_code, going_dict):
    if (race_date_No in going_dict.keys()) and (horse_code in going_dict[race_date_No].keys()):
        return going_dict[race_date_No][horse_code]
    return ''


def getHorseGoSpeed(raceCard_rows, results_rows, going_dict):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    go_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_speed = {}  # horse_code & {going & [highest_speed, lowest_speed, all_dis, all_time]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in go_speed_dict.keys():
            go_speed_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            going = __getGoing(race_date_No, horse_code, going_dict)

            # 赛前
            if (horse_code in temp_speed.keys()) and (going in temp_speed[horse_code].keys()):
                speed = temp_speed[horse_code][going]
                go_speed_dict[race_date_No][horse_code] = [speed[0], speed[1], speed[2]/(speed[3] + 0.00001)]
            else:
                go_speed_dict[race_date_No][horse_code] = [0, 0, 0]

            # 赛后
            time = __getTime(race_date_No, horse_code, results_rows)
            if time == None:
                # 无效马本场次不记录
                continue
            else:
                if horse_code not in temp_speed.keys():
                    temp_speed[horse_code] = {}
                if going not in temp_speed[horse_code].keys():
                    temp_speed[horse_code][going] = [0, 9999, 0, 0]
                distance = int(row['distance'])
                curSpeed = distance/(time + 0.00001)
                if curSpeed > temp_speed[horse_code][going][0]:
                    temp_speed[horse_code][going][0] = curSpeed
                if curSpeed < temp_speed[horse_code][going][1]:
                    temp_speed[horse_code][going][1] = curSpeed
                temp_speed[horse_code][going][2] += distance
                temp_speed[horse_code][going][3] += time

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, going, distance, curSpeed)
            #     print(temp_speed[horse_code])
            #     print(go_speed_dict[race_date_No][horse_code])

    return go_speed_dict

