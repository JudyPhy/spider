from db.db import singleton_ScrubDB
from db.db import singleton_ResultsDB


def getResultsTableRows(tableName):
    if singleton_ResultsDB.table_exists(tableName):
        singleton_ResultsDB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_ResultsDB.cursor.fetchall()
        singleton_ResultsDB.connect.commit()
        return rows
    return []


def getScrubTableRows(tableName):
    if singleton_ScrubDB.table_exists(tableName):
        singleton_ScrubDB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
        return rows
    print('table[', tableName, '] not exist in scrub')
    return []


def compareTwoTable(table1, table2):
    rows_table1 = getResultsTableRows(table1)
    rows_table2 = getResultsTableRows(table2)
    exKeys = ['id', 'updateTime']
    # print(rows_table1[0].keys())
    diffrent_dict = {}  # key & raceInfo
    for row_2 in rows_table2:
        race_date = row_2['race_date']
        race_no = row_2['race_no']
        horse_no = row_2['horse_no']
        # print('\n', race_date, race_no, horse_no)
        find = False
        for row_1 in rows_table1:
            if (row_1['race_date'] == race_date) and (row_1['race_no'] == race_no) and (row_1['horse_no'] == horse_no):
                find = True
                keys = row_1.keys()
                for key in keys:
                    if key in exKeys:
                        continue
                    elif (key in row_2) and (row_1[key] != row_2[key]):
                        if key not in diffrent_dict.keys():
                            diffrent_dict[key] = {}
                        diffrent_dict[key]['race_date'] = race_date
                        diffrent_dict[key]['race_no'] = race_no
                        diffrent_dict[key]['horse_no'] = horse_no
                        diffrent_dict[key]['table1'] = row_1[key]
                        diffrent_dict[key]['table2'] = row_2[key]
                        # print('\n', race_date, race_no, horse_no)
                        # print('not same:', race_date, race_no, horse_no, ' key:', key, ' table1:', row_1[key], ' table2:', row_2[key])
                break
        if not find:
            print("data can't find in[", table1, ']:', race_date, race_no, horse_no)
    print('keys:', diffrent_dict.keys())
    for key, value in diffrent_dict.items():
        print(key, value)


compareTwoTable('today_table_dragon_model3s_20190403', 'today_table_dragon_model3s_20190403_A')

