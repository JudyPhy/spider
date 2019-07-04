from common import common


def GetTrackRecord(sort_race_date_rows, sort_history_raceResults_rows):
    track_record_dict = {}  # race_date & {site_course & record}
    temp_track_records = {}  # site_course & record
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in track_record_dict.keys():
            track_record_dict[race_date] = {}
        for row in rows:
            cur_site = row['site'].replace(' ', '')
            cur_course = row['course'].strip().upper()
            if '"' in cur_course:
                array_course = cur_course.split('"')
                cur_course = array_course[1].strip()
            cur_site_course = cur_site + '_' + cur_course
            if cur_site_course not in temp_track_records.keys():
                temp_track_records[cur_site_course] = 0
            # before
            track_record_dict[race_date][cur_site_course] = temp_track_records[cur_site_course]
        # after
        race_No_list = []
        for row in rows:
            race_No = row['race_No']
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            if race_date_No in sort_history_raceResults_rows.keys():
                cur_race_rows = list(sort_history_raceResults_rows[race_date_No].values())
                cur_site = cur_race_rows[0]['site'].replace(' ', '')
                cur_course = cur_race_rows[0]['course'].strip().upper()
                if '"' in cur_course:
                    array_course = cur_course.split('"')
                    cur_course = array_course[1].strip()
                cur_site_course = cur_site + '_' + cur_course
                if race_date_No not in race_No_list:
                    race_No_list.append(race_date_No)
                    temp_track_records[cur_site_course] += 1
    return track_record_dict

