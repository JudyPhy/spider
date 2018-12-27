###  计算马匹年龄  ###
from db.database import singleton_Scrub_DB
from common import common
from config.myconfig import singleton_cfg

FROM_TABLE_LIST = singleton_cfg.getCombineHorseSourceTableList()


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


# 获取马匹出生年（只包含有年龄的马匹）
def __getHorseBornYearDict():
    dict_bornYear = {}  # horse_code & bornYear
    for table in FROM_TABLE_LIST:
        if singleton_Scrub_DB.table_exists(table):
            array_tableName = table.split('_')
            update_date = array_tableName[len(array_tableName) - 1]
            update_year = int(update_date[:4])
            singleton_Scrub_DB.cursor.execute('select code,age,retired from {}'.format(table))
            rows = singleton_Scrub_DB.cursor.fetchall()
            singleton_Scrub_DB.connect.commit()
            for row in rows:
                if row['retired'] == 0:
                    code = row['code']
                    age = row['age']
                    if (code not in dict_bornYear.keys()) and (age > 0):
                        dict_bornYear[code] = update_year - age
    common.log('horse age: has born year horse count=' + str(len(dict_bornYear)))
    return dict_bornYear


def __getHorseBornYear(horse_code, dict_bornYear, race_begin_date_dict):
    if horse_code in dict_bornYear.keys():
        return dict_bornYear[horse_code]
    else:
        # 没有找到年龄的马，将首次参赛当作三岁
        race_begin_date = str(race_begin_date_dict[horse_code])
        race_begin_year = int(race_begin_date[:len(race_begin_date) - 4])
        return race_begin_year - 3


def __calculateHorseAgeByRace(race_rows, dict_bornYear, race_begin_date_dict):
    results_dict = {}   # new_race_id & {horse_code & age}
    for row in race_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in results_dict.keys():
            results_dict[new_race_id] = {}
        code = row['horse_code']
        str_raceDate = str(row['race_date'])
        curYear = int(str_raceDate[:len(str_raceDate) - 4])
        curAge = curYear - __getHorseBornYear(code, dict_bornYear, race_begin_date_dict)
        results_dict[new_race_id][code] = curAge
    return results_dict


def getHorseAgeDict(history_rows):
    dict_bornYear = __getHorseBornYearDict()  # horse_code & bornYear
    race_begin_date_dict = __calculateRaceBeginDate(history_rows)  # horse_code & begin_date
    dict_race_age = __calculateHorseAgeByRace(history_rows, dict_bornYear, race_begin_date_dict)  # new_race_id & {horse_code & age}
    return dict_race_age

