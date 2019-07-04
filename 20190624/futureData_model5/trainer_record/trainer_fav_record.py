from common import common


def __getTrainerFavRecords(trainer, history_raceResults_rows):
    trainer_fav_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array = row['trainer'].split('(')
            cur_trainer = array[0].strip()
            if (plc not in common.words) and (cur_trainer == trainer):
                cur_odds = float(row['win_odds'])
                isFav = common.IsLowestOdds(cur_odds, dict)
                if isFav:
                    trainer_fav_records[4] += 1
                    if int(plc) == 1:
                        trainer_fav_records[0] += 1
                    elif int(plc) == 2:
                        trainer_fav_records[1] += 1
                    elif int(plc) == 3:
                        trainer_fav_records[2] += 1
                    elif int(plc) == 4:
                        trainer_fav_records[3] += 1
    return trainer_fav_records


def getTrainerFavRecord(future_raceCard_rows, history_raceResults_rows):
    trainer_fav_record_dict = {}  # trainer & [No1, No2, No3, No4, All]
    trainer_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            array = row['trainer'].split('(')
            trainer = array[0].strip()
            if trainer not in trainer_list:
                trainer_list.append(trainer)
    for trainer in trainer_list:
        trainer_fav_record_dict[trainer] = __getTrainerFavRecords(trainer, history_raceResults_rows)
    return trainer_fav_record_dict

