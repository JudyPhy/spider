from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


def __getGoing(race_date_No, horse_code, going_dict):
    if (race_date_No in going_dict.keys()) and (horse_code in going_dict[race_date_No].keys()):
        return going_dict[race_date_No][horse_code]
    return ''


# plc_dict: race_date_No & {horse_code & plc}
# going_dict: race_date_No & {horse_code & going}
def getHorseGoingRecord(raceCard_rows, plc_dict, going_dict):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    going_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_going_record = {}  # horse_code & {going & [No1, No2, No3, No4, All]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in going_record_dict.keys():
            going_record_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            going = __getGoing(race_date_No, horse_code, going_dict)

            # 赛前
            if (horse_code in temp_going_record.keys()) and (going in temp_going_record[horse_code].keys()):
                record = temp_going_record[horse_code][going]
                going_record_dict[race_date_No][horse_code] = [record[0], record[1], record[2], record[3], record[4]]
            else:
                going_record_dict[race_date_No][horse_code] = [0, 0, 0, 0, 0]

            # 赛后
            if horse_code not in temp_going_record.keys():
                temp_going_record[horse_code] = {}
            if going not in temp_going_record[horse_code].keys():
                temp_going_record[horse_code][going] = [0, 0, 0, 0, 0]
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if int(plc) == 1:
                    temp_going_record[horse_code][going][0] += 1
                elif int(plc) == 2:
                    temp_going_record[horse_code][going][1] += 1
                elif int(plc) == 3:
                    temp_going_record[horse_code][going][2] += 1
                elif int(plc) == 4:
                    temp_going_record[horse_code][going][3] += 1
                temp_going_record[horse_code][going][4] += 1

            # if 'B414' == horse_code:
            #     print('\n', race_date_No, going, plc)
            #     print(temp_going_record[horse_code])
            #     print(going_record_dict[race_date_No][horse_code])
    return going_record_dict

