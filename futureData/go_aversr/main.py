###  取比赛前的所有历史数据，计算going上所有马的平均速度 ###
from config.myconfig import singleton_cfg
from common import common
from db.database import singleton_Results_DB

HISTORY_RESULTS_FROM_TABLE = singleton_cfg.getHistoryRaceTable()


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


# 获取计算速度相关的历史数据
def __getHistoryGoingRaceData(going_list, today_date):
    going_rows = {}  # going & [row, row, ...]
    if singleton_Results_DB.table_exists(HISTORY_RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute(
            'select race_date,race_id,finish_time,distance,plc,going from {} where race_date<%s'.format(HISTORY_RESULTS_FROM_TABLE), today_date)
        rows_orig = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in rows_orig:
            going = row['going'].strip().upper()
            if going == '':
                going = 'GOOD'
            if going in going_list:
                if going not in going_rows.keys():
                    going_rows[going] = []
                going_rows[going].append(row)
    else:
        common.log('go_avesr: table[' + HISTORY_RESULTS_FROM_TABLE + '] not exist')
    return going_rows


def getTodayGoingAveSpeed(today_rows):
    going_list = []
    for row in today_rows:
        going = row['going'].replace(' ', '').strip().upper()
        if going == '':
            going = 'GOOD'
        if going not in going_list:
            going_list.append(going)
    today_date = today_rows[0]['race_date']
    going_rows = __getHistoryGoingRaceData(going_list, today_date)

    going_ave_dict = {}   # going & avesr
    for going, rows in going_rows.items():
        if going not in going_ave_dict.keys():
            going_ave_dict[going] = 0

        all_time = 0
        all_dis = 0
        for row in rows:
            if row['plc'] not in common.words:
                all_dis += int(row['distance'])
                all_time += __getRaceSeconds(row['finish_time'])
        if all_time != 0:
            going_ave_dict[going] = all_dis / all_time
    return going_ave_dict





