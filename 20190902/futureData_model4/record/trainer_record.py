from common import common


def __getTrainerRecords(trainer, history_raceResults_rows):
    trainer_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            cur_trainer = row['trainer'].strip()
            if (plc not in common.words) and (cur_trainer == trainer):
                trainer_records[4] += 1
                if int(plc) == 1:
                    trainer_records[0] += 1
                elif int(plc) == 2:
                    trainer_records[1] += 1
                elif int(plc) == 3:
                    trainer_records[2] += 1
                elif int(plc) == 4:
                    trainer_records[3] += 1
    return trainer_records


def getTrainerRecord(future_raceCard_rows, history_raceResults_rows):
    trainer_record_dict = {}  # trainer & [No1, No2, No3, No4, All]
    trainer_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            trainer = row['trainer'].strip()
            if trainer not in trainer_list:
                trainer_list.append(trainer)
    for trainer in trainer_list:
        trainer_record_dict[trainer] = __getTrainerRecords(trainer, history_raceResults_rows)
    return trainer_record_dict

