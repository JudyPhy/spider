### 计算每场比赛的马匹数量，并导出 ###

from db.db import singleton_ScrubDB
from common import common
import csv

RESULTS_BASE_TABLE = 'f_race_results_year'

EXPORT_FILENAME = 'each_race_horse_count.csv'

def getRaceHorseCountByDate(year, month, day):
    dict = {}   # race_id & count
    tableName = RESULTS_BASE_TABLE.replace('year', str(year))
    if singleton_ScrubDB.table_exists(tableName):
        try:
            race_date = common.toDoubleDigitStr(day) + '/' + common.toDoubleDigitStr(month) + '/' + str(year)
            singleton_ScrubDB.cursor.execute("select race_id from {} where race_date=%s".format(tableName), race_date)
            list = singleton_ScrubDB.cursor.fetchall()
            singleton_ScrubDB.connect.commit()

            for row in list:
                key = row['race_id']
                if key in dict.keys():
                    dict[key] += 1
                else:
                    dict[key] = 1
        except Exception as error:
            common.log('[check_each_race_count]getRaceHorseCountByDate error:' + str(error))
    else:
        common.log('[check_each_race_count]table[' + tableName + ' not exist')
    return dict


def export(dict, year, month, day):
    race_date = str(year) + '/' + str(month) + '/' + str(day)
    file = open(EXPORT_FILENAME, 'a+', newline='')
    writer = csv.writer(file)
    for key, value in dict.items():
        writer.writerow([race_date, key, value])
    file.close()


def exportEachRaceHorseCount():
    for year in range(2018, 2019):
        for month in range(1,13):
            for day in range(1, 32):
                dict = getRaceHorseCountByDate(year, month, day)
                # 按race_id排序
                key_sorted_list = sorted(dict.keys())
                newDict = {}
                for key in key_sorted_list:
                    newDict[key] = dict[key]
                export(newDict, year, month, day)


if __name__ == '__main__':
    exportEachRaceHorseCount()


