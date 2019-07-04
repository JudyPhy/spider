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


def __getGearRecords(horse_code, gear_list, history_raceCard_rows, history_raceResults_rows):
    gear_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                if (race_date_No in history_raceCard_rows.keys()) and (horse_code in history_raceCard_rows[race_date_No].keys()):
                    cur_gear_list = __getGearList(history_raceCard_rows[race_date_No][horse_code]['gear'])
                    for sub_gear in cur_gear_list:
                        if sub_gear in gear_list:
                            gear_records[4] += 1
                            if int(plc) == 1:
                                gear_records[0] += 1
                            elif int(plc) == 2:
                                gear_records[1] += 1
                            elif int(plc) == 3:
                                gear_records[2] += 1
                            elif int(plc) == 4:
                                gear_records[3] += 1
                            break
    return gear_records


def GetHorseGearRecord(future_raceCard_rows, history_raceCard_rows, history_raceResults_rows):
    gear_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in gear_record_dict.keys():
            gear_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            gear_list = __getGearList(row['gear'])
            gear_record_dict[race_date_No][horse_No] = __getGearRecords(horse_code, gear_list, history_raceCard_rows, history_raceResults_rows)
    return gear_record_dict

