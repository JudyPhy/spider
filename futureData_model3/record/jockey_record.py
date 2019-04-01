from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


# plc_dict: race_date_No & {horse_code & plc}
def getJockeyRecord(raceCard_rows, plc_dict):
    temp_raceCard_rows = {}  # race_date & [rows]
    for row in raceCard_rows:
        race_date = row['race_date']
        if race_date not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date] = []
        temp_raceCard_rows[race_date].append(row)

    jockey_record_dict = {}  # race_date & {jockey & [No1, No2, No3, No4, All]}
    temp_jockey_plc_record = {}  # jockey & [No1, No2, No3, No4, All]
    sort_date_list = sorted(temp_raceCard_rows.keys())
    for race_date in sort_date_list:
        if race_date not in jockey_record_dict.keys():
            jockey_record_dict[race_date] = {}

        # 赛前
        for jockey, array in temp_jockey_plc_record.items():
            jockey_record_dict[race_date][jockey] = [array[0], array[1], array[2], array[3], array[4]]

        # 赛后
        rows = temp_raceCard_rows[race_date]
        for row in rows:
            array_jockey = row['jockey'].split('(')
            jockey = array_jockey[0].strip()

            if jockey not in temp_jockey_plc_record.keys():
                temp_jockey_plc_record[jockey] = [0, 0, 0, 0, 0]
            horse_code = row['horse_code'].strip()
            race_date_No = race_date + common.toDoubleDigitStr(row['race_No'])
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if int(plc) == 1:
                    temp_jockey_plc_record[jockey][0] += 1
                elif int(plc) == 2:
                    temp_jockey_plc_record[jockey][1] += 1
                elif int(plc) == 3:
                    temp_jockey_plc_record[jockey][2] += 1
                elif int(plc) == 4:
                    temp_jockey_plc_record[jockey][3] += 1
                temp_jockey_plc_record[jockey][4] += 1

        # print('\n', race_date)
        # print(temp_jockey_plc_record)
        # print(jockey_record_dict[race_date])
    return jockey_record_dict

