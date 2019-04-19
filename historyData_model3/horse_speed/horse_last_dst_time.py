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


def __getHorseLastDstTime():
    last_dst_time_dict = {}  # race_date_No & {horse_code & last_dst_time}
    scgd_dict = {}  # race_date_No & scgd(site_course_going_distance)
    now = datetime.datetime.now()
    for year in range(2014, now.year + 1):
        tableName = common.HORSE_SECTIONAL_TIME_TABLE.replace('{0}', str(year))
        if singleton_Scrub_DB.table_exists(tableName):
            singleton_Scrub_DB.cursor.execute('select * from {}'.format(tableName))
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

                if race_date_No not in scgd_dict.keys():
                    site = row['site'].replace(' ', '')
                    course = row['course'].strip()
                    going = row['going'].replace(' ', '').upper()
                    if going == '':
                        going = 'GOOD'
                    distance = str(int(row['distance']))
                    scgd = site + '_' + course + '_' + going + '_' + distance
                    scgd_dict[race_date_No] = scgd
        else:
            print('table[', tableName, '] not exist')
    return last_dst_time_dict, scgd_dict


def __getScgd(race_date_No, scgd_dict):
    if race_date_No in scgd_dict.keys():
        return scgd_dict[race_date_No]
    else:
        return None


def getHorseLastDstTimeDicts(raceCard_rows):
    # last_dst_time_dict: race_date_No & {horse_code & last_dst_time}
    # scgd_dict: race_date_No & scgd(site_course_going_distance)
    last_dst_time_dict, scgd_dict = __getHorseLastDstTime()

    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    last_dst_time_ave_dict = {}  # race_date_No & {horse_code & last_dst_time_ave}
    prev_last_dst_time_dict = {}  # race_date_No & {horse_code & prev_last_dst_time}
    temp_time_dict = {}  # horse_code & {scgd & [last_dst_time]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in last_dst_time_ave_dict.keys():
            last_dst_time_ave_dict[race_date_No] = {}
        if race_date_No not in prev_last_dst_time_dict.keys():
            prev_last_dst_time_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            scgd = __getScgd(race_date_No, scgd_dict)

            if scgd == None:
                continue

            # 赛前
            if (horse_code in temp_time_dict.keys()) and (scgd in temp_time_dict[horse_code].keys()):
                array_time = temp_time_dict[horse_code][scgd]
                sum = 0
                for value in array_time:
                    sum += value
                last_dst_time_ave_dict[race_date_No][horse_code] = sum/len(array_time)
                prev_last_dst_time_dict[race_date_No][horse_code] = array_time[len(array_time) - 1]
            else:
                last_dst_time_ave_dict[race_date_No][horse_code] = 0
                prev_last_dst_time_dict[race_date_No][horse_code] = 0

            # 赛后
            if horse_code not in temp_time_dict.keys():
                temp_time_dict[horse_code] = {}
            if scgd not in temp_time_dict[horse_code].keys():
                temp_time_dict[horse_code][scgd] = []
            if (race_date_No in last_dst_time_dict.keys()) and (horse_code in last_dst_time_dict[race_date_No].keys()):
                last_time = last_dst_time_dict[race_date_No][horse_code]
                temp_time_dict[horse_code][scgd].append(last_time)

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, scgd)
            #     print(temp_time_dict[horse_code])
            #     print(prev_last_dst_time_dict[race_date_No][horse_code])
            #     print(last_dst_time_ave_dict[race_date_No][horse_code])

    return last_dst_time_ave_dict, prev_last_dst_time_dict

