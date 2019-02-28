### 计算每年/全部马匹数量，并与已爬取到的马匹数量进行对比，导出遗漏马匹代号 ###

from db.db import singleton_ScrubDB
from common import common
import csv

base_results_table = 'f_race_results_year'

horse_table_list = ['a_all_horse_info_20181119', 'a_all_horse_info_20181113']

FILENAME_LOST_HORSE_CODE = 'lost_horse_code.csv'


def getLoadedHorseCodeList():
    codeList = []
    for table in horse_table_list:
        if singleton_ScrubDB.table_exists(table):
            singleton_ScrubDB.cursor.execute('select code from {}'.format(table))
            list = singleton_ScrubDB.cursor.fetchall()
            for row in list:
                code = row['code'].strip()
                if code not in codeList:
                    codeList.append(code)
    return codeList

def getHorseCodeListByYear(year):
    codeList = []
    tableName = base_results_table.replace('year', str(year))
    if singleton_ScrubDB.table_exists(tableName):
        singleton_ScrubDB.cursor.execute('select horse_code from {}'.format(tableName))
        list = singleton_ScrubDB.cursor.fetchall()
        for row in list:
            code = row['horse_code'].strip()
            if code not in codeList:
                codeList.append(code)
    print('year:', year, 'horse code count:', len(codeList))
    return codeList


def exportLostCode(code):
    file = open(FILENAME_LOST_HORSE_CODE, 'a+', newline='')
    writer = csv.writer(file)
    writer.writerow([code])
    file.close()


def compareOrigAndLoaded(origList, loadedList):
    for code in origList:
        if code not in loadedList:
            # common.log('horse[' + code + '] lost')
            exportLostCode(code)

if __name__ == '__main__':
    all_horse_code_list = []
    for year in range(2013, 2020):
        list = getHorseCodeListByYear(year)
        for code in list:
            if code not in all_horse_code_list:
                all_horse_code_list.append(code)
    print('all horse count:', len(all_horse_code_list))

    # all_loaded_horse_code_list = getLoadedHorseCodeList()
    # print('loaded horse code count:', len(all_loaded_horse_code_list))

    # compareOrigAndLoaded(all_horse_code_list, all_loaded_horse_code_list)

