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
    return last_dst_time_dict


def __getGoing(race_date_No, horse_code, going_dict):
    if (race_date_No in going_dict.keys()) and (horse_code in going_dict[race_date_No].keys()):
        return going_dict[race_date_No][horse_code]
    return ''


def __getPlc(race_date_No, horse_code, plc_dict):
    if (race_date_No in plc_dict.keys()) and (horse_code in plc_dict[race_date_No].keys()):
        return plc_dict[race_date_No][horse_code]
    return ''


def getHorseLastDstTimePrev(raceCard_rows, going_dict, plc_dict):
    last_dst_time_dict = __getHorseLastDstTime()  # race_date_No & {horse_code & last_dst_time}

    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    # log = []
    last_dst_time_prev_dict = {}  # race_date_No & {horse_code & last_dst_time_prev}
    last_dst_time_ave_dict = {}  # race_date_No & {horse_code & last_dst_time_ave}
    last_dst_time_min_dict = {} # race_date_No & {horse_code & last_dst_time_min}
    temp_last_dst_time_dict = {}   # horse_code_site_course_going_distance & [last_dst_time(按时间先后排序)]
    sorted_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sorted_date_No_list:
        if race_date_No not in last_dst_time_prev_dict.keys():
            last_dst_time_prev_dict[race_date_No] = {}
        if race_date_No not in last_dst_time_ave_dict.keys():
            last_dst_time_ave_dict[race_date_No] = {}
        if race_date_No not in last_dst_time_min_dict.keys():
            last_dst_time_min_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            site = row['site'].replace(' ', '')
            course = row['course'].strip()
            going = __getGoing(race_date_No, horse_code, going_dict)
            distance = int(row['distance'])
            horse_code_site_course_going_distance = horse_code + '_' + site + '_' + course + '_' + going + '_' + str(distance)

            # 赛前
            if horse_code_site_course_going_distance in temp_last_dst_time_dict.keys():
                array = temp_last_dst_time_dict[horse_code_site_course_going_distance]
                # prev
                last_dst_time_prev_dict[race_date_No][horse_code] = array[len(array) - 1]
                # ave
                sum = 0
                for value in array:
                    sum += value
                last_dst_time_ave_dict[race_date_No][horse_code] = sum/len(array)
                # min
                minTime = array[0]
                for value in array:
                    if value < minTime:
                        minTime = value
                last_dst_time_min_dict[race_date_No][horse_code] = minTime
            else:
                last_dst_time_prev_dict[race_date_No][horse_code] = 0
                last_dst_time_ave_dict[race_date_No][horse_code] = 0
                last_dst_time_min_dict[race_date_No][horse_code] = 0

            # 赛后
            plc = __getPlc(race_date_No, horse_code, plc_dict)
            if plc not in common.words:
                if horse_code_site_course_going_distance not in temp_last_dst_time_dict.keys():
                    temp_last_dst_time_dict[horse_code_site_course_going_distance] = []
                if (race_date_No in last_dst_time_dict.keys()) and (horse_code in last_dst_time_dict[race_date_No].keys()):
                    temp_last_dst_time_dict[horse_code_site_course_going_distance].append(last_dst_time_dict[race_date_No][horse_code])
                else:
                    print(race_date_No, ' horse[', horse_code, '] has no last_dst_time')
            else:
                # 无效马不记录
                pass

            # if 'A270' == horse_code:
            # # if race_date_No == '2019050508' and row['horse_No'] == 11:
            #     # if horse_code_site_course_going_distance not in log:
            #     #     log.append(horse_code_site_course_going_distance)
            #     print('\n', race_date_No, horse_code_site_course_going_distance)
            #     print(temp_last_dst_time_dict[horse_code_site_course_going_distance])
            #     print(last_dst_time_prev_dict[race_date_No][horse_code])
    # print(log)
    return last_dst_time_prev_dict, last_dst_time_ave_dict, last_dst_time_min_dict


