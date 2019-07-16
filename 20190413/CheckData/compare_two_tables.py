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
    diffrent_dict = {}  # key & [{raceInfo}]
    for row_2 in rows_table2:
        if row_2['horse_no'] >= 1000:
            continue
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
                    elif row_1[key] != row_2[key]:
                        if key not in diffrent_dict.keys():
                            diffrent_dict[key] = []
                        info_dict = {}
                        info_dict['race_date'] = race_date
                        info_dict['race_no'] = race_no
                        info_dict['horse_no'] = horse_no
                        info_dict['table1'] = row_1[key]
                        info_dict['table2'] = row_2[key]
                        diffrent_dict[key].append(info_dict)
                        # print('\n', race_date, race_no, horse_no)
                        # print('not same:', race_date, race_no, horse_no, ' key:', key, ' table1:', row_1[key], ' table2:', row_2[key])
                break
        if not find:
        #     if 20190224 == row_2['race_date']:
        #         pass
        #     else:
            print("data can't find in[", table1, ']:', race_date, race_no, horse_no)
    print('keys:', diffrent_dict.keys())
    for key, array in diffrent_dict.items():
        for dif in array:
            print(key, dif)


compareTwoTable('table_dragon_history_model5', 'table_dragon_history_model5_7_14')

