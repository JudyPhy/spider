from common import common


def __getCourseStandardTimesRow(track, distance, course_standard_times_rows):
    for row in course_standard_times_rows:
        cur_track = row['track']
        cur_distance = row['distance']
        if (track == cur_track) and (distance == cur_distance):
            return row
    return None


def GetClsStandardSpeedDict(history_raceCard_rows, course_standard_times_rows):
    cls_standard_speed_dict = {}  # race_date_No & {horse_code & speed}
    for race_date_No, dict in history_raceCard_rows.items():
        for horse_code, row in dict.items():
            if race_date_No not in cls_standard_speed_dict.keys():
                cls_standard_speed_dict[race_date_No] = {}
            cur_site = row['site'].replace(' ', '')
            cur_course = row['course']
            if '"' in cur_course:
                cur_track = cur_site + 'TurfTrack'
            else:
                cur_track = cur_site + 'AllWeatherTrack'
            cur_distance = int(row['distance'])
            course_standard_times_row = __getCourseStandardTimesRow(cur_track, cur_distance, course_standard_times_rows)
            if course_standard_times_row:
                cur_cls = row['cls'].strip()
                cur_time = ''
                if 'Class' in cur_cls:
                    if '1' in cur_cls:
                        cur_time = course_standard_times_row['cls_1']
                    elif '2' in cur_cls:
                        cur_time = course_standard_times_row['cls_2']
                    elif '3' in cur_cls:
                        cur_time = course_standard_times_row['cls_3']
                    elif '4' in cur_cls:
                        cur_time = course_standard_times_row['cls_4']
                    elif '5' in cur_cls:
                        cur_time = course_standard_times_row['cls_5']
                elif 'Group' in cur_cls:
                    cur_time = course_standard_times_row['GroupRace']
                elif 'Griffin' in cur_cls:
                    cur_time = course_standard_times_row['GriffinRace']
                else:
                    cur_time = course_standard_times_row['GroupRace']   # ∆‰”‡µƒ»°GroupRace
                # to time
                if (cur_time == '') or ('-' in cur_time):
                    cls_standard_speed_dict[race_date_No][horse_code] = 0
                else:
                    cls_standard_speed_dict[race_date_No][horse_code] = cur_distance/common.GetTotalSeconds(cur_time)
    return cls_standard_speed_dict

