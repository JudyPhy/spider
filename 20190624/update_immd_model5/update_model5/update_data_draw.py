from update_model5 import records
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, cur_row, update_table, race_No, horse_No):
    # draw_record
    draw = cur_row['draw']
    draw_record = __getRecords(records.getDrawRecords(draw, race_results_rows))

    race_date = cur_row['race_date']
    sql_update = '''update {} set draw_record_before4=%s, draw_record_total=%s where race_date=%s and 
    race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (draw_record[0], draw_record[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


