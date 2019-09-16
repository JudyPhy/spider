from common import common


def __getJockey(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array_jockey = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array_jockey[0].strip()
    return ''


def __getTrainer(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        return immd_info_dict[race_date_No][horse_No]['trainer'].strip()
    return ''


def __getJockeyTrainerRecords(jockey__trainer, history_raceResults_rows):
    jockey_trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            cur_trainer = row['trainer'].strip()
            cur_jockey__trainer = cur_jockey + '__' + cur_trainer
            if (plc not in common.words) and (cur_jockey__trainer == jockey__trainer):
                jockey_trainer_records[4] += 1
                if int(plc) == 1:
                    jockey_trainer_records[0] += 1
                elif int(plc) == 2:
                    jockey_trainer_records[1] += 1
                elif int(plc) == 3:
                    jockey_trainer_records[2] += 1
                elif int(plc) == 4:
                    jockey_trainer_records[3] += 1
    return jockey_trainer_records


def GetJockeyTrainerRecord(future_raceCard_rows, immd_info_dict, history_raceResults_rows):
    jockey_trainer_record_dict = {}  # jockey__trainer & [No1, No2, No3, No4, All]
    jockey_trainer_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            jockey = __getJockey(race_date_No, horse_No, immd_info_dict)
            if jockey == '':
                array_jockey = row['jockey'].split('(')
                jockey = array_jockey[0].strip()
            trainer = __getTrainer(race_date_No, horse_No, immd_info_dict)
            if trainer == '':
                trainer = row['trainer'].strip()
            jockey__trainer = jockey + '__' + trainer
            if jockey__trainer not in jockey_trainer_list:
                jockey_trainer_list.append(jockey__trainer)
    for jockey__trainer in jockey_trainer_list:
        jockey_trainer_record_dict[jockey__trainer] = __getJockeyTrainerRecords(jockey__trainer, history_raceResults_rows)
    return jockey_trainer_record_dict

