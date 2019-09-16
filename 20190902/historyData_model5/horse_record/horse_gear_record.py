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


def GetHorseGearRecord(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_gear_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_horse_gear_plc = {}  # horse_code & {gear & {race_date_No & plc}}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_gear_record_dict.keys():
            horse_gear_record_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_gear_list = __getGearList(row['gear'])
                    if horse_code not in temp_horse_gear_plc.keys():
                        temp_horse_gear_plc[horse_code] = {}
                    for sub_gear in cur_gear_list:
                        if sub_gear not in temp_horse_gear_plc[horse_code].keys():
                            temp_horse_gear_plc[horse_code][sub_gear] = {}
                    # before
                    cur_race_plc_dict = {}    # race_date_No & plc
                    for sub_gear in cur_gear_list:
                        for race, plc in temp_horse_gear_plc[horse_code][sub_gear].items():
                            if race not in cur_race_plc_dict.keys():
                                cur_race_plc_dict[race] = plc
                    cur_record = [0, 0, 0, 0, 0]
                    for race, plc in cur_race_plc_dict.items():
                        cur_record[4] += 1
                        if int(plc) == 1:
                            cur_record[0] += 1
                        elif int(plc) == 2:
                            cur_record[1] += 1
                        elif int(plc) == 3:
                            cur_record[2] += 1
                        elif int(plc) == 4:
                            cur_record[3] += 1
                    horse_gear_record_dict[race_date_No][horse_code] = [cur_record[0], cur_record[1], cur_record[2], cur_record[3], cur_record[4]]
                    # after
                    for sub_gear in cur_gear_list:
                        temp_horse_gear_plc[horse_code][sub_gear][race_date_No] = cur_plc
    return horse_gear_record_dict

