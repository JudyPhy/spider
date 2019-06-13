from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


# plc_dict: race_date_No & {horse_code & plc}
def getJockeyTrainerRecord(raceCard_rows, plc_dict):
    temp_raceCard_rows = {}  # race_date & [rows]
    for row in raceCard_rows:
        race_date = row['race_date']
        if race_date not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date] = []
        temp_raceCard_rows[race_date].append(row)

    jockey_trainer_record_dict = {}  # race_date & {jockey__trainer & [No1, No2, No3, No4, All]}
    temp_jockey_trainer_plc_record = {}  # jockey__trainer & [No1, No2, No3, No4, All]
    sort_date_list = sorted(temp_raceCard_rows.keys())
    for race_date in sort_date_list:
        if race_date not in jockey_trainer_record_dict.keys():
            jockey_trainer_record_dict[race_date] = {}

        # 赛前
        rows = temp_raceCard_rows[race_date]
        for row in rows:
            array_jockey = row['jockey'].split('(')
            jockey = array_jockey[0].strip()
            trainer = row['trainer'].strip()
            jockey__trainer = jockey + '__' + trainer
            if jockey__trainer in temp_jockey_trainer_plc_record.keys():
                array = temp_jockey_trainer_plc_record[jockey__trainer]
                jockey_trainer_record_dict[race_date][jockey__trainer] = [array[0], array[1], array[2], array[3], array[4]]

        # 赛后
        for row in rows:
            array_jockey = row['jockey'].split('(')
            jockey = array_jockey[0].strip()
            trainer = row['trainer'].strip()
            jockey__trainer = jockey + '__' + trainer

            if jockey__trainer not in temp_jockey_trainer_plc_record.keys():
                temp_jockey_trainer_plc_record[jockey__trainer] = [0, 0, 0, 0, 0]
            horse_code = row['horse_code'].strip()
            race_date_No = race_date + common.toDoubleDigitStr(row['race_No'])
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                temp_jockey_trainer_plc_record[jockey__trainer][4] += 1
                if int(plc) == 1:
                    temp_jockey_trainer_plc_record[jockey__trainer][0] += 1
                elif int(plc) == 2:
                    temp_jockey_trainer_plc_record[jockey__trainer][1] += 1
                elif int(plc) == 3:
                    temp_jockey_trainer_plc_record[jockey__trainer][2] += 1
                elif int(plc) == 4:
                    temp_jockey_trainer_plc_record[jockey__trainer][3] += 1

        # print('\n', race_date)
        # print(temp_jockey_trainer_plc_record)
        # print(jockey_trainer_record_dict[race_date])
    return jockey_trainer_record_dict

