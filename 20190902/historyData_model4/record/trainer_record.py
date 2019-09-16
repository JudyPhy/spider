from common import common


def GetTrainerRecord(sort_race_date_rows, sort_history_raceResults_rows):
    trainer_record_dict = {}  # race_date & {trainer & [No1, No2, No3, No4, All]}
    temp_trainer_records = {}  # trainer & [No1, No2, No3, No4, All]
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in trainer_record_dict.keys():
            trainer_record_dict[race_date] = {}
        for row in rows:
            cur_trainer = row['trainer'].strip()
            if cur_trainer not in temp_trainer_records.keys():
                temp_trainer_records[cur_trainer] = [0, 0, 0, 0, 0]
            # before
            records = temp_trainer_records[cur_trainer]
            trainer_record_dict[race_date][cur_trainer] = [records[0], records[1], records[2], records[3], records[4]]
        # after
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            horse_code = row['horse_code'].strip()
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_trainer = sort_history_raceResults_rows[race_date_No][horse_code]['trainer'].strip()
                    temp_trainer_records[cur_trainer][4] += 1
                    if int(cur_plc) == 1:
                        temp_trainer_records[cur_trainer][0] += 1
                    elif int(cur_plc) == 2:
                        temp_trainer_records[cur_trainer][1] += 1
                    elif int(cur_plc) == 3:
                        temp_trainer_records[cur_trainer][2] += 1
                    elif int(cur_plc) == 4:
                        temp_trainer_records[cur_trainer][3] += 1
    return trainer_record_dict


