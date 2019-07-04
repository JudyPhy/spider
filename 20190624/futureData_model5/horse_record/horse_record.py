# coding=gbk
from common import common


def __getRecords(horse_code, history_raceResults_rows):
    rescords = [0, 0, 0, 0, 0]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                rescords[4] += 1
                if int(plc) == 1:
                    rescords[0] += 1
                elif int(plc) == 2:
                    rescords[1] += 1
                elif int(plc) == 3:
                    rescords[2] += 1
                elif int(plc) == 4:
                    rescords[3] += 1
    return rescords


def GetHorseRecord(future_raceCard_rows, history_raceResults_rows):
    record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in record_dict.keys():
            record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            record_dict[race_date_No][horse_No] = __getRecords(horse_code, history_raceResults_rows)
    return record_dict

