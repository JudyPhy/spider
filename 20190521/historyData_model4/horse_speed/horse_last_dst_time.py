from common import common


def __getLastDstTime(row):
    time_list = []
    for n in range(1, 7):
        key = 'sec{0}_time'.replace('{0}', str(n))
        if row[key] != '':
            time_list.append(row[key])
    if len(time_list) == 0:
        return 0
    else:
        cur_time = time_list[len(time_list) - 1]
        return common.GetTotalSeconds(cur_time)


def GetHorseLastDstTimePrev(sort_history_raceCard_rows, sort_history_raceResults_rows, display_sectional_time_rows):
    last_dst_time_dict = {}  # race_date_No & {horse_code & [prev, ave, min]}
    temp_last_dst_time_dict = {}  # horse_code_site_course_going_distance & {race_date_No & last_dst_time}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in last_dst_time_dict.keys():
            last_dst_time_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    cur_site = sort_history_raceResults_rows[race_date_No][horse_code]['site'].replace(' ', '')
                    cur_course = sort_history_raceResults_rows[race_date_No][horse_code]['course'].strip()
                    if '"' in cur_course:
                        array_course = cur_course.split('"')
                        cur_course = array_course[1].strip()
                    cur_going = sort_history_raceResults_rows[race_date_No][horse_code]['going'].replace(' ', '').upper()
                    if cur_going == '':
                        cur_going = 'GOOD'
                    cur_distance = int(sort_history_raceResults_rows[race_date_No][horse_code]['distance'])
                    cscgd = horse_code + '_' + cur_site + '_' + cur_course + '_' + cur_going + '_' + str(cur_distance)
                    if cscgd not in temp_last_dst_time_dict.keys():
                        temp_last_dst_time_dict[cscgd] = {}
                    # before
                    prev = 0
                    min = 9999
                    total_time = 0
                    for last_dst_time in temp_last_dst_time_dict[cscgd].values():
                        total_time += last_dst_time
                        prev = last_dst_time
                        if last_dst_time < min:
                            min = last_dst_time
                    count = len(temp_last_dst_time_dict[cscgd].values())
                    if count == 0:
                        ave = 0
                    else:
                        ave = total_time/count
                    if min == 9999:
                        min = 0
                    last_dst_time_dict[race_date_No][horse_code] = [prev, ave, min]
                    # after
                    cur_last_dst_time = __getLastDstTime(display_sectional_time_rows[race_date_No][horse_code])
                    temp_last_dst_time_dict[cscgd][race_date_No] = cur_last_dst_time
    return last_dst_time_dict


