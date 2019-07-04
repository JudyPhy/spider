from common import common
import datetime

RECENT_COUNT = 90


def getRecords(horse_code, race_results_rows):
    records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                records[4] += 1
                if int(plc) == 1:
                    records[0] += 1
                elif int(plc) == 2:
                    records[1] += 1
                elif int(plc) == 3:
                    records[2] += 1
                elif int(plc) == 4:
                    records[3] += 1
    return records


def getRecentRecord(cur_race_date, horse_code, race_results_rows):
    cur_year = int(cur_race_date[: len(cur_race_date) - 4])
    cur_month = int(cur_race_date[len(cur_race_date) - 4: len(cur_race_date) - 2])
    cur_day = int(cur_race_date[len(cur_race_date) - 2:])
    cur_race_date = datetime.datetime(cur_year, cur_month, cur_day)
    before_N_date = common.GetBeforeNDayDate(cur_race_date, RECENT_COUNT)
    records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            race_date = race_date_No[: len(race_date_No) - 2]
            if (plc not in common.words) and (int(race_date) >= int(before_N_date)):
                records[4] += 1
                if int(plc) == 1:
                    records[0] += 1
                elif int(plc) == 2:
                    records[1] += 1
                elif int(plc) == 3:
                    records[2] += 1
                elif int(plc) == 4:
                    records[3] += 1
    return records


def getFavRecords(horse_code, race_results_rows):
    records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            if plc not in common.words:
                cur_odds = float(dict[horse_code]['win_odds'])
                isFav = common.IsLowestOdds(cur_odds, dict)
                if isFav:
                    records[4] += 1
                    if int(plc) == 1:
                        records[0] += 1
                    elif int(plc) == 2:
                        records[1] += 1
                    elif int(plc) == 3:
                        records[2] += 1
                    elif int(plc) == 4:
                        records[3] += 1
    return records


def getSiteCourseRecord(horse_code, site, course, race_results_rows):
    site_course_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_site = dict[horse_code]['site'].replace(' ', '')
            cur_course = dict[horse_code]['course'].strip().upper()
            if '"' in cur_course:
                array_course = cur_course.split('"')
                cur_course = array_course[1].strip()
            if (plc not in common.words) and (site == cur_site) and (course == cur_course):
                site_course_records[4] += 1
                if int(plc) == 1:
                    site_course_records[0] += 1
                elif int(plc) == 2:
                    site_course_records[1] += 1
                elif int(plc) == 3:
                    site_course_records[2] += 1
                elif int(plc) == 4:
                    site_course_records[3] += 1
    return site_course_records


def getSiteCourseFavRecord(horse_code, site, course, race_results_rows):
    site_course_Fav_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_site = dict[horse_code]['site'].replace(' ', '')
            cur_course = dict[horse_code]['course'].strip().upper()
            if '"' in cur_course:
                array_course = cur_course.split('"')
                cur_course = array_course[1].strip()
            if (plc not in common.words) and (site == cur_site) and (course == cur_course):
                cur_odds = float(dict[horse_code]['win_odds'])
                isFav = common.IsLowestOdds(cur_odds, dict)
                if isFav:
                    site_course_Fav_records[4] += 1
                    if int(plc) == 1:
                        site_course_Fav_records[0] += 1
                    elif int(plc) == 2:
                        site_course_Fav_records[1] += 1
                    elif int(plc) == 3:
                        site_course_Fav_records[2] += 1
                    elif int(plc) == 4:
                        site_course_Fav_records[3] += 1
    return site_course_Fav_records


def getGoingRecords(horse_code, going, race_results_rows):
    going_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_going = dict[horse_code]['going'].replace(' ', '').upper()
            if cur_going == '':
                cur_going = 'GOOD'
            if (plc not in common.words) and (cur_going == going):
                going_records[4] += 1
                if int(plc) == 1:
                    going_records[0] += 1
                elif int(plc) == 2:
                    going_records[1] += 1
                elif int(plc) == 3:
                    going_records[2] += 1
                elif int(plc) == 4:
                    going_records[3] += 1
    return going_records


def getDistanceRecords(horse_code, distance, race_results_rows):
    distance_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_distance = int(dict[horse_code]['distance'])
            if (plc not in common.words) and (cur_distance == distance):
                distance_records[4] += 1
                if int(plc) == 1:
                    distance_records[0] += 1
                elif int(plc) == 2:
                    distance_records[1] += 1
                elif int(plc) == 3:
                    distance_records[2] += 1
                elif int(plc) == 4:
                    distance_records[3] += 1
    return distance_records


def getClassRecords(horse_code, cls, race_results_rows):
    cls_records = [0, 0, 0, 0, 0]  # [No1, No2, No3, No4, All]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_cls = dict[horse_code]['cls'].replace('Class', '').strip()
            if (plc not in common.words) and (cur_cls == cls):
                cls_records[4] += 1
                if int(plc) == 1:
                    cls_records[0] += 1
                elif int(plc) == 2:
                    cls_records[1] += 1
                elif int(plc) == 3:
                    cls_records[2] += 1
                elif int(plc) == 4:
                    cls_records[3] += 1
    return cls_records


def __getGearList(gear):
    array_gear = gear.split('/')
    gear_list = []
    for sub in array_gear:
        for number in range(10):
            sub = sub.replace(str(number), '')
        if ('-' in sub) or (sub == ''):
            sub = '-'
        if sub not in gear_list:
            gear_list.append(sub)
    return gear_list


def getGearRecord(horse_code, draw, race_results_rows):
    draw_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in race_results_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_draw = dict[horse_code]['draw']
            if (plc not in common.words) and (int(cur_draw) == draw):
                draw_records[4] += 1
                if int(plc) == 1:
                    draw_records[0] += 1
                elif int(plc) == 2:
                    draw_records[1] += 1
                elif int(plc) == 3:
                    draw_records[2] += 1
                elif int(plc) == 4:
                    draw_records[3] += 1
    return draw_records

