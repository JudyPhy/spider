from common import common
import datetime

RECENT_COUNT = 90


def getHorseBestRecentSpeed(race_date, horse_code, site, course, distance, race_results_rows):
    cur_year = int(race_date[: len(race_date) - 4])
    cur_month = int(race_date[len(race_date) - 4: len(race_date) - 2])
    cur_day = int(race_date[len(race_date) - 2:])
    cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
    before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
    best_time = 9999
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_date = dict[horse_code]['race_date']
            cur_site = dict[horse_code]['site'].replace(' ', '')
            cur_course = dict[horse_code]['course'].strip().upper()
            if '"' in cur_course:
                array_course = cur_course.split('"')
                cur_course = array_course[1].strip()
            cur_dst = int(dict[horse_code]['distance'])
            if (plc not in common.words) and (int(cur_date) >= int(before_N_date)) and (cur_site == site) \
                    and (cur_course == course) and (cur_dst == distance):
                cur_time = common.GetTotalSeconds(dict[horse_code]['finish_time'])
                if cur_time < best_time:
                    best_time = cur_time
    if best_time == 9999:
        return 0
    else:
        return distance/best_time

