###     赛前going上所有马的平均速度，以天为单位统计     ###
from common import common


def __getRaceSeconds(time_text):
    seconds = 0
    array_time = []
    array1 = time_text.split('.')
    for item1 in array1:
        array2 = item1.split(':')
        for item2 in array2:
            array_time.append(item2)
    if len(array_time) == 3:
        seconds = int(array_time[0]) * 60 + int(array_time[1]) + int(array_time[2]) / 100
    elif len(array_time) == 2:
        seconds = int(array_time[0]) + int(array_time[1]) / 100
    elif len(array_time) == 1:
        seconds = int(array_time[0]) / 100
    return seconds


def getGoingAveSpeed(history_rows):
    # 按比赛日期排序
    race_rows = {}  # race_date & [row, row, ...]
    for row in history_rows:
        race_date = row['race_date']
        if race_date not in race_rows.keys():
            race_rows[race_date] = []
        race_rows[race_date].append(row)
    race_date_sorted_list = sorted(race_rows.keys())
    # 计算going上的平均速度
    going_date_dict = {}   # going & [all_distance, all_time]
    going_speed_dict = {}  # new_race_id & go_speed
    for race_date in race_date_sorted_list:
        curDayRaceRows = race_rows[race_date]
        curDayGoing = {}    # going & [all_distance, all_time]
        for row in curDayRaceRows:
            race_id = int(str(race_date) + common.toThreeDigitStr(row['race_id']))
            going = row['going'].replace(' ', '').strip().upper()
            if going == '':
                going = 'GOOD'

            # 赛前
            if going in going_date_dict.keys():
                if going_date_dict[going][1] == 0:
                    going_speed_dict[race_id] = 0
                else:
                    going_speed_dict[race_id] = going_date_dict[going][0] / going_date_dict[going][1]
            else:
                going_speed_dict[race_id] = 0

            # 赛后统计当日数据
            if going not in curDayGoing.keys():
                curDayGoing[going] = [0, 0]
            if row['plc'] not in common.words:
                curDayGoing[going][0] += int(row['distance'])
                curDayGoing[going][1] += __getRaceSeconds(row['finish_time'])
        # 将当日数据累加到总数据中
        for going, array in curDayGoing.items():
            if going not in going_date_dict.keys():
                going_date_dict[going] = [0, 0]
            all_dis = going_date_dict[going][0] + array[0]
            all_time = going_date_dict[going][1] + array[1]
            going_date_dict[going] = [all_dis, all_time]

    print('\ngo_aversr over:', going_date_dict.keys())
    return going_speed_dict





