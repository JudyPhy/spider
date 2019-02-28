from db.db import singleton_ScrubDB
from common import common


def getAllRace():
    rows = []
    for year in range(2017, 2020):
        tableName = 't_race_card_' + str(year)
        singleton_ScrubDB.cursor.execute('select * from {}'.format(tableName))
        rows += singleton_ScrubDB.cursor.fetchall()
        singleton_ScrubDB.connect.commit()
    return rows


def getSomeRace():
    tableName = 't_race_card_20190220'
    singleton_ScrubDB.cursor.execute('select * from {}'.format(tableName))
    rows = singleton_ScrubDB.cursor.fetchall()
    singleton_ScrubDB.connect.commit()
    return rows


def compare():
    all_race = getAllRace()
    som_race = getSomeRace()
    for row_some in som_race:
        race_date_some = row_some['race_date']
        race_No_some = row_some['race_No']
        horse_No_some = row_some['horse_No']
        find = False
        for row_all in all_race:
            race_date_all = row_all['race_date']
            race_No_all = row_all['race_No']
            horse_No_all = row_all['horse_No']
            if (race_date_all == race_date_some) and (race_No_some == race_No_all) and (horse_No_some == horse_No_all):
                find = True
                for key, value in row_some.items():
                    if key == 'id' or key == 'updateTime':
                        continue
                    if value != row_all[key]:
                        print('\nrace_date=', race_date_all, ', race_No=', race_No_all, ', horse_No=', horse_No_all,
                              ', key=', key, ', some=', value, ', all=', row_all[key])
                break
        if not find:
            print('less:', row_some)


def sameHorseCheck():
    horse_count = {}    # code & count
    all_race = getAllRace()
    for row_all in all_race:
        horse_code = row_all['horse_code'].strip()
        if horse_code not in horse_count:
            horse_count[horse_code] = 0
        horse_count[horse_code] += 1

    code_list = []
    for code, count in horse_count.items():
        if count > 1 and code not in code_list:
            code_list.append(code)
    print(len(code_list))

    in_some_list = []
    som_race = getSomeRace()
    for row_some in som_race:
        horse_code = row_some['horse_code'].strip()
        if (horse_code in code_list) and (horse_code not in in_some_list):
            in_some_list.append(horse_code)
    print(len(in_some_list))

    test_code = in_some_list[0]
    print('test_code:', test_code, horse_count[test_code])
    race_list = []
    for row_all in all_race:
        horse_code = row_all['horse_code'].strip()
        if horse_code == test_code:
            race_list.append([row_all['race_date'], row_all['race_No']])
    print(race_list)

    for row_all in all_race:
        horse_code = row_all['horse_code'].strip()
        if horse_code == test_code and row_all['race_date'] == '20181202':
            print(row_all['rtg'], row_all['rtg_as'])
        if horse_code == test_code and row_all['race_date'] == '20181212':
            print(row_all['rtg'], row_all['rtg_as'])
        if horse_code == test_code and row_all['race_date'] == '20190101':
            print(row_all['rtg'], row_all['rtg_as'])
        if horse_code == test_code and row_all['race_date'] == '20190116':
            print(row_all['rtg'], row_all['rtg_as'])
        if horse_code == test_code and row_all['race_date'] == '20190202':
            print(row_all['rtg'], row_all['rtg_as'])
        if horse_code == test_code and row_all['race_date'] == '20190220':
            print(row_all['rtg'], row_all['rtg_as'])


def sameHorse():
    horse_count = {}  # code & count
    all_race = getAllRace()
    for row_all in all_race:
        horse_code = row_all['horse_code'].strip()
        if horse_code not in horse_count:
            horse_count[horse_code] = 0
        horse_count[horse_code] += 1

    code_list = []
    for code, count in horse_count.items():
        if count > 1 and code not in code_list:
            code_list.append(code)
    print(len(code_list))

    for row_all in all_race:
        horse_code = row_all['horse_code'].strip()
        if horse_code == code_list[0]:
            print(row_all['race_date'], row_all['age'])


if __name__ == '__main__':
    # compare()
    # sameHorseCheck()
    sameHorse()
