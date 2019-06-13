from common import common


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


def __getTime(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        finish_time = results_rows[race_date_No][horse_code]['finish_time']
        if ('-' in finish_time) and (results_rows[race_date_No][horse_code]['plc'] in common.words):
            return None
        else:
            return __getRaceSeconds(finish_time)
    return -1


def __getPlc(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        return results_rows[race_date_No][horse_code]['plc'].replace('DH', '').strip()
    return ''


def getSpeed(raceCard_rows, results_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_speed = {}  # horse_code & [highest_speed, lowest_speed, all_dis, all_time]
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in speed_dict.keys():
            speed_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()

            # 赛前
            if horse_code not in temp_speed.keys():
                speed_dict[race_date_No][horse_code] = [0, 0, 0]
            else:
                speed = temp_speed[horse_code]
                speed_dict[race_date_No][horse_code] = [speed[0], speed[1], speed[2]/(speed[3] + 0.00001)]

            # 赛后
            time = __getTime(race_date_No, horse_code, results_rows)
            plc = __getPlc(race_date_No, horse_code, results_rows)
            if plc in common.words:
                continue
            else:
                if horse_code not in temp_speed.keys():
                    temp_speed[horse_code] = [0, 9999, 0, 0]
                distance = int(row['distance'])
                curSpeed = distance/(time + 0.00001)
                if curSpeed > temp_speed[horse_code][0]:
                    temp_speed[horse_code][0] = curSpeed
                if curSpeed < temp_speed[horse_code][1]:
                    temp_speed[horse_code][1] = curSpeed
                temp_speed[horse_code][2] += distance
                temp_speed[horse_code][3] += time

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, distance, curSpeed)
            #     print(temp_speed[horse_code])
            #     print(speed_dict[race_date_No][horse_code])
    return speed_dict

