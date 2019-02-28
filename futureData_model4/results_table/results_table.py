from db.database import singleton_Scrub_DB
from common import common
import datetime


def __getSeasonId(race_date):   # race_date: 20190202 int
    str_date = str(race_date)
    year = int(str_date[len(str_date) - 6: len(str_date) - 4])
    month = int(str_date[len(str_date) - 4: len(str_date) - 2])
    if month < 8:
        return year - 1
    else:
        return year


# results_rows: race_date_No & {horse_code & row}
def getWinOddsDict(raceCard_rows, results_rows):
    win_odds_dict = {}  # race_date_No & {horse_code & win_odds}
    for row_raceCard in raceCard_rows:
        horse_code = row_raceCard['horse_code'].strip()
        race_date_No = row_raceCard['race_date'] + common.toDoubleDigitStr(row_raceCard['race_No'])
        if (race_date_No in results_rows) and (horse_code in results_rows[race_date_No]):
            if race_date_No not in win_odds_dict.keys():
                win_odds_dict[race_date_No] = {}
            win_odds = results_rows[race_date_No][horse_code]['win_odds']
            win_odds_dict[race_date_No][horse_code] = win_odds
    return win_odds_dict


def getPlcDict(raceCard_rows, results_rows):
    plc_dict = {}  # race_date_No & {horse_code & plc}
    for row_raceCard in raceCard_rows:
        horse_code = row_raceCard['horse_code'].strip()
        race_date_No = row_raceCard['race_date'] + common.toDoubleDigitStr(row_raceCard['race_No'])
        if race_date_No not in plc_dict.keys():
            plc_dict[race_date_No] = {}
        if (race_date_No in results_rows) and (horse_code in results_rows[race_date_No]):
            plc = results_rows[race_date_No][horse_code]['plc'].replace('DH', '')
            plc_dict[race_date_No][horse_code] = plc
    return plc_dict


def getGoingDict(raceCard_rows, results_rows):
    going_dict = {}  # race_date_No & {horse_code & going}
    for row_raceCard in raceCard_rows:
        horse_code = row_raceCard['horse_code'].strip()
        race_date_No = row_raceCard['race_date'] + common.toDoubleDigitStr(row_raceCard['race_No'])
        if (race_date_No in results_rows) and (horse_code in results_rows[race_date_No]):
            if race_date_No not in going_dict.keys():
                going_dict[race_date_No] = {}
            going = results_rows[race_date_No][horse_code]['going'].replace(' ', '').upper()
            if going == '':
                going = 'GOOD'
            going_dict[race_date_No][horse_code] = going
    return going_dict

