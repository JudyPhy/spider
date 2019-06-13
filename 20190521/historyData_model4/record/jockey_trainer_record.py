from common import common


def GetJockeyTrainerRecord(sort_race_date_rows, sort_history_raceResults_rows):
    jockey_trainer_record_dict = {}  # race_date & {jockey__trainer & [No1, No2, No3, No4, All]}
    temp_jockey_trainer_record = {}  # jockey__trainer & [No1, No2, No3, No4, All]
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in jockey_trainer_record_dict.keys():
            jockey_trainer_record_dict[race_date] = {}
        for row in rows:
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            cur_trainer = row['trainer'].strip()
            cur_jockey_trainer = cur_jockey + '__' + cur_trainer
            if cur_jockey_trainer not in temp_jockey_trainer_record.keys():
                temp_jockey_trainer_record[cur_jockey_trainer] = [0, 0, 0, 0, 0]
            # before
            records = temp_jockey_trainer_record[cur_jockey_trainer]
            jockey_trainer_record_dict[race_date][cur_jockey_trainer] = [records[0], records[1], records[2], records[3], records[4]]
        # after
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            horse_code = row['horse_code'].strip()
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    array_jockey = sort_history_raceResults_rows[race_date_No][horse_code]['jockey'].split('(')
                    cur_jockey = array_jockey[0].strip()
                    cur_trainer = sort_history_raceResults_rows[race_date_No][horse_code]['trainer'].strip()
                    cur_jockey_trainer = cur_jockey + '__' + cur_trainer
                    temp_jockey_trainer_record[cur_jockey_trainer][4] += 1
                    if int(cur_plc) == 1:
                        temp_jockey_trainer_record[cur_jockey_trainer][0] += 1
                    elif int(cur_plc) == 2:
                        temp_jockey_trainer_record[cur_jockey_trainer][1] += 1
                    elif int(cur_plc) == 3:
                        temp_jockey_trainer_record[cur_jockey_trainer][2] += 1
                    elif int(cur_plc) == 4:
                        temp_jockey_trainer_record[cur_jockey_trainer][3] += 1
    return jockey_trainer_record_dict

