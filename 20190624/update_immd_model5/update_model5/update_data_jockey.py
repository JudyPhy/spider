from update_model5 import records
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def __getFavRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, cur_row, update_table, race_No, horse_No):
    # jockey_record
    array_jockey = cur_row['jockey'].split('(')
    jockey = array_jockey[0].strip()
    jockey_record = __getRecords(records.getJockeyRecords(jockey, race_results_rows))
    race_date = cur_row['race_date']
    jockey_recent_record = __getRecords(records.getJockeyRecentRecords(race_date, jockey, race_results_rows))
    jockey_fav_record = __getFavRecords(records.getJockeyFavRecords(jockey, race_results_rows))

    race_date = cur_row['race_date']
    sql_update = '''update {} set jockey_record_before4=%s, jockey_record_total=%s, 
    jockey_recent_before4=%s, jockey_recent_total=%s, jockey_fav_record_before3=%s,
    jockey_fav_record_total=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (jockey_record[0], jockey_record[1], jockey_recent_record[0], jockey_recent_record[1],
                jockey_fav_record[0], jockey_fav_record[1], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


