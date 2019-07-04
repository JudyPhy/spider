from common import common


def __getTrackRecords(track, history_raceResults_rows):
    track_records = 0
    for race_date_No, dict in history_raceResults_rows.items():
        rows = list(dict.values())
        site = rows[0]['site'].replace(' ', '')
        course = rows[0]['course'].strip().upper()
        if '"' in course:
            array_course = course.split('"')
            course = array_course[1].strip()
        cur_site_course = site + '_' + course
        if cur_site_course == track:
            track_records += 1
    return track_records


def GetTrackRecord(future_raceCard_rows, history_raceResults_rows):
    track_record_dict = {}  # track & record
    track_list = []
    for race_date_No, dict in future_raceCard_rows.items():
        for horse_No, row in dict.items():
            site = row['site'].replace(' ', '')
            course = row['course'].strip().upper()
            if '"' in course:
                array_course = course.split('"')
                course = array_course[1].strip()
            cur_site_course = site + '_' + course
            if cur_site_course not in track_list:
                track_list.append(cur_site_course)
    for track in track_list:
        track_record_dict[track] = __getTrackRecords(track, history_raceResults_rows)
    return track_record_dict

