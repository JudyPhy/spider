###     赛前distance上所有马的平均速度，以天为单位统计     ###
from common import common


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


def getDistanceAveSpeed(history_rows):
    # 按比赛日期排序
    race_rows = {} # race_date & [row, row, ...]
    for row in history_rows:
        race_date = row['race_date']
        if race_date not in race_rows.keys():
            race_rows[race_date] = []
        race_rows[race_date].append(row)
    race_date_sorted_list = sorted(race_rows.keys())

    # 计算distance下的平均速度
    dis_date_dict = {} # distance & [all_distance, all_time]
    dis_speed_dict = {}  # new_race_id & ave_speed
    for race_date in race_date_sorted_list:
        curDayRaceRows = race_rows[race_date]
        curDayDis = {}  # distance & [all_distance, all_time]
        for row in curDayRaceRows:
            race_id = int(str(race_date) + common.toThreeDigitStr(row['race_id']))
            distance = int(row['distance'])

            # 赛前
            if distance in dis_date_dict.keys():
                if dis_date_dict[distance][1] == 0:
                    dis_speed_dict[race_id] = 0
                else:
                    dis_speed_dict[race_id] = dis_date_dict[distance][0] / dis_date_dict[distance][1]
            else:
                dis_speed_dict[race_id] = 0

            # 赛后统计当日数据
            if distance not in curDayDis.keys():
                curDayDis[distance] = [0, 0]
            if row['plc'] not in common.words:
                curDayDis[distance][0] += int(row['distance'])
                curDayDis[distance][1] += __getRaceSeconds(row['finish_time'])
        # 将当日数据累加到总数据中
        for dis, array in curDayDis.items():
            if dis not in dis_date_dict.keys():
                dis_date_dict[dis] = [0, 0]
            all_dis = dis_date_dict[dis][0] + array[0]
            all_time = dis_date_dict[dis][1] + array[1]
            dis_date_dict[dis] = [all_dis, all_time]

    print('\ndis_aversr over:', dis_date_dict.keys())
    return dis_speed_dict





