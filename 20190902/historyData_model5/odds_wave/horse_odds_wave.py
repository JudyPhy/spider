from common import common


def getOddsWave(sort_history_raceCard_rows, sort_history_raceResults_rows, odds_sectional_rows, odds_immd_sectional_rows):
    odds_wave_dict = {}  # race_date_No & {horse_code & odds_wave}
    # 先从苹果网提取
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in odds_wave_dict.keys():
            odds_wave_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (
                    horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    horse_No = int(row['horse_No'])
                    if (race_date_No in odds_sectional_rows.keys()) and (
                            horse_No in odds_sectional_rows[race_date_No].keys()):
                        old_odds = odds_sectional_rows[race_date_No][horse_No]['odds3']
                        cur_odds = odds_sectional_rows[race_date_No][horse_No]['odds4']
                        if old_odds == '' or cur_odds == '':
                            odds_wave_dict[race_date_No][horse_code] = 1
                        else:
                            odds_wave_dict[race_date_No][horse_code] = (float(cur_odds) - float(old_odds)) / float(
                                old_odds)

    # 再用immd表中数据覆盖
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in odds_wave_dict.keys():
            odds_wave_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    horse_No = int(row['horse_No'])
                    if (race_date_No in odds_immd_sectional_rows.keys()) and (horse_No in odds_immd_sectional_rows[race_date_No].keys()):
                        old_odds = odds_immd_sectional_rows[race_date_No][horse_No]['before10_odds']
                        cur_odds = sort_history_raceResults_rows[race_date_No][horse_code]['win_odds']
                        if old_odds == '' or cur_odds == '':
                            odds_wave_dict[race_date_No][horse_code] = 1
                        else:
                            odds_wave_dict[race_date_No][horse_code] = (float(cur_odds) - float(old_odds)) / float(old_odds)
    return odds_wave_dict


def getOddsDiff(sort_history_raceCard_rows, sort_history_raceResults_rows, odds_sectional_rows, odds_immd_sectional_rows):
    odds_trend_dict = {}  # race_date_No & {horse_code & odds_trend}
    # 先从苹果网提取
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in odds_trend_dict.keys():
            odds_trend_dict[race_date_No] = {}
        else:
            continue
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (
                    horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    horse_No = int(row['horse_No'])
                    if (race_date_No in odds_sectional_rows.keys()) and (
                            horse_No in odds_sectional_rows[race_date_No].keys()):
                        old_odds = odds_sectional_rows[race_date_No][horse_No]['odds3']
                        cur_odds = odds_sectional_rows[race_date_No][horse_No]['odds4']
                        if old_odds == '' or cur_odds == '':
                            odds_trend_dict[race_date_No][horse_code] = 0
                        else:
                            odds_trend_dict[race_date_No][horse_code] = float(cur_odds) - float(old_odds)

    # 再用immd表中数据覆盖
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in odds_trend_dict.keys():
            odds_trend_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    horse_No = int(row['horse_No'])
                    if (race_date_No in odds_immd_sectional_rows.keys()) and (horse_No in odds_immd_sectional_rows[race_date_No].keys()):
                        old_odds = odds_immd_sectional_rows[race_date_No][horse_No]['before10_odds']
                        cur_odds = sort_history_raceResults_rows[race_date_No][horse_code]['win_odds']
                        if old_odds == '' or cur_odds == '':
                            odds_trend_dict[race_date_No][horse_code] = 0
                        else:
                            odds_trend_dict[race_date_No][horse_code] = float(cur_odds) - float(old_odds)
    return odds_trend_dict


