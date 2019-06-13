from common import common


def __getWinOdds(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        return results_rows[race_date_No][horse_code]['win_odds']
    return -1


def __getPlc(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        return results_rows[race_date_No][horse_code]['plc']
    return None


def getJockeyHot(raceCard_rows, results_rows):
    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    jockey_dict = {}  # race_date_No & {horse_code & jockey_hot}
    jockey_before4_dict = {}  # race_date_No & {horse_code & jockey_hot_before4}
    temp_jockey = {}  # jockey & jockey_hot
    temp_jockey_before4 = {}  # jockey & jockey_hot_before4
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in jockey_dict.keys():
            jockey_dict[race_date_No] = {}
        if race_date_No not in jockey_before4_dict.keys():
            jockey_before4_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        lowest_odds = 999
        lowest_jockey_plc_dict = {}
        for row in rows:
            horse_code = row['horse_code'].strip()
            array_jockey = row['jockey'].split('(')
            jockey = array_jockey[0].strip()

            # 赛前
            if jockey in temp_jockey.keys():
                jockey_dict[race_date_No][horse_code] = temp_jockey[jockey]
            else:
                jockey_dict[race_date_No][horse_code] = 0
            if jockey in temp_jockey_before4.keys():
                jockey_before4_dict[race_date_No][horse_code] = temp_jockey_before4[jockey]
            else:
                jockey_before4_dict[race_date_No][horse_code] = 0

            # 赛后
            plc = __getPlc(race_date_No, horse_code, results_rows)
            if plc not in common.words:
                curOdds = float(__getWinOdds(race_date_No, horse_code, results_rows))
                if (curOdds > 0) and (curOdds < lowest_odds):
                    lowest_odds = curOdds
                    lowest_jockey_plc_dict = {jockey:plc.replace('DH', '')}
                elif curOdds == lowest_odds:
                    lowest_jockey_plc_dict[jockey] = plc.replace('DH', '')

        # 赛后
        for lowest_jockey, plc in lowest_jockey_plc_dict.items():
            # temp_jockey
            if lowest_jockey not in temp_jockey:
                temp_jockey[lowest_jockey] = 0
            temp_jockey[lowest_jockey] += 1
            # temp_jockey_before4
            if lowest_jockey not in temp_jockey_before4:
                temp_jockey_before4[lowest_jockey] = 0
            if (int(plc) > 0) and (int(plc) <= 4):
                temp_jockey_before4[lowest_jockey] += 1

        # print('\n', race_date_No, lowest_odds, lowest_jockey_plc_dict)
        # for lowest_jockey in lowest_jockey_plc_dict:
        #     print(temp_jockey[lowest_jockey], temp_jockey_before4[lowest_jockey])

    return jockey_dict, jockey_before4_dict

