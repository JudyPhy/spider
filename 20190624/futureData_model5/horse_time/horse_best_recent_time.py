from common import common
import datetime


RECENT_COUNT = 90


def __getBestRecentSpeed(horse_code, site, course, dst, before_N_date, history_raceResults_rows):
    best_time = 9999
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            race_date = race_date_No[: len(race_date_No) - 2]
            if (plc not in common.words) and (int(race_date) >= int(before_N_date)):
                cur_site = dict[horse_code]['site'].replace(' ', '')
                cur_course = dict[horse_code]['course'].strip().upper()
                if '"' in cur_course:
                    array_course = cur_course.split('"')
                    cur_course = array_course[1].strip()
                cur_dst = int(dict[horse_code]['distance'])
                if (cur_site == site) and (cur_course == course) and (cur_dst == dst):
                    cur_time = common.GetTotalSeconds(dict[horse_code]['finish_time'])
                    if cur_time < best_time:
                        best_time = cur_time
    if best_time == 9999:
        return 0
    else:
        return dst/best_time


def GetHorseBestRecentSpeed(future_raceCard_rows, history_raceResults_rows):
    horse_best_recent_speed_dict = {}  # race_date_No & {horse_No & best_time}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in horse_best_recent_speed_dict.keys():
            horse_best_recent_speed_dict[race_date_No] = {}
        cur_race_date = race_date_No[: len(race_date_No) - 2]
        cur_year = int(cur_race_date[: len(cur_race_date) - 4])
        cur_month = int(cur_race_date[len(cur_race_date) - 4: len(cur_race_date) - 2])
        cur_day = int(cur_race_date[len(cur_race_date) - 2:])
        cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
        before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            site = row['site'].replace(' ', '')
            course = row['course'].strip().upper()
            if '"' in course:
                array_course = course.split('"')
                course = array_course[1].strip()
            dst = int(row['distance'])
            horse_best_recent_speed_dict[race_date_No][horse_No] = __getBestRecentSpeed(horse_code, site, course, dst, before_N_date, history_raceResults_rows)
    return horse_best_recent_speed_dict

