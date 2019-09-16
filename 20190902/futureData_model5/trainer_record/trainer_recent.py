from common import common
import datetime

RECENT_COUNT = 90


def __getTrainerRecentRecord(trainer, before_N_date, history_raceResults_rows):
    trainer_recent_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array = row['trainer'].split('(')
            cur_trainer = array[0].strip()
            cur_date = race_date_No[: len(race_date_No) - 2]
            if (plc not in common.words) and (cur_trainer == trainer) and (int(cur_date) >= int(before_N_date)):
                trainer_recent_records[4] += 1
                if int(plc) == 1:
                    trainer_recent_records[0] += 1
                elif int(plc) == 2:
                    trainer_recent_records[1] += 1
                elif int(plc) == 3:
                    trainer_recent_records[2] += 1
                elif int(plc) == 4:
                    trainer_recent_records[3] += 1
    return trainer_recent_records


def getTrainerRecentRecord(future_raceCard_rows, history_raceResults_rows):
    trainer_recent_record_dict = {}  # trainer & [No1, No2, No3, No4, All]
    trainer_date_dict = {}   # trainer & before_N_date
    for race_date_No, dict in future_raceCard_rows.items():
        cur_race_date = race_date_No[: len(race_date_No) - 2]
        cur_year = int(cur_race_date[: len(cur_race_date) - 4])
        cur_month = int(cur_race_date[len(cur_race_date) - 4: len(cur_race_date) - 2])
        cur_day = int(cur_race_date[len(cur_race_date) - 2:])
        cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
        before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
        for horse_No, row in dict.items():
            array = row['trainer'].split('(')
            trainer = array[0].strip()
            if trainer not in trainer_date_dict.keys():
                trainer_date_dict[trainer] = before_N_date
    for trainer, before_N_date in trainer_date_dict.items():
        if trainer not in trainer_recent_record_dict.keys():
            trainer_recent_record_dict[trainer] = __getTrainerRecentRecord(trainer, before_N_date, history_raceResults_rows)
    return trainer_recent_record_dict

