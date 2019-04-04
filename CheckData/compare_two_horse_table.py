from db.db import singleton_ScrubDB
from db.db import singleton_ResultsDB
from common import common


TABLE1 = 'all_origin_horse_data'
TABLE2 = 'a_future_horse_info_20181226'


def getAllHorseList(tableName):
    codeList = []
    singleton_ResultsDB.cursor.execute('select code from {}'.format(tableName))
    all = singleton_ResultsDB.cursor.fetchall()
    singleton_ResultsDB.connect.commit()
    for row in all:
        if row['code'] not in codeList:
            codeList.append(row['code'])
    return codeList


def getHorseList(tableName):
    codeList = []
    singleton_ScrubDB.cursor.execute('select code from {}'.format(tableName))
    all = singleton_ScrubDB.cursor.fetchall()
    singleton_ScrubDB.connect.commit()
    for row in all:
        if row['code'] not in codeList:
            codeList.append(row['code'])
    return codeList


def compareTwoHorseTables():
    codeList1 = getAllHorseList(TABLE1)
    codeList2 = getHorseList(TABLE2)
    lostCodeList = []
    for horse2 in codeList2:
        # for horse1 in codeList1:
        #     if horse1 == horse2:
        #         print(horse1)
        if horse2 not in codeList1:
            lostCodeList.append(horse2)
    print('table2 lost horse count:', len(lostCodeList))
    print(lostCodeList)


if __name__ == '__main__':
    compareTwoHorseTables()

