### 计算每场比赛的马匹数量，并导出 ###

from db.db import singleton_ScrubDB
from common import common

SECTIONAL_TIME_TABLE = 'g_display_sectional_time_year'


def getSectionalTimeCountByDate(year, month, day):
    tableName = SECTIONAL_TIME_TABLE.replace('year', str(year))
    if singleton_ScrubDB.table_exists(tableName):
        race_date = common.toDoubleDigitStr(day) + '/' + common.toDoubleDigitStr(month) + '/' + str(year)
        singleton_ScrubDB.cursor.execute("select id from {} where race_date=%s".format(tableName), race_date)
        rows = singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
        return len(rows)
    else:
        common.log('[check_each_month_count]table[' + tableName + '] not exist')
        return 0


def eachMonthCount():
    dict = {}  # year & {month & count}
    for year in range(2014, 2015):
        for month in range(1,13):
            for day in range(1, 32):
                count = getSectionalTimeCountByDate(year, month, day)
                # print(year, month, day, count)
                if year not in dict.keys():
                    dict[year] = {}
                if month not in dict[year].keys():
                    dict[year][month] = 0
                dict[year][month] += count

    for year, item in dict.items():
        print(year, '=>', item)


if __name__ == '__main__':
    eachMonthCount()


