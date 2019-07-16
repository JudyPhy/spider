from common import common


def __getDateNoTrack(sort_race_date_rows):
    date_No_track_dit = {}  # race_date & {race_No & track}
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in date_No_track_dit.keys():
            date_No_track_dit[race_date] = {}
        for row in rows:
            race_No = row['race_No']
            if race_No not in date_No_track_dit[race_date].keys():
                cur_site = row['site'].replace(' ', '')
                cur_course = row['course'].strip().upper()
                if '"' in cur_course:
                    array_course = cur_course.split('"')
                    cur_course = array_course[1].strip()
                cur_site_course = cur_site + '_' + cur_course
                date_No_track_dit[race_date][race_No] = cur_site_course
    return date_No_track_dit


def GetTrackRecord(sort_race_date_rows):
    track_record_dict = {}  # race_date & {site_course & record}
    temp_track_records = {}  # site_course & record
    date_No_track_dit = __getDateNoTrack(sort_race_date_rows)
    for race_date, No_track_dict in date_No_track_dit.items():
        if race_date not in track_record_dict.keys():
            track_record_dict[race_date] = {}
        # before
        for race_No, track in No_track_dict.items():
            if track not in temp_track_records.keys():
                temp_track_records[track] = 0
            track_record_dict[race_date][track] = temp_track_records[track]
        # after
        for race_No, track in No_track_dict.items():
            temp_track_records[track] += 1
    return track_record_dict

