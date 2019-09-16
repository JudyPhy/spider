from common import common


def __getGoingRecords(horse_code, going, history_raceResults_rows):
    going_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_going = dict[horse_code]['going'].replace(' ', '').upper()
            if cur_going == '':
                cur_going = 'GOOD'
            if (plc not in common.words) and (cur_going == going):
                going_records[4] += 1
                if int(plc) == 1:
                    going_records[0] += 1
                elif int(plc) == 2:
                    going_records[1] += 1
                elif int(plc) == 3:
                    going_records[2] += 1
                elif int(plc) == 4:
                    going_records[3] += 1
    return going_records


def __getGoing(race_date_No, going_dict):
    if race_date_No in going_dict.keys():
        return going_dict[race_date_No]
    print(race_date_No, "can't find going in going_dict")
    return ''


def GetHorseGoingRecord(future_raceCard_rows, history_raceResults_rows, going_dict):
    going_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in going_record_dict.keys():
            going_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            going = __getGoing(race_date_No, going_dict)
            going_record_dict[race_date_No][horse_No] = __getGoingRecords(horse_code, going, history_raceResults_rows)
    return going_record_dict

