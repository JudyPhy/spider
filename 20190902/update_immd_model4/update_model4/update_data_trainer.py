from update_model4 import records
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, cur_row, update_table, race_No, horse_No):
    # trainer_record
    trainer = cur_row['trainer']
    trainer_record = __getRecords(records.getTrainerRecords(trainer, race_results_rows))

    # jockey_trainer_record
    array_jockey = cur_row['jockey'].split('(')
    jockey = array_jockey[0].strip()
    jockey__trainer = jockey + '__' + trainer
    jockey_trainer_record = __getRecords(records.getJockeyTrainerRecords(jockey__trainer, race_results_rows))

    race_date = cur_row['race_date']
    sql_update = '''update {} set trainer_record_before4=%s, trainer_record_total=%s, 
    jockey_trainer_record_before4=%s, jockey_trainer_record_total=%s where race_date=%s and race_no=%s 
    and horse_no=%s'''.format(update_table)
    cur_data = (trainer_record[0], trainer_record[1], jockey_trainer_record[0], jockey_trainer_record[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)




