from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


# plc_dict: race_date_No & {horse_code & plc}
def getTrainerRecord(raceCard_rows, plc_dict):
    temp_raceCard_rows = {}  # race_date & [rows]
    for row in raceCard_rows:
        race_date = row['race_date']
        if race_date not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date] = []
        temp_raceCard_rows[race_date].append(row)

    trainer_record_dict = {}  # race_date & {trainer & [No1, No2, No3, No4, All]}
    temp_trainer_plc_record = {}  # trainer & [No1, No2, No3, No4, All]
    sort_date_list = sorted(temp_raceCard_rows.keys())
    for race_date in sort_date_list:
        if race_date not in trainer_record_dict.keys():
            trainer_record_dict[race_date] = {}

        # 赛前
        for trainer, array in temp_trainer_plc_record.items():
            trainer_record_dict[race_date][trainer] = [array[0], array[1], array[2], array[3], array[4]]

        # 赛后
        rows = temp_raceCard_rows[race_date]
        for row in rows:
            array_trainer = row['trainer'].split('(')
            trainer = array_trainer[0].strip()
            if trainer not in temp_trainer_plc_record.keys():
                temp_trainer_plc_record[trainer] = [0, 0, 0, 0, 0]
            horse_code = row['horse_code'].strip()
            race_date_No = race_date + common.toDoubleDigitStr(row['race_No'])
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if int(plc) == 1:
                    temp_trainer_plc_record[trainer][0] += 1
                elif int(plc) == 2:
                    temp_trainer_plc_record[trainer][1] += 1
                elif int(plc) == 3:
                    temp_trainer_plc_record[trainer][2] += 1
                elif int(plc) == 4:
                    temp_trainer_plc_record[trainer][3] += 1
                temp_trainer_plc_record[trainer][4] += 1

        # print('\n', race_date)
        # print(temp_trainer_plc_record)
        # print(trainer_record_dict[race_date])
    return trainer_record_dict

