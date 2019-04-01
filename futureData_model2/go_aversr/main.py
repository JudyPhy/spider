###  取比赛前的所有历史数据，计算going上所有马的平均速度 ###
from common import common
from db.database import singleton_Scrub_DB
import datetime
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


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


# 获取计算速度相关的历史数据
def __getHistoryGoingRaceData(going_list, today_date):
    going_rows = {}  # going & [row, row, ...]
    now = datetime.datetime.now()
    for year in range(2013, now.year + 1):
        tableName = RESULTS_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                'select race_date,race_id,finish_time,distance,plc,going from {}'.format(tableName))
            rows_orig = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows_orig:
                array_date = row['race_date'].split('/')
                if int(array_date[2] + array_date[1] + array_date[0]) < today_date:
                    going = row['going'].replace(' ', '').strip().upper()
                    if going == '':
                        going = 'GOOD'
                    if going in going_list:
                        if going not in going_rows.keys():
                            going_rows[going] = []
                        going_rows[going].append(row)
        else:
            common.log('go_avesr: table[' + tableName + '] not exist')
    return going_rows


def getTodayGoingAveSpeed(today_rows):
    going_list = []
    for row in today_rows:
        going = row['going'].replace(' ', '').strip().upper()
        if going == '':
            going = 'GOOD'
        if going not in going_list:
            going_list.append(going)
    print('\ntoday going type:', going_list)
    today_date = int(singleton_cfg.getRaceDate())
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
    print(going_ave_dict)
    return going_ave_dict





