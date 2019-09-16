from common import common


def __getJockey(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array_jockey = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array_jockey[0].strip()
    return ''


def __getJockeyFavRecords(jockey, history_raceResults_rows):
    jockey_fav_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in history_raceResults_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            if (plc not in common.words) and (cur_jockey == jockey):
                cur_odds = float(row['win_odds'])
                isFav = common.IsLowestOdds(cur_odds, dict)
                if isFav:
                    jockey_fav_records[4] += 1
                    if int(plc) == 1:
                        jockey_fav_records[0] += 1
                    elif int(plc) == 2:
                        jockey_fav_records[1] += 1
                    elif int(plc) == 3:
                        jockey_fav_records[2] += 1
                    elif int(plc) == 4:
                        jockey_fav_records[3] += 1
    return jockey_fav_records


def GetJockeyFavRecent(future_raceCard_rows, immd_info_dict, history_raceResults_rows):
    jockey_fav_record_dict = {}  # jockey & [No1, No2, No3, No4, All]
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
        jockey_fav_record_dict[jockey] = __getJockeyFavRecords(jockey, history_raceResults_rows)
    return jockey_fav_record_dict

