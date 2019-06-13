from common import common
from update_model4 import data_util
import datetime


def getDctTrend(horse_code, dct, race_results_rows, race_card_history_rows):
    sort_race_date_No = sorted(list(race_results_rows.keys()))
    sort_race_date_No.reverse()
    for race_date_No in sort_race_date_No:
        dict = race_results_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_dct = data_util.getDct(race_date_No, horse_code, race_card_history_rows)
            if plc not in common.words:
                return int(dct) - int(cur_dct)
    return 0


def getActTrend(horse_code, act, race_results_rows, race_card_history_rows):
    sort_race_date_No = sorted(list(race_results_rows.keys()))
    sort_race_date_No.reverse()
    for race_date_No in sort_race_date_No:
        dict = race_results_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_act = data_util.getAct(race_date_No, horse_code, race_card_history_rows)
            if plc not in common.words:
                return act - int(cur_act)
    return 0


def getOddsTrend(horse_code, win_odds, race_results_rows):
    sort_race_date_No = sorted(list(race_results_rows.keys()))
    sort_race_date_No.reverse()
    for race_date_No in sort_race_date_No:
        dict = race_results_rows[race_date_No]
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_win_odds = dict[horse_code]['win_odds']
            if plc not in common.words:
                return win_odds - float(cur_win_odds)
    return 0


def __getWinOddsByTime(race_No, horse_No, time, immd_rows):
    if (race_No in immd_rows.keys()) and (horse_No in immd_rows[race_No].keys()):
        immd_data_rows = immd_rows[race_No][horse_No]
        target_row = None
        for row in immd_data_rows:
            cur_update_time = common.toDateTime(row['update_time'])
            if target_row == None:
                target_row = row
            else:
                prev_update_time = common.toDateTime(target_row['update_time'])
                if (cur_update_time < time) and (cur_update_time > prev_update_time):
                    target_row = row
        return float(target_row['win_odds'])
    return 0


def getOddsWave(race_date, race_No, horse_No, win_odds, today_race_start_time, immd_rows):
    race_date_No = race_date + common.toDoubleDigitStr(race_No)
    if race_date_No in today_race_start_time.keys():
        base_time = today_race_start_time[race_date_No][0]
        before10_time = today_race_start_time[race_date_No][1]
        if (datetime.datetime.now() - before10_time).total_seconds() <= 0:
            base_odds = __getWinOddsByTime(race_No, horse_No, before10_time, immd_rows)
        else:
            base_odds = __getWinOddsByTime(race_No, horse_No, base_time, immd_rows)
        if base_odds != 0:
            return (win_odds - base_odds) / base_odds
    return 1







