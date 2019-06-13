### 计算某年未退役的马匹 ###
from db.db import singleton_ScrubDB
from common import common
import csv

RESULTS_BASE_TABLE = 'f_race_results_year'

HORSE_TABLE_LIST = ['a_all_horse_info_20181115', 'a_all_horse_info_20181113']

FILENAME_UNRETIRED_HORSE_CODE = 'unretired_horse_code.csv'


def getHorseCodeListByYear(year):
    codeList = []
    tableName = RESULTS_BASE_TABLE.replace('year', str(year))
    if singleton_ScrubDB.table_exists(tableName):
        singleton_ScrubDB.cursor.execute('select horse_code from {}'.format(tableName))
        list = singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
        for row in list:
            code = row['horse_code'].strip()
            if code not in codeList:
                codeList.append(code)
    print('year:', year, 'horse code count:', len(codeList))
    return codeList


def getHorse(code):
    for table in HORSE_TABLE_LIST:
        if singleton_ScrubDB.table_exists(table):
            singleton_ScrubDB.cursor.execute('select retired from {} where code=%s'.format(table), code)
            horse = singleton_ScrubDB.cursor.fetchone()
            singleton_ScrubDB.connect.commit()
            if horse:
                return horse
        else:
            common.log('Table[' + table + '] not exist')
    return None


def getRetiredHorseDict(codeList):
    retiredDict = {}    # code & retired
    notFind = 0
    for code in codeList:
        horse = getHorse(code)
        if horse:
            retiredDict[code] = (horse['retired'] == 1)
        else:
            notFind += 1
    print('notFind:', notFind)
    return retiredDict


def exportUnretiredHorse(codeList):
    file = open(FILENAME_UNRETIRED_HORSE_CODE, 'a+', newline='')
    writer = csv.writer(file)
    for code in codeList:
        writer.writerow([code])
    file.close()


def main():
    unRetiredList = []
    for year in range(2013, 2014):
        codeList = getHorseCodeListByYear(year)
        retired_horse_dict = getRetiredHorseDict(codeList)
        year_unRetiredList = []
        for code, retired in retired_horse_dict.items():
            if not retired:
                if code not in unRetiredList:
                    unRetiredList.append(code)
                # year
                if code in year_unRetiredList:
                    common.log('horse[' + code + '] repeat, year:' + str(year))
                else:
                    year_unRetiredList.append(code)
        common.log('year:' + str(year) + ' => has ' + str(len(year_unRetiredList)) + ' unretired horses')

    common.log('all year=> has ' + str(len(unRetiredList)) + ' unretired horses')
    exportUnretiredHorse(unRetiredList)

if __name__ == '__main__':
    main()

