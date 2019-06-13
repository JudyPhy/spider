from common import common


def GetHorseDstSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows):
    horse_dst_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_horse_dst_speed = {}  # horse_code & {distance & [highest_speed, lowest_speed, all_dis, all_time]}
    for race_date_No, dict in sort_history_raceCard_rows.items():
        if race_date_No not in horse_dst_speed_dict.keys():
            horse_dst_speed_dict[race_date_No] = {}
        for horse_code, row in dict.items():
            if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
                cur_plc = sort_history_raceResults_rows[race_date_No][horse_code]['plc'].replace('DH', '')
                cur_distance = int(sort_history_raceResults_rows[race_date_No][horse_code]['distance'])
                if cur_plc not in common.words:
                    if horse_code not in temp_horse_dst_speed.keys():
                        temp_horse_dst_speed[horse_code] = {}
                    if cur_distance not in temp_horse_dst_speed[horse_code].keys():
                        temp_horse_dst_speed[horse_code][cur_distance] = [0, 9999, 0, 0]
                    # before
                    cur_speeds = temp_horse_dst_speed[horse_code][cur_distance]
                    cur_lowest_speed = cur_speeds[1]
                    if cur_lowest_speed == 9999:
                        cur_lowest_speed = 0
                    ave_speed = 0
                    if cur_speeds[3] > 0:
                        ave_speed = cur_speeds[2]/cur_speeds[3]
                    horse_dst_speed_dict[race_date_No][horse_code] = [cur_speeds[0], cur_lowest_speed, ave_speed]
                    # after
                    cur_seconds = common.GetTotalSeconds(sort_history_raceResults_rows[race_date_No][horse_code]['finish_time'])
                    cur_speed = cur_distance/cur_seconds
                    temp_horse_dst_speed[horse_code][cur_distance][2] += cur_distance
                    temp_horse_dst_speed[horse_code][cur_distance][3] += cur_seconds
                    if cur_speed > temp_horse_dst_speed[horse_code][cur_distance][0]:
                        temp_horse_dst_speed[horse_code][cur_distance][0] = cur_speed
                    if cur_speed < temp_horse_dst_speed[horse_code][cur_distance][1]:
                        temp_horse_dst_speed[horse_code][cur_distance][1] = cur_speed
    return horse_dst_speed_dict

