from common import common


def __getTrackFavRecords(site_course, history_raceResults_rows):
    track_fav_record = 0
    for race_date_No, dict in history_raceResults_rows.items():
        rows = list(dict.values())
        cur_site = rows[0]['site'].replace(' ', '')
        cur_course = rows[0]['course'].strip().upper()
        if '"' in cur_course:
            array_course = cur_course.split('"')
            cur_course = array_course[1].strip()
        cur_site_course = cur_site + '_' + cur_course
        if cur_site_course == site_course:
            fav_is_before3 = False
            for horse_code, row in dict.items():
                plc = row['plc'].replace('DH', '')
                if plc not in common.words:
                    cur_odds = float(row['win_odds'])
                    isFav = common.IsLowestOdds(cur_odds, dict)
                    if isFav and (int(plc) <= 3):
                        fav_is_before3 = True
            if fav_is_before3:
                track_fav_record += 1
    return track_fav_record


def GetTrackFavRecord(future_raceCard_rows, history_raceResults_rows):
    track_fav_record_dict = {}  # site_course & record
    site_course_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            site = row['site'].replace(' ', '')
            course = row['course'].strip().upper()
            if '"' in course:
                array_course = course.split('"')
                course = array_course[1].strip()
            site_course = site + '_' + course
            if site_course not in site_course_list:
                site_course_list.append(site_course)
    for site_course in site_course_list:
        track_fav_record_dict[site_course] = __getTrackFavRecords(site_course, history_raceResults_rows)
    return track_fav_record_dict

