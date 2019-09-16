from update_model5 import horse_records
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, cur_row, prev_row, update_table, race_No, horse_No):
    # horse_go_record
    horse_code = cur_row['horse_code']
    going = cur_row['going']
    horse_go_record = __getRecords(horse_records.getGoingRecords(horse_code, going, race_results_rows))

    race_date = cur_row['race_date']
    sql_update = '''update {} set horse_going_record_before4=%s, horse_going_record_total=%s where race_date=%s 
    and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (horse_go_record[0], horse_go_record[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


