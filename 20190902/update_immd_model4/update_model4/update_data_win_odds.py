from update_model4 import horse_trend
from db.db import singleton_ResultsDb


def updateData(race_results_rows, immd_rows, today_race_start_time, cur_row, update_table, race_No, horse_No):
    # odd_trend
    horse_code = cur_row['horse_code']
    win_odds = float(cur_row['win_odds'])
    odd_trend = horse_trend.getOddsTrend(horse_code, win_odds, race_results_rows)

    # odd_wave
    race_date = cur_row['race_date']
    odd_wave = horse_trend.getOddsWave(race_date, race_No, horse_No, win_odds, today_race_start_time, immd_rows)

    sql_update = '''update {} set odd_trend=%s, odd_wave=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (odd_trend, odd_wave, race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


