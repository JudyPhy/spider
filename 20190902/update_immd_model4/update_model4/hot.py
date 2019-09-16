from common import common


def __isLoweatWinOdds(rows_dict, odds):
    for horse_code, row in rows_dict.items():
        plc = row['plc'].replace('DH', '')
        if plc not in common.words:
            cur_odds = float(row['win_odds'])
            if cur_odds < odds:
                return False
    return True


def getJockeyHotRecords(jockey, race_results_rows):
    jockey_hot_records = [0, 0]  # [hot, hot_before4]
    for race_date_No, dict in race_results_rows.items():
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





