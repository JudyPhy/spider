from common import common


def __getSpeeds(horse_code, history_raceResults_rows):
    total_distance = 0
    total_time = 0
    highest_speed = 0
    lowest_speed = 9999
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_distance = int(dict[horse_code]['distance'])
            cur_time = common.GetTotalSeconds(dict[horse_code]['finish_time'])
            if plc not in common.words:
                total_distance += cur_distance
                total_time += cur_time
                cur_speed = cur_distance/cur_time
                if cur_speed > highest_speed:
                    highest_speed = cur_speed
                if cur_speed < lowest_speed:
                    lowest_speed = cur_speed
    if lowest_speed == 9999:
        lowest_speed = 0
    ave_speed = 0
    if total_time > 0:
        ave_speed = total_distance / total_time
    return [highest_speed, lowest_speed, ave_speed]  # [highest_speed, lowest_speed, avr_speed]


def GetSpeed(future_raceCard_rows, history_raceResults_rows):
    speed_dict = {}  # race_date_No & {horse_No & [highest_speed, lowest_speed, avr_speed]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in speed_dict.keys():
            speed_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            speed_dict[race_date_No][horse_No] = __getSpeeds(horse_code, history_raceResults_rows)
    return speed_dict

