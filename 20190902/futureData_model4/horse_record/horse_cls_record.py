from common import common


def __getClassRecords(horse_code, cls, history_raceResults_rows):
    cls_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_cls = dict[horse_code]['cls'].replace('Class', '').strip()
            if (plc not in common.words) and (cur_cls == cls):
                cls_records[4] += 1
                if int(plc) == 1:
                    cls_records[0] += 1
                elif int(plc) == 2:
                    cls_records[1] += 1
                elif int(plc) == 3:
                    cls_records[2] += 1
                elif int(plc) == 4:
                    cls_records[3] += 1
    return cls_records


def GetHorseClsRecord(future_raceCard_rows, history_raceResults_rows):
    cls_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in cls_record_dict.keys():
            cls_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            cls = row['cls'].replace('Class', '').replace(' ', '')
            cls_record_dict[race_date_No][horse_No] = __getClassRecords(horse_code, cls, history_raceResults_rows)
    return cls_record_dict

