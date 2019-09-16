from common import common

RECENT_COUNT = 6


def __getJockey(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array_jockey = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array_jockey[0].strip()
    return ''


def __getJockeyRecentRecords(jockey, history_raceResults_rows):
    sort_race_date_No_list = sorted(list(history_raceResults_rows.keys()))
    sort_race_date_No_list.reverse()
    jockey_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    race_date_list = []
    for race_date_No in sort_race_date_No_list:
        race_date = race_date_No[: len(race_date_No) - 2]
        dict = history_raceResults_rows[race_date_No]
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey):
                if race_date not in race_date_list:
                    race_date_list.append(race_date)
                if len(race_date_list) > RECENT_COUNT:
                    return jockey_records
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


def GetJockeyRecent(future_raceCard_rows, immd_info_dict, history_raceResults_rows):
    jockey_recent_dict = {}  # jockey & [No1, No2, No3, No4, All]
    jockey_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            jockey = __getJockey(race_date_No, horse_No, immd_info_dict)
            if jockey == '':
                array_jockey = row['jockey'].split('(')
                jockey = array_jockey[0].strip()
            if jockey not in jockey_list:
                jockey_list.append(jockey)
    for jockey in jockey_list:
        jockey_recent_dict[jockey] = __getJockeyRecentRecords(jockey, history_raceResults_rows)
    return jockey_recent_dict

