from common import common

RECENT_COUNT = 6


def GetJockeyRecent(sort_race_date_rows, sort_history_raceResults_rows):
    jockey_recent_dict = {}  # race_date & {jockey & [No1, No2, No3, No4, All]}
    temp_jockey_date_records = {}  # jockey & {race_date & [No1, No2, No3, No4, All]}
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in jockey_recent_dict.keys():
            jockey_recent_dict[race_date] = {}
        for row in rows:
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if cur_jockey not in temp_jockey_date_records.keys():
                temp_jockey_date_records[cur_jockey] = {}
            # before
            array_list = list(temp_jockey_date_records[cur_jockey].values())
            start_index = 0
            if len(array_list) >= RECENT_COUNT:
                start_index = len(array_list) - RECENT_COUNT
            records = [0, 0, 0, 0, 0]
            for array in array_list[start_index:]:
                records[0] += array[0]
                records[1] += array[1]
                records[2] += array[2]
                records[3] += array[3]
                records[4] += array[4]
            jockey_recent_dict[race_date][cur_jockey] = records
        # after
        cur_day_records = {}    # jockey & [No1, No2, No3, No4, All]
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            horse_code = row['horse_code'].strip()
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    array_jockey = sort_history_raceResults_rows[race_date_No][horse_code]['jockey'].split('(')
                    cur_jockey = array_jockey[0].strip()
                    if cur_jockey not in cur_day_records.keys():
                        cur_day_records[cur_jockey] = [0, 0, 0, 0, 0]
                    cur_day_records[cur_jockey][4] += 1
                    if int(cur_plc) == 1:
                        cur_day_records[cur_jockey][0] += 1
                    elif int(cur_plc) == 2:
                        cur_day_records[cur_jockey][1] += 1
                    elif int(cur_plc) == 3:
                        cur_day_records[cur_jockey][2] += 1
                    elif int(cur_plc) == 4:
                        cur_day_records[cur_jockey][3] += 1
        for jockey, array in cur_day_records.items():
            temp_jockey_date_records[jockey][race_date] = array
    return jockey_recent_dict

