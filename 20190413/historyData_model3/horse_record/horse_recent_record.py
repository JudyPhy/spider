from common import common

RECENT_COUNT = 6


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


def __getRecentRecord(horse_code, race_date_No, horse_plc_dict):
    if horse_code in horse_plc_dict.keys():
        sort_date_No_list = sorted(horse_plc_dict[horse_code].keys())
        sort_date_No_list.reverse()
        flag = False
        count = 0
        record = [0, 0, 0, 0, 0]
        for sub_race_date_No in sort_date_No_list:
            if sub_race_date_No == race_date_No:
                flag = True
            elif flag:
                plc = horse_plc_dict[horse_code][sub_race_date_No]
                if plc not in common.words:
                    if int(plc) == 1:
                        record[0] += 1
                    elif int(plc) == 2:
                        record[1] += 1
                    elif int(plc) == 3:
                        record[2] += 1
                    elif int(plc) == 4:
                        record[3] += 1
                    record[4] += 1
                count += 1
                if count >= RECENT_COUNT:
                    flag = False
                    break
        return record
    else:
        return [-1, -1, -1, -1, -1]


# plc_dict: race_date_No & {horse_code & plc}
def getHorseRecentRecord(raceCard_rows, plc_dict):
    horse_plc_dict = {}  # horse_code & {race_date_No & plc}
    for row in raceCard_rows:
        horse_code = row['horse_code'].strip()
        if horse_code not in horse_plc_dict.keys():
            horse_plc_dict[horse_code] = {}
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        horse_plc_dict[horse_code][race_date_No] = __getPlc(race_date_No, horse_code, plc_dict)

    recent_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in recent_record_dict.keys():
            recent_record_dict[race_date_No] = {}
        horse_code = row['horse_code'].strip()
        recent_record_dict[race_date_No][horse_code] = __getRecentRecord(horse_code, race_date_No, horse_plc_dict)
    return recent_record_dict

