from update_model5 import records
from db.db import singleton_ResultsDb
from common import common


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def __getFavRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2]
    return [before4, rescords_array[4]]


def updateData(immd_rows, race_results_rows, cur_row, update_table, race_No, horse_No):
    # trainer_record
    array_trainer = cur_row['trainer'].split('(')
    trainer = array_trainer[0].strip()
    trainer_record = __getRecords(records.getTrainerRecords(trainer, race_results_rows))
    race_date = cur_row['race_date']
    trainer_recent_record = __getRecords(records.getTrainerRecentRecords(race_date, trainer, race_results_rows))
    trainer_fav_record = __getFavRecords(records.getTrainerFavRecords(trainer, race_results_rows))

    race_date = cur_row['race_date']
    sql_update = '''update {} set trainer_record_before4=%s, trainer_record_total=%s, 
    trainer_recent_before4=%s, trainer_recent_total=%s, trainer_fav_record_before3=%s, 
    trainer_fav_record_total=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (trainer_record[0], trainer_record[1], trainer_recent_record[0], trainer_recent_record[1],
                trainer_fav_record[0], trainer_fav_record[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)

    # same_trainer_count
    updateSameTrainerCount(immd_rows, cur_row, update_table, race_No)


def updateSameTrainerCount(immd_rows, cur_row, update_table, race_No):
    # same_trainer_count
    trainer_dict = {}  # horse_No & trainer
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
            if target_row['exit_race'] == 0:
                array_trainer = target_row['trainer'].split('(')
                trainer_dict[horse_no] = array_trainer[0].strip()
    trainer_count_dict = {}  # trainer & count
    for horse_No, trainer in trainer_dict.items():
        if trainer not in trainer_count_dict.keys():
            trainer_count_dict[trainer] = 0
        trainer_count_dict[trainer] += 1
    race_date = cur_row['race_date']
    for horse_No, trainer in trainer_dict.items():
        sql_update = '''update {} set same_trainer_count=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
        cur_data = (trainer_count_dict[trainer], race_date, race_No, horse_No)
        singleton_ResultsDb.cursor.execute(sql_update, cur_data)







