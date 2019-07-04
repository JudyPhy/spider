from common import common
import datetime

RECENT_COUNT = 90


def __getRecentRecord(horse_code, before_N_date, history_raceResults_rows):
    records = [0, 0, 0, 0, 0]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            cur_race_date = race_date_No[: len(race_date_No) - 2]
            if int(cur_race_date) >= int(before_N_date):
                plc = dict[horse_code]['plc'].replace('DH', '')
                if plc not in common.words:
                    records[4] += 1
                    if int(plc) == 1:
                        records[0] += 1
                    elif int(plc) == 2:
                        records[1] += 1
                    elif int(plc) == 3:
                        records[2] += 1
                    elif int(plc) == 4:
                        records[3] += 1
    return records


def GetHorseRecentRecord(future_raceCard_rows, history_raceResults_rows):
    recent_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in recent_record_dict.keys():
            recent_record_dict[race_date_No] = {}
        cur_race_date = race_date_No[: len(race_date_No) - 2]
        cur_year = int(cur_race_date[: len(cur_race_date) - 4])
        cur_month = int(cur_race_date[len(cur_race_date) - 4: len(cur_race_date) - 2])
        cur_day = int(cur_race_date[len(cur_race_date) - 2:])
        cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
        before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            recent_record_dict[race_date_No][horse_No] = __getRecentRecord(horse_code, before_N_date, history_raceResults_rows)
    return recent_record_dict

