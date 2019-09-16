from common import common


def __getRaceDateNoTrack(sort_race_date_rows):
    date_No_track = {}  # race_date & {race_No & site_course}
    for race_date, rows in sort_race_date_rows.items():
        if race_date not in date_No_track.keys():
            date_No_track[race_date] = {}
        for row in rows:
            race_No = row['race_No']
            if race_No not in date_No_track[race_date].keys():
                cur_site = row['site'].replace(' ', '')
                cur_course = row['course'].strip().upper()
                if '"' in cur_course:
                    array_course = cur_course.split('"')
                    cur_course = array_course[1].strip()
                cur_site_course = cur_site + '_' + cur_course
                date_No_track[race_date][race_No] = cur_site_course
    return date_No_track


def GetTrackFavRecord(sort_race_date_rows, sort_history_raceResults_rows):
    track_record_dict = {}  # race_date & {site_course & record}
    temp_track_records = {}  # site_course & record
    date_No_track_dict = __getRaceDateNoTrack(sort_race_date_rows)
    for race_date, No_track_dict in date_No_track_dict.items():
        if race_date not in track_record_dict.keys():
            track_record_dict[race_date] = {}
        for race_No, track in No_track_dict.items():
            if track not in temp_track_records.keys():
                temp_track_records[track] = 0
            # before
            if track not in track_record_dict[race_date].keys():
                track_record_dict[race_date][track] = temp_track_records[track]
            # after
            race_date_No = race_date + common.toDoubleDigitStr(race_No)
            if race_date_No in sort_history_raceResults_rows.keys():
                fav_is_before3 = False
                for horse_code, row in sort_history_raceResults_rows[race_date_No].items():
                    cur_plc = row['plc'].replace('DH', '')
                    if cur_plc not in common.words:
                        cur_odds = float(row['win_odds'])
                        isFav = common.IsLowestOdds(cur_odds, sort_history_raceResults_rows[race_date_No])
                        if isFav and (int(cur_plc) <= 3):
                            fav_is_before3 = True
                if fav_is_before3:
                    temp_track_records[track] += 1
    return track_record_dict

