from common import common
from db.database import singleton_Scrub_DB
from config.myconfig import singleton_cfg

TAG = 'horse_cls_speed'


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


def __getTime(race_date_No, horse_code, results_rows):
    if (race_date_No in results_rows.keys()) and (horse_code in results_rows[race_date_No].keys()):
        finish_time = results_rows[race_date_No][horse_code]['finish_time']
        if ('-' in finish_time) and (results_rows[race_date_No][horse_code]['plc'] in common.words):
            return None
        else:
            return __getRaceSeconds(finish_time)
    return -1


def __getCls(cls_dict, race_date_No):
    if race_date_No in cls_dict.keys():
        return cls_dict[race_date_No]
    # print("class can't find", race_date_No)
    return None


# race_No_dict: race_date_id & race_No
def __getClsDict(race_No_dict):
    cls_dict = {}    # race_date_No & cls
    if singleton_Scrub_DB.table_exists(common.HORSE_RACE_TABLE):
        singleton_Scrub_DB.cursor.execute('select race_date,class,race_id from {}'.format(common.HORSE_RACE_TABLE))
        rows = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows:
            array_date = row['race_date'].split('/')
            year = array_date[2]
            if len(year) == 2:
                year = '20' + year
            race_date_id = year + array_date[1] + array_date[0] + common.toThreeDigitStr(row['race_id'])
            if race_date_id in race_No_dict.keys():
                race_date_No = year + array_date[1] + array_date[0] + common.toDoubleDigitStr(race_No_dict[race_date_id])
                if race_date_No not in cls_dict.keys():
                    cls_dict[race_date_No] = ''
                cls_dict[race_date_No] = row['class'].strip()
    return cls_dict


def __getRaceNoDict(results_rows):
    race_No_dict = {}   # race_date_id & race_No
    for race_date_No, horse_dict in results_rows.items():
        race_date = race_date_No[:len(race_date_No) - 2]
        for horse_code, row in horse_dict.items():
            race_date_id = race_date + common.toThreeDigitStr(row['race_id'])
            if race_date_id not in race_No_dict.keys():
                race_No_dict[race_date_id] = row['race_No']
            break
    return race_No_dict


no_cls_list = []
def getHorseClsSpeed(raceCard_rows, results_rows):
    race_No_dict = __getRaceNoDict(results_rows)  # race_date_id & race_No
    cls_dict = __getClsDict(race_No_dict)  # race_date_No & cls

    temp_raceCard_rows = {}  # race_date_No & [rows]
    for row in raceCard_rows:
        race_date_No = row['race_date'] + common.toDoubleDigitStr(row['race_No'])
        if race_date_No not in temp_raceCard_rows.keys():
            temp_raceCard_rows[race_date_No] = []
        temp_raceCard_rows[race_date_No].append(row)

    cls_speed_dict = {}  # race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
    temp_speed = {}  # horse_code & {cls & [highest_speed, lowest_speed, all_dis, all_time]}
    sort_date_No_list = sorted(temp_raceCard_rows.keys())
    for race_date_No in sort_date_No_list:
        if race_date_No not in cls_speed_dict.keys():
            cls_speed_dict[race_date_No] = {}
        rows = temp_raceCard_rows[race_date_No]
        for row in rows:
            horse_code = row['horse_code'].strip()
            cls = __getCls(cls_dict, race_date_No)
            race_date = row['race_date']
            if (cls == None) and (race_date == singleton_cfg.getRaceDate()):
                today_cls = row['cls'].replace('Class', '').strip()
                cls = common.__toHorseRaceClass(today_cls)

            if cls == None and (race_date + common.toDoubleDigitStr(row['race_No']) not in no_cls_list):
                no_cls_list.append(race_date + common.toDoubleDigitStr(row['race_No']))

            # 赛前
            if (horse_code in temp_speed.keys()) and (cls in temp_speed[horse_code].keys()):
                speed = temp_speed[horse_code][cls]
                cls_speed_dict[race_date_No][horse_code] = [speed[0], speed[1], speed[2]/(speed[3] + 0.00001)]
            else:
                cls_speed_dict[race_date_No][horse_code] = [0, 0, 0]

            # 赛后
            time = __getTime(race_date_No, horse_code, results_rows)
            if time == None:
                # 无效马本场次不记录
                continue
            else:
                if horse_code not in temp_speed.keys():
                    temp_speed[horse_code] = {}
                if cls not in temp_speed[horse_code].keys():
                    temp_speed[horse_code][cls] = [0, 9999, 0, 0]
                distance = int(row['distance'])
                curSpeed = distance/(time + 0.00001)
                if curSpeed > temp_speed[horse_code][cls][0]:
                    temp_speed[horse_code][cls][0] = curSpeed
                if curSpeed < temp_speed[horse_code][cls][1]:
                    temp_speed[horse_code][cls][1] = curSpeed
                temp_speed[horse_code][cls][2] += distance
                temp_speed[horse_code][cls][3] += time

            # if 'V082' == horse_code:
            #     print('\n', race_date_No, cls, distance, curSpeed)
            #     print(temp_speed[horse_code])
            #     print(cls_speed_dict[race_date_No][horse_code])
    print(TAG, no_cls_list)
    return cls_speed_dict

