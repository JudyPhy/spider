from db.db import singleton_ScrubDB
from common import common

def getAllResults():
    results = {}    # horse_code & {new_race_id & row}
    for year in range(2013, 2020):
        tableName = 'f_race_results_' + str(year)
        singleton_ScrubDB.cursor.execute('select * from {}'.format(tableName))
        rows = singleton_ScrubDB.cursor.fetchall()
        for row in rows:
            horse_code = row['horse_code'].strip()
            if horse_code not in results.keys():
                results[horse_code] = {}
            array_race_date = row['race_date'].split('/')
            year = array_race_date[2]
            race_id = row['race_id']
            new_race_id = year[len(year) - 2:] + common.toDoubleDigitStr(array_race_date[1]) + common.toDoubleDigitStr(array_race_date[0]) + common.toThreeDigitStr(race_id)
            results[horse_code][new_race_id] = row
        singleton_ScrubDB.connect.commit()
    return results


def getHorseInfo(horse_code):
    horse_race = {}  # new_race_id & row
    tableName = 'c_horse_race_info'
    singleton_ScrubDB.cursor.execute('select * from {} where code=%s'.format(tableName), horse_code)
    rows = singleton_ScrubDB.cursor.fetchall()
    singleton_ScrubDB.connect.commit()
    for row in rows:
        array_race_date = row['race_date'].split('/')
        str_year = array_race_date[2]
        if len(str_year) > 2:
            year = int(str_year[len(str_year) - 2:])
        else:
            year = int(str_year)
        race_id = row['race_id']
        if (year >= 13) and (race_id != 'Overseas'):
            new_race_id = str(year) + common.toDoubleDigitStr(array_race_date[1]) + common.toDoubleDigitStr(array_race_date[0]) + common.toThreeDigitStr(race_id)
            horse_race[new_race_id] = row
    return horse_race


# 数量检查 ['L308', 'T044', 'V126']
def compareCount():
    results = getAllResults()
    print('horse count:', len(results.keys()))
    less_code_list = []
    for horse_code, results_races in results.items():
        print('\n', horse_code)
        horse_race = getHorseInfo(horse_code)
        for horse_race_id, horseRace in horse_race.items():
            if horse_race_id not in results_races.keys():
                common.log('horse[' + horse_code + '] race_id more than results:' + horse_race_id)
        less_race_id = ''
        for results_race_id in results_races.keys():
            if results_race_id not in horse_race.keys():
                less_race_id += results_race_id + ', '
                if horse_code not in less_code_list:
                    less_code_list.append(horse_code)
        if less_race_id != '':
            common.log('horse[' + horse_code + '] race_id less than results:\n' + less_race_id)
    if len(less_code_list) > 0:
        print('less_code_list\n', less_code_list)


def comparePlc():
    results = getAllResults()
    error_code_list = []
    for horse_code, results_races in results.items():
        print('\n', horse_code)
        horse_race = getHorseInfo(horse_code)
        for horse_race_id, horseRace in horse_race.items():
            if ('N287' == horse_code) and (horse_race_id == '130120333'):
                continue
            same = False
            plc_horseRace = horseRace['pla'].replace('DH', '').strip()
            plc_results = results_races[horse_race_id]['plc'].replace('DH', '').strip()
            if plc_horseRace not in common.words:
                if plc_results not in common.words:
                    same = int(plc_horseRace) == int(plc_results)
            else:
                same = plc_horseRace == plc_results
            if not same:
                common.log('horse[' + horse_code + '], race_id[' + horse_race_id + ']=> ' + plc_horseRace + ',' + plc_results)
                if horse_code not in error_code_list:
                    error_code_list.append(horse_code)
    print(error_code_list)


if __name__ == '__main__':
    comparePlc()

