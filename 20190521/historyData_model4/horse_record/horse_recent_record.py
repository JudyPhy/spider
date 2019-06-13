from common import common

RECENT_COUNT = 6


def GetHorseRecentRecord(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_recent_record_dict = {}  # race_date_No & {horse_code & [No1, No2, No3, No4, All]}
    temp_horse_plc_dict = {}  # horse_code & {race_date_No & plc}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_recent_record_dict.keys():
            horse_recent_record_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_plc_dict.keys():
                        temp_horse_plc_dict[horse_code] = {}
                    # before
                    plc_list = list(temp_horse_plc_dict[horse_code].values())
                    cur_records = [0, 0, 0, 0, 0]
                    start_index = 0
                    if len(plc_list) >= RECENT_COUNT:
                        start_index = len(plc_list) - RECENT_COUNT
                    for tem_plc in plc_list[start_index:]:
                        cur_records[4] += 1
                        if int(tem_plc) == 1:
                            cur_records[0] += 1
                        elif int(tem_plc) == 2:
                            cur_records[1] += 1
                        elif int(tem_plc) == 3:
                            cur_records[2] += 1
                        elif int(tem_plc) == 4:
                            cur_records[3] += 1
                    horse_recent_record_dict[race_date_No][horse_code] = cur_records
                    # after
                    temp_horse_plc_dict[horse_code][race_date_No] = cur_plc
    return horse_recent_record_dict

