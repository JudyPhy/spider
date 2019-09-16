from common import common


def GetSeasonId(race_date):   # race_date: 20190202
    str_date = str(race_date)
    year = int(str_date[len(str_date) - 6: len(str_date) - 4])
    month = int(str_date[len(str_date) - 4: len(str_date) - 2])
    if month < 8:
        return year - 1
    else:
        return year


def GetRaceInfoDict(history_raceCard_rows, history_raceResults_rows):
    race_info_dict = {}
    win_odds_dict = {}  # race_date_No & {horse_code & win_odds}
    plc_dict = {}  # race_date_No & {horse_code & plc}
    going_dict = {}  # race_date_No & {horse_code & going}
    for race_date_No, dict in history_raceCard_rows.items():
        for horse_code, row in dict.items():
            if (race_date_No in history_raceResults_rows.keys()) and (horse_code in history_raceResults_rows[race_date_No].keys()):
                plc = history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if plc not in common.words:
                    # win_odds
                    win_odds = history_raceResults_rows[race_date_No][horse_code]['win_odds']
                    if race_date_No not in win_odds_dict.keys():
                        win_odds_dict[race_date_No] = {}
                    win_odds_dict[race_date_No][horse_code] = float(win_odds)
                    # plc
                    if race_date_No not in plc_dict.keys():
                        plc_dict[race_date_No] = {}
                    plc_dict[race_date_No][horse_code] = int(plc)
                    # going
                    going = history_raceResults_rows[race_date_No][horse_code]['going'].replace(' ', '').upper()
                    if going == '':
                        going = 'GOOD'
                    if race_date_No not in going_dict.keys():
                        going_dict[race_date_No] = {}
                    going_dict[race_date_No][horse_code] = going
    race_info_dict['win_odds_dict'] = win_odds_dict
    race_info_dict['plc_dict'] = plc_dict
    race_info_dict['going_dict'] = going_dict
    return race_info_dict

