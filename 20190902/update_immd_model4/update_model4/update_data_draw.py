from update_model4 import horse_records
from update_model4 import horse_speeds
from update_model4 import records
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, cur_row, update_table, race_No, horse_No):
    # horse_draw_record
    horse_code = cur_row['horse_code']
    draw = cur_row['draw']
    horse_draw_record = __getRecords(horse_records.getDrawRecord(horse_code, draw, race_results_rows))

    # horse_draw_speed
    horse_draw_speed = horse_speeds.getDrawSpeeds(horse_code, draw, race_results_rows)

    # draw_record
    draw_record = __getRecords(records.getDrawRecords(draw, race_results_rows))

    race_date = cur_row['race_date']
    sql_update = '''update {} set horse_draw_record_before4=%s, horse_draw_record_total=%s, 
    horse_draw_best_speed=%s, horse_draw_lowest_speed=%s, horse_draw_avr_speed=%s, 
    draw_record_before4=%s, draw_record_total=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (horse_draw_record[0], horse_draw_record[1], horse_draw_speed[0], horse_draw_speed[1],
                horse_draw_speed[2], draw_record[0], draw_record[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


