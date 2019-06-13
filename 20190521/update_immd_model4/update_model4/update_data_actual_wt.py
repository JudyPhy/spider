from update_model4 import horse_trend
from db.db import singleton_ResultsDb


def updateData(race_results_rows, race_card_history_rows, cur_row, update_table, race_No, horse_No):
    # act_trend
    horse_code = cur_row['horse_code']
    act = cur_row['actual_wt']
    act_trend = horse_trend.getActTrend(horse_code, act, race_results_rows, race_card_history_rows)

    race_date = cur_row['race_date']
    sql_update = '''update {} set act_trend=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (act_trend, race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


