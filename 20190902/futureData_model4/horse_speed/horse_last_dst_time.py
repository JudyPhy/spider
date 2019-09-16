from common import common


def __getLastDstTotalSeconds(race_date_No, horse_code, display_sectional_time_rows):
    if (race_date_No in display_sectional_time_rows.keys()) and (horse_code in display_sectional_time_rows[race_date_No].keys()):
        row = display_sectional_time_rows[race_date_No][horse_code]
        time_list = []
        for n in range(1, 7):
            key = 'sec{0}_time'.replace('{0}', str(n))
            if row[key] != '':
                time_list.append(row[key])
        if len(time_list) > 0:
            return common.GetTotalSeconds(time_list[len(time_list) - 1])
    return 0


def __getLastDstTimeArray(horse_code, site, course, going, distance, history_raceResults_rows, display_sectional_time_rows):
    total_time = 0
    count = 0
    prev_time = 0
    min_time = 9999
    ave_time = 0
    for race_date_No, dict in history_raceResults_rows.items():
        if horse_code in dict.keys():
            plc = dict[horse_code]['plc'].replace('DH', '')
            cur_site = dict[horse_code]['site'].replace(' ', '')
            cur_course = dict[horse_code]['course'].strip().upper()
            if '"' in cur_course:
                array_course = cur_course.split('"')
                cur_course = array_course[1].strip()
            cur_going = dict[horse_code]['going'].replace(' ', '').upper()
            if cur_going == '':
                cur_going = 'GOOD'
            cur_distance = int(dict[horse_code]['distance'])
            cur_last_dst_time = __getLastDstTotalSeconds(race_date_No, horse_code, display_sectional_time_rows)
            if (plc not in common.words) and (cur_site == site) and (cur_course == course) and (cur_going == going) \
                    and (cur_distance == distance) and (cur_last_dst_time > 0):
                prev_time = cur_last_dst_time
                if cur_last_dst_time < min_time:
                    min_time = cur_last_dst_time
                total_time += cur_last_dst_time
                count += 1
    if count > 0:
        ave_time = total_time/count
    if min_time == 9999:
        min_time = 0
    return [prev_time, ave_time, min_time]


def __getGoing(race_date_No, going_dict):
    if race_date_No in going_dict.keys():
        return going_dict[race_date_No]
    print(race_date_No, "can't find going in going_dict")
    return ''


def GetHorseLastDstTime(future_raceCard_rows, history_raceResults_rows, display_sectional_time_rows, going_dict):
    horse_last_dst_time_dict = {}   # race_date_No & {horse_No & [prev, ave, min]}
    for race_date_No, dict in future_raceCard_rows.items():
        if race_date_No not in horse_last_dst_time_dict.keys():
            horse_last_dst_time_dict[race_date_No] = {}
        for horse_No, row in dict.items():
            horse_code = row['horse_code'].strip()
            site = row['site'].replace(' ', '')
            course = row['course'].strip().upper()
            if '"' in course:
                array_course = course.split('"')
                course = array_course[1].strip()
            going = __getGoing(race_date_No, going_dict)
            distance = int(row['distance'])
            horse_last_dst_time_dict[race_date_No][horse_No] = __getLastDstTimeArray(horse_code, site, course, going, distance,
                                                                                     history_raceResults_rows, display_sectional_time_rows)
    return horse_last_dst_time_dict


