from db.db import singleton_ScrubDb
from common import common
from config.myconfig import singleton_cfg

RESULTS_TABLE = 'f_race_results_{0}'


def __getFromTime(from_date):
    year = int(from_date[: len(from_date) - 4])
    month = int(from_date[len(from_date) - 4: len(from_date) - 2])
    day = int(from_date[len(from_date) - 2:])
    if year != 0:
        if month != 0:
            if day != 0:
                return year, month, day
            else:
                return year, month, 1
        else:
            if day != 0:
                return year, 1, day
            else:
                return year, 1, 1
    else:
        return None, None, None


def __getToTime(to_date):
    year = int(to_date[: len(to_date) - 4])
    month = int(to_date[len(to_date) - 4: len(to_date) - 2])
    day = int(to_date[len(to_date) - 2:])
    if year != 0:
        if month != 0:
            if day != 0:
                return year, month, day
            else:
                return year, month, 31
        else:
            if day != 0:
                return year, 12, day
            else:
                return year, 12, 31
    else:
        return None, None, None


def __getRaceNum(race_date):
    race_Num = 0
    year = race_date[: len(race_date) - 4]
    tableName = RESULTS_TABLE.replace('{0}', year)
    if singleton_ScrubDb.table_exists(tableName):
        race_data_results = race_date[len(race_date) - 2:] + '/' + race_date[len(race_date) - 4: len(race_date) - 2] + '/' + year
        singleton_ScrubDb.cursor.execute('select race_No from {} where race_date=%s'.format(tableName), race_data_results)
        rows = singleton_ScrubDb.cursor.fetchall()
        for row in rows:
            if row['race_No'] > race_Num:
                race_Num = row['race_No']
    else:
        print('table[', tableName, '] not exist')
    return race_Num


def __getLoadedRace(race_date):
    race_No_list = []
    year = race_date[: len(race_date) - 4]
    tableName = singleton_cfg.getTargetTable().replace('{0}', year)
    if singleton_ScrubDb.table_exists(tableName):
        singleton_ScrubDb.cursor.execute('select race_No from {} where race_date=%s'.format(tableName), race_date)
        rows = singleton_ScrubDb.cursor.fetchall()
        for row in rows:
            race_No = row['race_No']
            if race_No not in race_No_list:
                race_No_list.append(race_No)
    else:
        print('table[', tableName, '] not exist')
    return race_No_list


def getUrlParamsDict():
    from_date = singleton_cfg.getFromDate()
    to_date = singleton_cfg.getToDate()
    year_from, month_from, day_from = __getFromTime(from_date)
    year_to, month_to, day_to = __getToTime(to_date)
    race_date_No = {}   # race_date & raceNum
    loaded_race_date_No = {}  # race_date & [race_No]
    for year in range(year_from, year_to + 1):
        for month in range(month_from, month_to + 1):
            for day in range(day_from, day_to + 1):
                race_date = str(year) + common.toDoubleDigitStr(month) + common.toDoubleDigitStr(day)
                raceNum = __getRaceNum(race_date)
                if raceNum == 0:
                    continue
                if race_date not in race_date_No.keys():
                    race_date_No[race_date] = raceNum
                else:
                    print('race date repeat')

                # loaded
                loaded_race_No_list = __getLoadedRace(race_date)
                if race_date not in loaded_race_date_No.keys():
                    loaded_race_date_No[race_date] = loaded_race_No_list
                else:
                    print('race date repeat')
    allCount = 0
    for race_date, count in race_date_No.items():
        allCount += count
    print('all url count=', allCount)

    loadedCount = 0
    for race_date, NoList in loaded_race_date_No.items():
        loadedCount += len(NoList)
    print('loaded url count=', loadedCount)

    need_spider_race_date_No = {}   # race_date & [race_No]
    for race_date, raceNum in race_date_No.items():
        for page in range(1, raceNum + 1):
            if (race_date in loaded_race_date_No.keys()) and (page in loaded_race_date_No[race_date]):
                continue
            else:
                if race_date not in need_spider_race_date_No.keys():
                    need_spider_race_date_No[race_date] = []
                need_spider_race_date_No[race_date] .append(page)
    needSpiderCount = 0
    for race_date, NoList in need_spider_race_date_No.items():
        needSpiderCount += len(NoList)
    print('need spider url count=', needSpiderCount)
    return need_spider_race_date_No

