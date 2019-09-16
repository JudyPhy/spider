from common import common
import datetime

RECENT_COUNT = 90


def GetTrainerRecentRecord(sort_race_date_rows, sort_history_raceResults_rows):
    trainer_recent_record_dict = {}  # race_date & {trainer & [No1, No2, No3, No4, All]}
    temp_trainer_record_dict = {}  # trainer & {race_date & [No1, No2, No3, No4, All]}
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in trainer_recent_record_dict.keys():
            trainer_recent_record_dict[race_date] = {}
        cur_year = int(race_date[: len(race_date) - 4])
        cur_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
        cur_day = int(race_date[len(race_date) - 2:])
        cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
        before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
        for row in rows:
            array_trainer = row['trainer'].split('(')
            cur_trainer = array_trainer[0].strip()
            if cur_trainer not in temp_trainer_record_dict.keys():
                temp_trainer_record_dict[cur_trainer] = {}
            # before
            records = [0, 0, 0, 0, 0]
            for cur_race_date, array in temp_trainer_record_dict[cur_trainer].items():
                if int(cur_race_date) >= int(before_N_date):
                    records[0] += array[0]
                    records[1] += array[1]
                    records[2] += array[2]
                    records[3] += array[3]
                    records[4] += array[4]
            trainer_recent_record_dict[race_date][cur_trainer] = records
        # after
        cur_day_records = {}    # trainer & [No1, No2, No3, No4, All]
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            horse_code = row['horse_code'].strip()
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    array_trainer= sort_history_raceResults_rows[race_date_No][horse_code]['trainer'].split('(')
                    cur_trainer = array_trainer[0].strip()
                    if cur_trainer not in cur_day_records.keys():
                        cur_day_records[cur_trainer] = [0, 0, 0, 0, 0]
                    cur_day_records[cur_trainer][4] += 1
                    if int(cur_plc) == 1:
                        cur_day_records[cur_trainer][0] += 1
                    elif int(cur_plc) == 2:
                        cur_day_records[cur_trainer][1] += 1
                    elif int(cur_plc) == 3:
                        cur_day_records[cur_trainer][2] += 1
                    elif int(cur_plc) == 4:
                        cur_day_records[cur_trainer][3] += 1
        for trainer, array in cur_day_records.items():
            temp_trainer_record_dict[trainer][race_date] = array
    return trainer_recent_record_dict

