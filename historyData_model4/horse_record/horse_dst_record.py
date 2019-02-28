from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


# plc_dict: race_date_No & {horse_code & plc}
def getHorseDstRecord(raceCard_rows, plc_dict):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    dst_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
    temp_plc_record = {}  # horse_code & {distance & [No1, No2, No3, No4, Fail]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in dst_record_dict.keys():
            dst_record_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            distance = int(row['distance'])

            # 赛前
            if (horse_code in temp_plc_record.keys()) and (distance in temp_plc_record[horse_code].keys()):
                record = temp_plc_record[horse_code][distance]
                dst_record_dict[race_date_No][horse_code] = [record[0], record[1], record[2], record[3], record[4]]
            else:
                dst_record_dict[race_date_No][horse_code] = [0, 0, 0, 0, 0]

            # 赛后
            if horse_code not in temp_plc_record.keys():
                temp_plc_record[horse_code] = {}
            if distance not in temp_plc_record[horse_code].keys():
                temp_plc_record[horse_code][distance] = [0, 0, 0, 0, 0]
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if int(plc) == 1:
                    temp_plc_record[horse_code][distance][0] += 1
                elif int(plc) == 2:
                    temp_plc_record[horse_code][distance][1] += 1
                elif int(plc) == 3:
                    temp_plc_record[horse_code][distance][2] += 1
                elif int(plc) == 4:
                    temp_plc_record[horse_code][distance][3] += 1
                elif int(plc) > 4:
                    temp_plc_record[horse_code][distance][4] += 1

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, distance, plc)
            #     print(temp_plc_record[horse_code])
            #     print(dst_record_dict[race_date_No][horse_code])
    return dst_record_dict

