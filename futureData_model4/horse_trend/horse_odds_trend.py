from common import common


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code].replace('DH', '')
    return -1


def __getWinOdds(race_date_No, horse_code, odds_dict):
    if (race_date_No in odds_dict.keys()) and (horse_code in odds_dict[race_date_No].keys()):
        return odds_dict[race_date_No][horse_code]
    return None


# odds_dict: race_date_No & {horse_code & win_odds}
# plc: race_date_No & {horse_code & plc}
def getOddsTrend(raceCard_rows, odds_dict, plc_dict):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    odds_trend_dict = {}  # race_date_No & {horse_code & odds_trend}
    temp_odds = {}   # horse_code & prev_odds
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in odds_trend_dict.keys():
            odds_trend_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            odds = __getWinOdds(race_date_No, horse_code, odds_dict)
            if odds == None:
                print('odds none:', race_date_No, horse_code)
            plc = __getPlc(race_date_No, horse_code, plc_dict)

            # 赛前
            if (horse_code not in temp_odds.keys()) or (plc in common.words):
                odds_trend_dict[race_date_No][horse_code] = 0
            else:
                odds_trend_dict[race_date_No][horse_code] = odds - temp_odds[horse_code]
                if odds == 0:
                    print('race horse has 0 win_odds:', race_date_No, horse_code)

            # 赛后
            if plc in common.words:
                # 无效马匹不记录
                continue
            else:
                temp_odds[horse_code] = odds

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, odds)
            #     print(temp_odds[horse_code])
            #     print(odds_trend_dict[race_date_No][horse_code])
    return odds_trend_dict


