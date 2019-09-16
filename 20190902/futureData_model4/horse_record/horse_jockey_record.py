from common import common


def __getJockey(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array_jockey = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array_jockey[0].strip()
    return ''


def __getJockeyRecord(horse_code, jockey, history_raceResults_rows):
    jockey_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            array_jockey = dict[horse_code]['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey):
                jockey_records[4] += 1
                if int(plc) == 1:
                    jockey_records[0] += 1
                elif int(plc) == 2:
                    jockey_records[1] += 1
                elif int(plc) == 3:
                    jockey_records[2] += 1
                elif int(plc) == 4:
                    jockey_records[3] += 1
    return jockey_records


def GetHorseJockeyRecord(future_raceCard_rows, immd_info_dict, history_raceResults_rows):
    jockey_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in jockey_record_dict.keys():
            jockey_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            jockey = __getJockey(race_date_No, horse_No, immd_info_dict)
            if jockey == '':
                array_jockey = row['jockey'].split('(')
                jockey = array_jockey[0].strip()
            if jockey == '':
                print(race_date_No, 'horse_No[', horse_No, '] has no jockey.')
            else:
                jockey_record_dict[race_date_No][horse_No] = __getJockeyRecord(horse_code, jockey, history_raceResults_rows)
    return jockey_record_dict

