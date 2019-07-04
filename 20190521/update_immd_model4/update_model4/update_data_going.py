from update_model4 import horse_records
from update_model4 import horse_speeds
from db.db import singleton_ResultsDb


def __getRecords(rescords_array):
    before4 = rescords_array[0] + rescords_array[1] + rescords_array[2] + rescords_array[3]
    return [before4, rescords_array[4]]


def updateData(race_results_rows, display_sectional_time_rows, cur_row, prev_row, update_table, race_No, horse_No):
    # horse_go_record
    horse_code = cur_row['horse_code']
    going = cur_row['going']
    horse_go_record = __getRecords(horse_records.getGoingRecords(horse_code, going, race_results_rows))

    # horse_go_speed
    horse_go_speed = horse_speeds.getGoingSpeeds(horse_code, going, race_results_rows)

    # horse_last_dst_time
    site = prev_row['site_label']
    course = cur_row['course'].strip()
    if '"' in course:
        array_course = course.split('"')
        course = array_course[1].strip()
    distance = cur_row['distance']
    horse_last_dst_time = horse_speeds.getLastDstTimeArray(horse_code, site, course, going, distance, race_results_rows, display_sectional_time_rows)

    race_date = cur_row['race_date']
    sql_update = '''update {} set horse_go_record_before4=%s, horse_go_record_total=%s, 
    horse_go_best_speed=%s, horse_go_lowest_speed=%s, horse_go_avr_speed=%s, 
    horse_last_dst_time_prev=%s, horse_last_dst_time_ave=%s, horse_last_dst_time_min=%s 
    where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (horse_go_record[0], horse_go_record[1], horse_go_speed[0], horse_go_speed[1],
                horse_go_speed[2], horse_last_dst_time[0], horse_last_dst_time[1], horse_last_dst_time[2], race_date,
                race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)


