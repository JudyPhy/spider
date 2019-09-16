from common import common

RECENT_COUNT = 6


def __getRecentRecord(horse_code, history_raceResults_rows):
    records = [0, 0, 0, 0, 0]
    sort_date_No_list = sorted(history_raceResults_rows.keys())
    sort_date_No_list.reverse()
    count = 0
    for race_date_No in sort_date_No_list:
        dict = history_raceResults_rows[race_date_No]
        if horse_code in dict.keys():
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
                count += 1
                if count >= RECENT_COUNT:
                    break
    return records


def GetHorseRecentRecord(future_raceCard_rows, history_raceResults_rows):
    recent_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in recent_record_dict.keys():
            recent_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            recent_record_dict[race_date_No][horse_No] = __getRecentRecord(horse_code, history_raceResults_rows)
    return recent_record_dict

