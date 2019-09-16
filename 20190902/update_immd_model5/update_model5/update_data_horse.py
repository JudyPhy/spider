from update_model5 import horse_records
from update_model5 import horse_trend
from update_model5 import data_util
from update_model5 import horse_rest
from update_model5 import horse_time
from db.db import singleton_ResultsDb


def __getRecords(horse_rescords_array):
    before4 = horse_rescords_array[0] + horse_rescords_array[1] + horse_rescords_array[2] + horse_rescords_array[3]
    return [before4, horse_rescords_array[4]]


def __getFavRecords(horse_rescords_array):
    before3 = horse_rescords_array[0] + horse_rescords_array[1] + horse_rescords_array[2]
    return [before3, horse_rescords_array[4]]


def updateData(race_results_rows, race_card_history_rows, cur_row, prev_row, update_table, race_No, horse_No):
    # records
    horse_code = cur_row['horse_code']
    horse_record = __getRecords(horse_records.getRecords(horse_code, race_results_rows))
    race_date = cur_row['race_date']
    horse_recent_records = __getRecords(horse_records.getRecentRecord(race_date, horse_code, race_results_rows))
    horse_fav_record = __getFavRecords(horse_records.getFavRecords(horse_code, race_results_rows))
    site = prev_row['site_label'].replace(' ', '')
    course = cur_row['course_label'].strip().upper()
    if '"' in course:
        array_course = course.split('"')
        course = array_course[1].strip()
    horse_site_course_records = __getRecords(horse_records.getSiteCourseRecord(horse_code, site, course, race_results_rows))
    horse_site_course_fav_records = __getFavRecords(horse_records.getSiteCourseFavRecord(horse_code, site, course, race_results_rows))
    going = cur_row['going']
    horse_going_records = __getRecords(horse_records.getGoingRecords(horse_code, going, race_results_rows))
    distance = cur_row['distance']
    horse_distance_records = __getRecords(horse_records.getDistanceRecords(horse_code, distance, race_results_rows))
    cls = prev_row['cls'].replace('Class', '').strip()
    horse_cls_records = __getRecords(horse_records.getClassRecords(horse_code, cls, race_results_rows))
    # horse_gear_records
    # horse_best_speed

    # trend
    dct = cur_row['declar_horse_wt']
    horse_dct_trend = horse_trend.getDctTrend(horse_code, dct, race_results_rows, race_card_history_rows)

    # horse speed
    horse_best_recent_speed = horse_time.getHorseBestRecentSpeed(race_date, horse_code, site, course, distance, race_results_rows)

    # rest
    horse_rests = horse_rest.getRest(horse_code, race_date, race_results_rows)

    # update db data
    sql_update = '''update {} set horse_record_before4=%s, horse_record_total=%s, 
    horse_recent_record_before4=%s, horse_recent_record_total=%s, horse_fav_record_before3=%s,
    horse_fav_record_total=%s, horse_site_course_record_before4=%s, horse_site_course_record_total=%s,
    horse_site_course_fav_record_before3=%s, horse_site_course_fav_record_total=%s,
    horse_go_record_before4=%s, horse_go_record_total=%s, horse_dst_record_before4=%s, 
    horse_dst_record_total=%s, horse_cls_record_before4=%s, horse_cls_record_total=%s, dct_trend=%s, 
    horse_best_recent_speed=%s, rest=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (horse_record[0], horse_record[1], horse_recent_records[0], horse_recent_records[1], horse_fav_record[0],
                horse_fav_record[1], horse_site_course_records[0], horse_site_course_records[1],
                horse_site_course_fav_records[0], horse_site_course_fav_records[1], horse_going_records[0],
                horse_going_records[1], horse_distance_records[0], horse_distance_records[1],
                horse_cls_records[0], horse_cls_records[1], horse_dct_trend, horse_best_recent_speed, horse_rests,
                race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)





