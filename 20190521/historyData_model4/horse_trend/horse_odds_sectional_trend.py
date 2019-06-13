from common import common


def getOddsSectionalTrend(sort_history_raceCard_rows, sort_history_raceResults_rows, odds_sectional_rows):
    odds_sectional_trend_dict = {}  # race_date_No & {horse_code & odds_sectional_trend}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in odds_sectional_trend_dict.keys():
            odds_sectional_trend_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    horse_No = int(row['horse_No'])
                    if (race_date_No in odds_sectional_rows.keys()) and (horse_No in odds_sectional_rows[race_date_No].keys()):
                        odds3 = odds_sectional_rows[race_date_No][horse_No]['odds3']
                        odds4 = odds_sectional_rows[race_date_No][horse_No]['odds4']
                        if odds3 == '' or odds4 == '':
                            odds_sectional_trend_dict[race_date_No][horse_code] = 1
                        else:
                            odds_sectional_trend_dict[race_date_No][horse_code] = (float(odds4) - float(odds3))/float(odds3)
    return odds_sectional_trend_dict


