from common import common


def __getJockey(race_date_No, horse_No, immd_info_dict):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array_jockey = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array_jockey[0].strip()
    return ''


def __isLoweatWinOdds(rows_dict, odds):
    for horse_code, row in rows_dict.items():
        plc = row['plc'].replace('DH', '')
        if plc not in common.words:
            cur_odds = float(row['win_odds'])
            if cur_odds < odds:
                return False
    return True


def __getJockeyHotRecords(jockey, history_raceResults_rows):
    jockey_hot_records = [0, 0]  # [hot, hot_before4]
    for race_date_No, dict in history_raceResults_rows.items():
        for horse_code, row in dict.items():
            plc = row['plc'].replace('DH', '')
            array_jockey = row['jockey'].split('(')
            cur_jockey = array_jockey[0].strip()
            cur_odds = float(row['win_odds'])
            if (plc not in common.words) and (cur_jockey == jockey) and (__isLoweatWinOdds(dict, cur_odds)):
                jockey_hot_records[0] += 1
                if (int(plc) > 0) and (int(plc) <= 4):
                    jockey_hot_records[1] += 1
    return jockey_hot_records


def GetJockeyHot(future_raceCard_rows, immd_info_dict, history_raceResults_rows):
    jockey_hot_dict = {}  # jockey & [jockey_hot, jockey_hot_before4]
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
        jockey_hot_dict[jockey] = __getJockeyHotRecords(jockey, history_raceResults_rows)
    return jockey_hot_dict

