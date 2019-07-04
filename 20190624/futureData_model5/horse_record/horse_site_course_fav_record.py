# coding=gbk
from common import common


def __getSiteCourseFavRecords(horse_code, site, course, history_raceResults_rows):
    site_course_fav_records = [0, 0, 0, 0, 0]
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_site = dict[horse_code]['site'].replace(' ', '')
            cur_course = dict[horse_code]['course'].strip().upper()
            if '"' in cur_course:
                array = cur_course.split('"')
                cur_course = array[1].strip()
            if (plc not in common.words) and (site == cur_site) and (course == cur_course):
                win_odds = float(dict[horse_code]['win_odds'])
                isFav = common.IsLowestOdds(win_odds, dict)
                if isFav:
                    site_course_fav_records[4] += 1
                    if int(plc) == 1:
                        site_course_fav_records[0] += 1
                    elif int(plc) == 2:
                        site_course_fav_records[1] += 1
                    elif int(plc) == 3:
                        site_course_fav_records[2] += 1
                    elif int(plc) == 4:
                        site_course_fav_records[3] += 1
    return site_course_fav_records


def GetHorseSiteCourseFavRecord(future_raceCard_rows, history_raceResults_rows):
    site_course_fav_record_dict = {}  # race_date_No & {horse_No & [No1, No2, No3, No4, All]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in site_course_fav_record_dict.keys():
            site_course_fav_record_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            site = row['site'].replace(' ', '')
            course = row['course'].strip().upper()
            if '"' in course:
                array = course.split('"')
                course = array[1].strip()
            site_course_fav_record_dict[race_date_No][horse_No] = __getSiteCourseFavRecords(horse_code, site, course, history_raceResults_rows)
    return site_course_fav_record_dict

