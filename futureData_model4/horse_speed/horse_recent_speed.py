from common import common

RECENT_COUNT = 6


def __getRaceSeconds(time_text):
    seconds = 0
    array_time = time_text.split('.')
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds


def __getTime(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        finish_time = results_rows[race_date_No][horse_code]['finish_time']
        if ('-' in finish_time) and (results_rows[race_date_No][horse_code]['plc'] in common.words):
            return None
        else:
            return __getRaceSeconds(finish_time)
    return -1


def __getRecentSpeed(horse_code, race_date_No, horse_dis_time_dict):
    if horse_code in horse_dis_time_dict.keys():
        sort_date_No_list = sorted(horse_dis_time_dict[horse_code].keys())
        sort_date_No_list.reverse()
        flag = False
        count = 0
        speed = [0, 9999, 0]
        all_dis = 0
        all_time = 0
        for sub_race_date_No in sort_date_No_list:
            if sub_race_date_No == race_date_No:
                flag = True
            elif flag:
                dis_time = horse_dis_time_dict[horse_code][sub_race_date_No]
                if dis_time[1] == None:
                    # 无效马匹本场不统计
                    continue
                else:
                    curSpeed = dis_time[0]/(dis_time[1] + 0.00001)
                    if curSpeed > speed[0]:
                        # highest_speed
                        speed[0] = curSpeed
                    if curSpeed < speed[1]:
                        # lowest_speed
                        speed[1] = curSpeed
                    all_dis += dis_time[0]
                    all_time += dis_time[1]
                    count += 1
                    if count >= RECENT_COUNT:
                        flag = False
                        break
        speed[2] = all_dis/(all_time + 0.00001)
        return speed
    else:
        return [0, 0, 0]


def getHorseRecentSpeed(raceCard_rows, results_rows):
    horse_dis_time_dict = {}  # horse_code & {race_date_No & [distance, time]}
    for row in raceCard_rows:
        horse_code = row['horse_code'].strip()
        if horse_code not in horse_dis_time_dict.keys():
            horse_dis_time_dict[horse_code] = {}
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        time = __getTime(race_date_No, horse_code, results_rows)
        horse_dis_time_dict[horse_code][race_date_No] = [int(row['distance']), time]

    recent_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in recent_speed_dict.keys():
            recent_speed_dict[race_date_No] = {}
        horse_code = row['horse_code'].strip()
        recent_speed_dict[race_date_No][horse_code] = __getRecentSpeed(horse_code, race_date_No, horse_dis_time_dict)

        # if 'V082' == horse_code:
        #     print('\n', race_date_No)
        #     print(horse_dis_time_dict[horse_code])
        #     print(recent_speed_dict[race_date_No][horse_code])
    return recent_speed_dict

