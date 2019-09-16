from update_model5 import horse_trend
from db.db import singleton_ResultsDb
from common import common


def __isLoweatOdds(odds, odds_dict):
    for horse_No, cur_odds in odds_dict.items():
        if cur_odds < odds:
            return False
    return True


def updateData(immd_rows, today_race_start_time, cur_row, update_table, race_No, horse_No):
    # odd_wave
    race_date = cur_row['race_date']
    win_odds = float(cur_row['win_odds'])
    odd_wave = horse_trend.getOddsWave(race_date, race_No, horse_No, win_odds, today_race_start_time, immd_rows)
    odd_diff = horse_trend.getOddsDiff(race_date, race_No, horse_No, win_odds, today_race_start_time, immd_rows)

    sql_update = '''update {} set odd_wave=%s, odd_diff=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (odd_wave, odd_diff, race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)

    # fav_match
    odds_dict = {}  # horse_No & odds
    if race_No in immd_rows.keys():
        for horse_no, rows in immd_rows[race_No].items():
            target_row = None
            for row in rows:
                cur_update_time = common.toDateTime(row['update_time'])
                if target_row == None:
                    target_row = row
                else:
                    prev_update_time = common.toDateTime(target_row['update_time'])
                    if cur_update_time > prev_update_time:
                        target_row = row
            if target_row['exit_race'] == 1:
                continue
            cur_odds = target_row['win_odds']
            if 'SCR' in cur_odds:
                continue
            odds_dict[horse_no] = float(cur_odds)
    for horse_no, odds in odds_dict.items():
        isFav = __isLoweatOdds(odds, odds_dict)
        sql_update = '''update {} set fav_match=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
        cur_data = (isFav, race_date, race_No, horse_no)
        singleton_ResultsDb.cursor.execute(sql_update, cur_data)




