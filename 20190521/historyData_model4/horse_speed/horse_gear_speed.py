from common import common


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


def GetHorseGearSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_gear_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_horse_gear_speed = {}  # horse_code & {gear & [highest_speed, lowest_speed, all_dis, all_time]}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_gear_speed_dict.keys():
            horse_gear_speed_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                cur_gear_list = __getGearList(row['gear'])
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_gear_speed.keys():
                        temp_horse_gear_speed[horse_code] = {}
                    for sub_gear in cur_gear_list:
                        if sub_gear not in temp_horse_gear_speed[horse_code].keys():
                            temp_horse_gear_speed[horse_code][sub_gear] = [0, 9999, 0, 0.0000001]
                    # before
                    highest_speed = 0
                    lowest_speed = 9999
                    all_dis = 0
                    all_time = 0
                    for sub_gear in cur_gear_list:
                        array_speeds = temp_horse_gear_speed[horse_code][sub_gear]
                        if array_speeds[0] > highest_speed:
                            highest_speed = array_speeds[0]
                        if array_speeds[1] < lowest_speed:
                            lowest_speed = array_speeds[1]
                        all_dis += array_speeds[2]
                        all_time += array_speeds[3]
                    if lowest_speed == 9999:
                        lowest_speed = 0
                    ave_speed = 0
                    if all_time > 0:
                        ave_speed = all_dis/all_time
                    horse_gear_speed_dict[race_date_No][horse_code] = [highest_speed, lowest_speed, ave_speed]
                    # after
                    cur_distance = int(sort_history_raceResults_rows[race_date_No][horse_code]['distance'])
                    cur_seconds = common.GetTotalSeconds(sort_history_raceResults_rows[race_date_No][horse_code]['finish_time'])
                    cur_speed = cur_distance/cur_seconds
                    for sub_gear in cur_gear_list:
                        temp_horse_gear_speed[horse_code][sub_gear][2] += cur_distance
                        temp_horse_gear_speed[horse_code][sub_gear][3] += cur_seconds
                        if cur_speed > temp_horse_gear_speed[horse_code][sub_gear][0]:
                            temp_horse_gear_speed[horse_code][sub_gear][0] = cur_speed
                        if cur_speed < temp_horse_gear_speed[horse_code][sub_gear][1]:
                            temp_horse_gear_speed[horse_code][sub_gear][1] = cur_speed
    return horse_gear_speed_dict

