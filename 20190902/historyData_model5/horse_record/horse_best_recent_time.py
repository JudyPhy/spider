from common import common
import datetime


RECENT_COUNT = 90


def GetHorseBestRecentSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_best_recent_speed_dict = {}  # race_date_No & {horse_code & best_speed}
    temp_horse_cls_record = {}  # horse_code & {site_course_dst & {race_date_No & finish_time}}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_best_recent_speed_dict.keys():
            horse_best_recent_speed_dict[race_date_No] = {}
        cur_race_date = race_date_No[: len(race_date_No) - 2]
        cur_year = int(cur_race_date[: len(cur_race_date) - 4])
        cur_month = int(cur_race_date[len(cur_race_date) - 4: len(cur_race_date) - 2])
        cur_day = int(cur_race_date[len(cur_race_date) - 2:])
        cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
        before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                cur_site = sort_history_raceResults_rows[race_date_No][horse_code]['site'].replace(' ', '')
                cur_course = sort_history_raceResults_rows[race_date_No][horse_code]['course'].strip().upper()
                if '"' in cur_course:
                    array_course = cur_course.split('"')
                    cur_course = array_course[1].strip()
                cur_distance = sort_history_raceResults_rows[race_date_No][horse_code]['distance']
                cur_site_course_dst = cur_site + '_' + cur_course + '_' + cur_distance
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_cls_record.keys():
                        temp_horse_cls_record[horse_code] = {}
                    if cur_site_course_dst not in temp_horse_cls_record[horse_code].keys():
                        temp_horse_cls_record[horse_code][cur_site_course_dst] = {}
                    # before
                    best_time = 9999
                    for cur_race_date_No, finish_time in temp_horse_cls_record[horse_code][cur_site_course_dst].items():
                        cur_race_date = cur_race_date_No[: len(cur_race_date_No) - 2]
                        if (int(cur_race_date) >= int(before_N_date)) and (finish_time < best_time):
                            best_time = finish_time
                    if best_time == 9999:
                        horse_best_recent_speed_dict[race_date_No][horse_code] = 0
                    else:
                        horse_best_recent_speed_dict[race_date_No][horse_code] = int(cur_distance) / best_time
                    # after
                    cur_finish_time = common.GetTotalSeconds(sort_history_raceResults_rows[race_date_No][horse_code]['finish_time'])
                    temp_horse_cls_record[horse_code][cur_site_course_dst][race_date_No] = cur_finish_time

                    # if 'S122' == horse_code:
                    #     print('\n', race_date_No, cur_site_course_dst, before_N_date)
                    #     print(temp_horse_cls_record[horse_code][cur_site_course_dst], cur_finish_time)
                    #     print(horse_best_recent_time_dict[race_date_No][horse_code])
    return horse_best_recent_speed_dict

