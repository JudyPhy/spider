from update_model4 import horse_records
from update_model4 import horse_speeds
from update_model4 import records
from update_model4 import hot
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, cur_row, update_table, race_No, horse_No):
    # horse_jockey_record
    horse_code = cur_row['horse_code']
    array_jockey = cur_row['jockey'].split('(')
    jockey = array_jockey[0].strip()
    horse_jockey_record = __getRecords(horse_records.getJockeyRecord(horse_code, jockey, race_results_rows))

    # horse_jockey_speed
    horse_jockey_speed = horse_speeds.getJockeySpeeds(horse_code, jockey, race_results_rows)

    # jockey_record
    jockey_record = __getRecords(records.getJockeyRecords(jockey, race_results_rows))
    jockey_recent_record = __getRecords(records.getJockeyRecentRecords(jockey, race_results_rows))
    trainer = cur_row['trainer']
    jockey__trainer = jockey + '__' + trainer
    jockey_trainer_record = __getRecords(records.getJockeyTrainerRecords(jockey__trainer, race_results_rows))

    # jockey_hot
    jockey_hot = hot.getJockeyHotRecords(jockey, race_results_rows)

    race_date = cur_row['race_date']
    sql_update = '''update {} set horse_jockey_record_before4=%s, horse_jockey_record_total=%s, 
    horse_jockey_best_speed=%s, horse_jockey_lowest_speed=%s, horse_jockey_avr_speed=%s, 
    jockey_record_before4=%s, jockey_record_total=%s, jockey_recent_before4=%s, jockey_recent_total=%s,
    jockey_trainer_record_before4=%s, jockey_trainer_record_total=%s, jockey_hot=%s, 
    jockey_hot_before4=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (horse_jockey_record[0], horse_jockey_record[1], horse_jockey_speed[0], horse_jockey_speed[1],
                horse_jockey_speed[2], jockey_record[0], jockey_record[1], jockey_recent_record[0],
                jockey_recent_record[1], jockey_trainer_record[0], jockey_trainer_record[1], jockey_hot[0],
                jockey_hot[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


