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


def __getRaceCardGear(race_date_No, horse_code, history_raceCard_rows):
    if (race_date_No in history_raceCard_rows.keys()) and (horse_code in history_raceCard_rows[race_date_No].keys()):
        return history_raceCard_rows[race_date_No][horse_code]['gear'].strip()
    print(race_date_No, 'horse[', horse_code, '] has no gear')
    return ''


def __getGearSpeeds(horse_code, gear_list, history_raceResults_rows, history_raceCard_rows):
    total_distance = 0
    total_time = 0
    highest_speed = 0
    lowest_speed = 9999
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_gear_list = __getGearList(__getRaceCardGear(race_date_No, horse_code, history_raceCard_rows))
            cur_distance = int(dict[horse_code]['distance'])
            cur_time = common.GetTotalSeconds(dict[horse_code]['finish_time'])
            if plc not in common.words:
                for cur_gear in cur_gear_list:
                    if cur_gear in gear_list:
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


def GetHorseGearSpeed(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows):
    gear_speed_dict = {}  # race_date_No & {horse_No & [highest_speed, lowest_speed, avr_speed]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in gear_speed_dict.keys():
            gear_speed_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            gear_list = __getGearList(row['gear'].strip())
            gear_speed_dict[race_date_No][horse_No] = __getGearSpeeds(horse_code, gear_list, history_raceResults_rows, history_raceCard_rows)
    return gear_speed_dict

