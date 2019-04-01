###  计算马匹年龄  ###
from db.database import singleton_Scrub_DB
from common import common


# 获取马匹开始参赛的时间
def __calculateRaceBeginDate(rows):
    race_begin_date_dict = {}  # horse_code & begin_date
    for row in rows:
        code = row['horse_code'].strip()
        if code not in race_begin_date_dict.keys():
            race_begin_date_dict[code] = row['race_date']
        else:
            if row['race_date'] < race_begin_date_dict[code]:
                race_begin_date_dict[code] = row['race_date']
    return race_begin_date_dict


# 获取赛前马匹信息中的马匹年龄，应全都有年龄
def __getHorseAgeBeforeRace():
    future_horse_age_dict = {}  # horse_code & {race_date & age}
    future_no_age_horse = []
    error_str = ''
    tableList_future = common.getFutureHorseTableList()
    for table in tableList_future:
        if singleton_Scrub_DB.table_exists(table):
            singleton_Scrub_DB.cursor.execute('select race_date,code,age from {}'.format(table))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                race_date = row['race_date']
                code = row['code']
                age = row['age']
                if age > 0:
                    if code not in future_horse_age_dict.keys():
                        future_horse_age_dict[code] = {}
                    future_horse_age_dict[code][race_date] = age
                else:
                    if code not in future_no_age_horse:
                        error_str += code + ','
                        future_no_age_horse.append(code)
        else:
            print('horse_age: table[' + table + '] not exist')
    print('horse[' + error_str + '] in future horse table have no age.')
    return future_horse_age_dict


# 获取马匹出生年（只包含有年龄的马匹）
def __getHorseBornYearDict(future_horse_age_dict):
    dict_bornYear = {}  # horse_code & bornYear
    for horse_code, ageDict in future_horse_age_dict.items():
        if horse_code not in dict_bornYear.keys():
            for str_date, age in ageDict.items():
                update_year = int(str_date[:len(str_date) - 4])
                born_year = update_year - age
                dict_bornYear[horse_code] = born_year
                break
    print('future horse age count:', len(dict_bornYear))
    # 遍历历史马匹信息，包含大量退役马匹，无法全都获取到年龄
    tableList_history = common.getHistoryHorseTableList()
    for table in tableList_history:
        if singleton_Scrub_DB.table_exists(table):
            array_tableName = table.split('_')
            update_date = array_tableName[len(array_tableName) - 1]
            update_year = int(update_date[:4])
            singleton_Scrub_DB.cursor.execute('select code,age from {}'.format(table))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                code = row['code']
                age = row['age']
                if (code not in dict_bornYear.keys()) and (age > 0):
                    dict_bornYear[code] = update_year - age
    print('all horse age count:', len(dict_bornYear))
    return dict_bornYear


def __getHorseBornYear(horse_code, dict_bornYear, race_begin_date_dict):
    if horse_code in dict_bornYear.keys():
        return dict_bornYear[horse_code]
    else:
        # 没有找到年龄的马，将首次参赛当作三岁
        race_begin_date = str(race_begin_date_dict[horse_code])
        race_begin_year = int(race_begin_date[:len(race_begin_date) - 4])
        return race_begin_year - 3


def __calculateHorseAgeByRace(race_rows, future_horse_age_dict, dict_bornYear, race_begin_date_dict):
    results_dict = {}   # new_race_id & {horse_code & age}
    for row in race_rows:
        race_date = row['race_date']
        new_race_id = int(str(race_date) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in results_dict.keys():
            results_dict[new_race_id] = {}
        code = row['horse_code']
        str_raceDate = str(race_date)
        if (code in future_horse_age_dict.keys()) and (str_raceDate in future_horse_age_dict[code].keys()):
            results_dict[new_race_id][code] = future_horse_age_dict[code][str_raceDate]
        else:
            curYear = int(str_raceDate[:len(str_raceDate) - 4])
            curAge = curYear - __getHorseBornYear(code, dict_bornYear, race_begin_date_dict)
            results_dict[new_race_id][code] = curAge
    return results_dict


def getHorseAgeDict(history_rows):
    future_horse_age_dict = __getHorseAgeBeforeRace() # horse_code & {race_date & age}
    dict_bornYear = __getHorseBornYearDict(future_horse_age_dict)  # horse_code & bornYear
    race_begin_date_dict = __calculateRaceBeginDate(history_rows)  # horse_code & begin_date
    dict_race_age = __calculateHorseAgeByRace(history_rows, future_horse_age_dict, dict_bornYear, race_begin_date_dict)  # new_race_id & {horse_code & age}
    return dict_race_age

