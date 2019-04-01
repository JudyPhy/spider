from common import common
from db.database import singleton_Scrub_DB
import datetime


def __parseTime(time_text):
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


def __getLastDstTime(row):
    time_list = []
    for n in range(1, 7):
        key = 'sec{0}_time'.replace('{0}', str(n))
        if row[key] != '':
            time_list.append(row[key])
    if len(time_list) == 0:
        if row['finishing_order'] in common.words:
            return '0'
        else:
            return None
    else:
        return time_list[len(time_list) - 1]


def getHorseLastDstTime():
    last_dst_time_dict = {}  # race_date_No & {horse_code & last_dst_time}
    now = datetime.datetime.now()
    for year in range(2014, now.year + 1):
        tableName = common.HORSE_SECTIONAL_TIME_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute(
                '''select finishing_order,race_date,race_No,horse_No,horse_code,sec1_time,sec2_time,sec3_time,sec4_time,sec5_time,sec6_time from {}'''.format(tableName))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                array_date = row['race_date'].split('/')
                race_date_No = array_date[2] + array_date[1] + array_date[0] + common.toDoubleDigitStr(row['race_No'])
                if race_date_No not in last_dst_time_dict.keys():
                    last_dst_time_dict[race_date_No] = {}
                horse_code = row['horse_code'].strip()
                last_time = __getLastDstTime(row)
                if last_time == None:
                    print('last_time none:', row)
                else:
                    last_dst_time_dict[race_date_No][horse_code] = __parseTime(__getLastDstTime(row))
    return last_dst_time_dict

