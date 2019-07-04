from common import common


def getGearList(gear):
    array_gear = gear.split('/')
    gear_list = []
    for sub in array_gear:
        for number in range(10):
            sub = sub.replace(str(number), '')
        if ('-' in sub) or (sub == ''):
            sub = '-'
        if sub not in gear_list:
            gear_list.append(sub)
    return gear_list



def getDct(race_date_No, horse_code, history_raceCard_rows):
    if (race_date_No in history_raceCard_rows.keys()) and (horse_code in history_raceCard_rows[race_date_No].keys()):
        return history_raceCard_rows[race_date_No][horse_code]['horse_wt_dec']
    print(race_date_No, horse_code, "can't find dct in history_raceCard_rows")
    return '-'


def getAct(race_date_No, horse_code, history_raceCard_rows):
    if (race_date_No in history_raceCard_rows.keys()) and (horse_code in history_raceCard_rows[race_date_No].keys()):
        return history_raceCard_rows[race_date_No][horse_code]['wt']
    print(race_date_No, horse_code, "can't find act in history_raceCard_rows")
    return '-'


def getLastDstTotalSeconds(race_date_No, horse_code, display_sectional_time_rows):
    if (race_date_No in display_sectional_time_rows.keys()) and (horse_code in display_sectional_time_rows[race_date_No].keys()):
        row = display_sectional_time_rows[race_date_No][horse_code]
        time_list = []
        for n in range(1, 7):
            key = 'sec{0}_time'.replace('{0}', str(n))
            if row[key] != '':
                time_list.append(row[key])
        if len(time_list) > 0:
            return common.GetTotalSeconds(time_list[len(time_list) - 1])
    return 0

