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


def __getGearList(gear):
    array_gear = gear.split('/')
    gear_list = []
    for sub in array_gear:
        for number in range(10):
            sub = sub.replace(str(number), '')
        if ('-' in sub) or (sub == ''):
            sub = '-'
        if sub not in gear_list:
            gear_list.append(sub)
    return gear_list


def getHorseGearSpeed(raceCard_rows, results_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    gear_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_speed = {}  # horse_code & {gear & [highest_speed, lowest_speed, all_dis, all_time]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in gear_speed_dict.keys():
            gear_speed_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            gear_list = __getGearList(row['gear'].strip())

            # 赛前
            if horse_code in temp_speed.keys():
                highest_speed_list = []
                lowest_speed_list = []
                all_dis = 0
                all_time = 0
                for gear in gear_list:
                    if gear in temp_speed[horse_code].keys():
                        highest_speed_list.append(temp_speed[horse_code][gear][0])
                        lowest_speed_list.append(temp_speed[horse_code][gear][1])
                        all_dis += temp_speed[horse_code][gear][2]
                        all_time += temp_speed[horse_code][gear][3]
                highest_speed = 0
                if len(highest_speed_list) > 0:
                    for highest in highest_speed_list:
                        if highest > highest_speed:
                            highest_speed = highest
                lowest_speed = 0
                if len(highest_speed_list) > 0:
                    lowest_speed = 9999
                    for lowest in lowest_speed_list:
                        if lowest < lowest_speed:
                            lowest_speed = lowest
                avr_speed = all_dis/(all_time + 0.00001)
                gear_speed_dict[race_date_No][horse_code] = [highest_speed, lowest_speed, avr_speed]
            else:
                gear_speed_dict[race_date_No][horse_code] = [0, 0, 0]

            # 赛后
            time = __getTime(race_date_No, horse_code, results_rows)
            if time == None:
                # 无效马本场次不记录
                continue
            else:
                if horse_code not in temp_speed.keys():
                    temp_speed[horse_code] = {}
                for gear in gear_list:
                    if gear not in temp_speed[horse_code].keys():
                        temp_speed[horse_code][gear] = [0, 9999, 0, 0]
                distance = int(row['distance'])
                curSpeed = distance/(time + 0.00001)
                for gear in gear_list:
                    if curSpeed > temp_speed[horse_code][gear][0]:
                        temp_speed[horse_code][gear][0] = curSpeed
                    if curSpeed < temp_speed[horse_code][gear][1]:
                        temp_speed[horse_code][gear][1] = curSpeed
                    temp_speed[horse_code][gear][2] += distance
                    temp_speed[horse_code][gear][3] += time

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, row['gear'].strip(), distance, curSpeed)
            #     print(temp_speed[horse_code])
            #     print(gear_speed_dict[race_date_No][horse_code])

    return gear_speed_dict

