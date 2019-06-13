from common import common


def __isLoweatWinOdds(rows_dict, odds):
    for horse_code, row in rows_dict.items():
        plc = row['plc'].replace('DH', '')
        if plc not in common.words:
            cur_odds = float(row['win_odds'])
            if cur_odds < odds:
                return False
    return True


def GetJockeyHot(sort_history_raceCard_rows, sort_history_raceResults_rows):
    jockey_hot_dict = {}  # race_date_No & {horse_code & [jockey_hot, jockey_hot_before4]}
    temp_jockey_hot = {}  # jockey & [jockey_hot, jockey_hot_before4]
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in jockey_hot_dict.keys():
            jockey_hot_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    array_jockey = sort_history_raceResults_rows[race_date_No][horse_code]['jockey'].split('(')
                    cur_jockey = array_jockey[0].strip()
                    if cur_jockey not in temp_jockey_hot.keys():
                        temp_jockey_hot[cur_jockey] = [0, 0]
                    # before
                    hot = temp_jockey_hot[cur_jockey]
                    jockey_hot_dict[race_date_No][horse_code] = [hot[0], hot[1]]
                    # after
                    cur_odds = float(sort_history_raceResults_rows[race_date_No][horse_code]['win_odds'])
                    isLowestOdds = __isLoweatWinOdds(sort_history_raceResults_rows[race_date_No], cur_odds)
                    if isLowestOdds == True:
                        temp_jockey_hot[cur_jockey][0] += 1
                        if (int(cur_plc) > 0) and (int(cur_plc) <= 4):
                            temp_jockey_hot[cur_jockey][1] += 1
    return jockey_hot_dict

