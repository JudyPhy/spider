from common import common


def GetJockeyFavRecord(sort_race_date_rows, sort_history_raceResults_rows):
    jockey_fav_record_dict = {}  # race_date & {jockey & [No1, No2, No3, No4, All]}
    temp_fav_record_dict = {}   # jockey & [No1, No2, No3, No4, All]}
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in jockey_fav_record_dict.keys():
            jockey_fav_record_dict[race_date] = {}
        for row in rows:
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if cur_jockey not in temp_fav_record_dict.keys():
                temp_fav_record_dict[cur_jockey] = [0, 0, 0, 0, 0]
            # before
            records = temp_fav_record_dict[cur_jockey]
            jockey_fav_record_dict[race_date][cur_jockey] = [records[0], records[1], records[2], records[3], records[4]]
        # after
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            horse_code = row['horse_code'].strip()
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    array_jockey = sort_history_raceResults_rows[race_date_No][horse_code]['jockey'].split('(')
                    cur_jockey = array_jockey[0].strip()
                    cur_odds = float(sort_history_raceResults_rows[race_date_No][horse_code]['win_odds'])
                    isFav = common.IsLowestOdds(cur_odds, sort_history_raceResults_rows[race_date_No])
                    if isFav:
                        temp_fav_record_dict[cur_jockey][4] += 1
                        if int(cur_plc) == 1:
                            temp_fav_record_dict[cur_jockey][0] += 1
                        elif int(cur_plc) == 2:
                            temp_fav_record_dict[cur_jockey][1] += 1
                        elif int(cur_plc) == 3:
                            temp_fav_record_dict[cur_jockey][2] += 1
                        elif int(cur_plc) == 4:
                            temp_fav_record_dict[cur_jockey][3] += 1
    return jockey_fav_record_dict

