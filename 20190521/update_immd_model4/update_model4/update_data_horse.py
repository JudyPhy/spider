from update_model4 import horse_records
from update_model4 import horse_speeds
from update_model4 import horse_trend
from update_model4 import data_util
from update_model4 import horse_rest
from update_model4 import horse_new_dis
from db.db import singleton_ResultsDb


def __getRecords(horse_rescords_array):
    before4 = horse_rescords_array[0] + horse_rescords_array[1] + horse_rescords_array[2] + horse_rescords_array[3]
    return [before4, horse_rescords_array[4]]


def updateData(race_results_rows, race_card_history_rows, display_sectional_time_rows, cur_row, prev_row, update_table, race_No, horse_No):
    # records
    horse_code = cur_row['horse_code']
    horse_record = __getRecords(horse_records.getRecords(horse_code, race_results_rows))
    horse_recent_records = __getRecords(horse_records.getRecentRecord(horse_code, race_results_rows))
    site = prev_row['site_label']
    horse_site_records = __getRecords(horse_records.getSiteRecord(horse_code, site, race_results_rows))
    going = cur_row['going']
    horse_going_records = __getRecords(horse_records.getGoingRecords(horse_code, going, race_results_rows))
    course = cur_row['course_label']
    horse_course_records = __getRecords(horse_records.getCorseRecords(horse_code, course, race_results_rows))
    distance = cur_row['distance']
    horse_distance_records = __getRecords(horse_records.getDistanceRecords(horse_code, distance, race_results_rows))
    cls = prev_row['cls'].replace('Class', '').strip()
    horse_cls_records = __getRecords(horse_records.getClassRecords(horse_code, cls, race_results_rows))
    draw = cur_row['draw']
    horse_draw_records = __getRecords(horse_records.getDrawRecord(horse_code, draw, race_results_rows))
    array_jockey = cur_row['jockey'].split('(')
    jockey = array_jockey[0].strip()
    horse_jockey_records = __getRecords(horse_records.getJockeyRecord(horse_code, jockey, race_results_rows))

    # speeds
    horse_speed = horse_speeds.getSpeeds(horse_code, race_results_rows)
    horse_recent_speeds = horse_speeds.getRecentSpeed(horse_code, race_results_rows)
    horse_site_speeds = horse_speeds.getSiteSpeeds(horse_code, site, race_results_rows)
    horse_going_speeds = horse_speeds.getGoingSpeeds(horse_code, going, race_results_rows)
    horse_course_speeds = horse_speeds.getCourseSpeeds(horse_code, course, race_results_rows)
    horse_distance_speeds = horse_speeds.getDistanceSpeeds(horse_code, distance, race_results_rows)
    horse_cls_speeds = horse_speeds.getClassSpeeds(horse_code, cls, race_results_rows)
    horse_draw_speeds = horse_speeds.getDrawSpeeds(horse_code, draw, race_results_rows)
    gear_list = data_util.getGearList(prev_row['gear_label'].strip())
    horse_gear_speeds = horse_speeds.getGearSpeeds(horse_code, gear_list, race_results_rows, race_card_history_rows)
    horse_jockey_speeds = horse_speeds.getJockeySpeeds(horse_code, jockey, race_results_rows)
    horse_last_dst_time = horse_speeds.getLastDstTimeArray(horse_code, site, course, going, distance, race_results_rows, display_sectional_time_rows)

    # trend
    dct = cur_row['declar_horse_wt']
    horse_dct_trend = horse_trend.getDctTrend(horse_code, dct, race_results_rows, race_card_history_rows)
    act = cur_row['actual_wt']
    horse_act_trend = horse_trend.getActTrend(horse_code, act, race_results_rows, race_card_history_rows)
    win_odds = float(cur_row['win_odds'])
    horse_odds_trend = horse_trend.getOddsTrend(horse_code, win_odds, race_results_rows)

    # rest
    race_date = cur_row['race_date']
    horse_rests = horse_rest.getRest(horse_code, race_date, race_results_rows)

    # new_dis
    horse_new_distance = horse_new_dis.getNewDis(horse_code, distance, race_results_rows)

    # update db data
    sql_update = '''update {} set horse_record_before4=%s, horse_record_total=%s, 
    horse_recent_record_before4=%s, horse_recent_record_total=%s, horse_site_record_before4=%s, 
    horse_site_record_total=%s, horse_go_record_before4=%s, horse_go_record_total=%s,
    horse_course_record_before4=%s, horse_course_record_total=%s, horse_dst_record_before4=%s, 
    horse_dst_record_total=%s, horse_cls_record_before4=%s, horse_cls_record_total=%s, 
    horse_draw_record_before4=%s, horse_draw_record_total=%s, horse_jockey_record_before4=%s, 
    horse_jockey_record_total=%s, horse_best_speed=%s, horse_lowest_speed=%s, horse_avr_speed=%s,
    horse_recent_best_speed=%s, horse_recent_lowest_speed=%s, horse_recent_avr_speed=%s,
    horse_site_best_speed=%s, horse_site_lowest_speed=%s, horse_site_avr_speed=%s, 
    horse_go_best_speed=%s, horse_go_lowest_speed=%s, horse_go_avr_speed=%s, 
    horse_course_best_speed=%s, horse_course_lowest_speed=%s, horse_course_avr_speed=%s,
    horse_dst_best_speed=%s, horse_dst_lowest_speed=%s, horse_dst_avr_speed=%s, 
    horse_cls_best_speed=%s, horse_cls_lowest_speed=%s, horse_cls_avr_speed=%s, 
    horse_draw_best_speed=%s, horse_draw_lowest_speed=%s, horse_draw_avr_speed=%s, 
    horse_gear_best_speed=%s, horse_gear_lowest_speed=%s, horse_gear_avr_speed=%s, 
    horse_jockey_best_speed=%s, horse_jockey_lowest_speed=%s, horse_jockey_avr_speed=%s, dct_trend=%s, 
    act_trend=%s, odd_trend=%s, rest=%s, new_dis=%s, horse_last_dst_time_prev=%s, 
    horse_last_dst_time_ave=%s, horse_last_dst_time_min=%s where race_date=%s and race_no=%s and horse_no=%s'''.format(update_table)
    cur_data = (horse_record[0], horse_record[1], horse_recent_records[0], horse_recent_records[1],
                horse_site_records[0], horse_site_records[1], horse_going_records[0], horse_going_records[1],
                horse_course_records[0], horse_course_records[1], horse_distance_records[0], horse_distance_records[1],
                horse_cls_records[0], horse_cls_records[1], horse_draw_records[0], horse_draw_records[1],
                horse_jockey_records[0], horse_jockey_records[1], horse_speed[0], horse_speed[1], horse_speed[2],
                horse_recent_speeds[0], horse_recent_speeds[1], horse_recent_speeds[2], horse_site_speeds[0],
                horse_site_speeds[1], horse_site_speeds[2], horse_going_speeds[0], horse_going_speeds[1],
                horse_going_speeds[2], horse_course_speeds[0], horse_course_speeds[1], horse_course_speeds[2],
                horse_distance_speeds[0], horse_distance_speeds[1], horse_distance_speeds[2], horse_cls_speeds[0],
                horse_cls_speeds[1], horse_cls_speeds[2], horse_draw_speeds[0], horse_draw_speeds[1],
                horse_draw_speeds[2], horse_gear_speeds[0], horse_gear_speeds[1], horse_gear_speeds[2],
                horse_jockey_speeds[0], horse_jockey_speeds[1], horse_jockey_speeds[2], horse_dct_trend, horse_act_trend,
                horse_odds_trend, horse_rests, horse_new_distance, horse_last_dst_time[0], horse_last_dst_time[1],
                horse_last_dst_time[2], race_date, race_No, horse_No)
    singleton_ResultsDb.cursor.execute(sql_update, cur_data)





