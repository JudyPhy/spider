from common import common


def __getDistanceRecords(horse_code, distance, history_raceResults_rows):
    distance_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_distance = int(dict[horse_code]['distance'])
            if (plc not in common.words) and (cur_distance == distance):
                distance_records[4] += 1
                if int(plc) == 1:
                    distance_records[0] += 1
                elif int(plc) == 2:
                    distance_records[1] += 1
                elif int(plc) == 3:
                    distance_records[2] += 1
                elif int(plc) == 4:
                    distance_records[3] += 1
    return distance_records


def GetHorseDstRecord(future_raceCard_rows, history_raceResults_rows):
    dst_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in dst_record_dict.keys():
            dst_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            distance = int(row['distance'])
            dst_record_dict[race_date_No][horse_No] = __getDistanceRecords(horse_code, distance, history_raceResults_rows)
    return dst_record_dict

