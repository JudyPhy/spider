from common import common


def GetHorseWinOddsTrend(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_win_odds_trend_dict = {}  # race_date_No & {horse_code & win_odds_trend}
    temp_horse_win_odds_prev = {}   # horse_code & prev_win_odds
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_win_odds_trend_dict.keys():
            horse_win_odds_trend_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_win_odds_prev.keys():
                        temp_horse_win_odds_prev[horse_code] = -1
                    cur_win_odds = float(sort_history_raceResults_rows[race_date_No][horse_code]['win_odds'])
                    # before
                    if temp_horse_win_odds_prev[horse_code] == -1:
                        horse_win_odds_trend_dict[race_date_No][horse_code] = 0
                    else:
                        horse_win_odds_trend_dict[race_date_No][horse_code] = cur_win_odds - temp_horse_win_odds_prev[horse_code]
                    # after
                    temp_horse_win_odds_prev[horse_code] = cur_win_odds
    return horse_win_odds_trend_dict


