from common import common

RECENT_COUNT = 6


def GetHorseRecentSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_recent_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_horse_dis_time_dict = {}  # horse_code & {race_date_No & [distance, time]}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_recent_speed_dict.keys():
            horse_recent_speed_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_dis_time_dict.keys():
                        temp_horse_dis_time_dict[horse_code] = {}
                    # before
                    array_dis_time_list = list(temp_horse_dis_time_dict[horse_code].values())
                    highest_speed = 0
                    lowest_speed = 9999
                    total_dis = 0
                    total_time = 0
                    start_index = 0
                    if len(array_dis_time_list) >= RECENT_COUNT:
                        start_index = len(array_dis_time_list) - RECENT_COUNT
                    for temp_array_dis_time in array_dis_time_list[start_index:]:
                        temp_cur_speed = temp_array_dis_time[0]/temp_array_dis_time[1]
                        if temp_cur_speed > highest_speed:
                            highest_speed = temp_cur_speed
                        if temp_cur_speed < lowest_speed:
                            lowest_speed = temp_cur_speed
                        total_dis += temp_array_dis_time[0]
                        total_time += temp_array_dis_time[1]
                    if lowest_speed == 9999:
                        lowest_speed = 0
                    ave_speed = 0
                    if total_time > 0:
                        ave_speed = total_dis / total_time
                    horse_recent_speed_dict[race_date_No][horse_code] = [highest_speed, lowest_speed, ave_speed]
                    # after
                    cur_distance = int(sort_history_raceResults_rows[race_date_No][horse_code]['distance'])
                    cur_time = common.GetTotalSeconds(sort_history_raceResults_rows[race_date_No][horse_code]['finish_time'])
                    temp_horse_dis_time_dict[horse_code][race_date_No] = [cur_distance, cur_time]
    return horse_recent_speed_dict

