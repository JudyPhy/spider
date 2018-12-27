from common import common
import datetime


def __getCurRaceRest(last_race_date, cur_race_date):
    last_year = int(last_race_date[: (len(last_race_date) - 4)])
    last_month = int(last_race_date[(len(last_race_date) - 4): (len(last_race_date) - 2)])
    last_day = int(last_race_date[(len(last_race_date) - 2):])
    cur_year = int(cur_race_date[: (len(cur_race_date) - 4)])
    cur_month = int(cur_race_date[(len(cur_race_date) - 4): (len(cur_race_date) - 2)])
    cur_day = int(cur_race_date[(len(cur_race_date) - 2):])
    last_time = datetime.datetime(last_year, last_month, last_day)
    cur_time = datetime.datetime(cur_year, cur_month, cur_day)
    deltaDays = (cur_time - last_time).days
    return deltaDays


def getHorseNewDisDict(history_rows):
    # 按比赛日期排序
    race_rows = {}  # new_race_id & [row, row, ...]
    for row in history_rows:
        new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if new_race_id not in race_rows.keys():
            race_rows[new_race_id] = []
        race_rows[new_race_id].append(row)
    race_id_sorted_list = sorted(race_rows.keys())
    # 计算每场比赛各匹马的new_dis, rest, act_delta, dct_delta
    horse_race_dict = {}   # horse_code & [{key=>distance, race_date, actual_wt, declar_horse_wt}, {key=>distance, race_date, actual_wt, declar_horse_wt}, ...]
    horse_newDis_dict = {}  # new_race_id & {horse_code & {keys=>new_dis, rest, act_delta, dct_delta}}
    for race_id in race_id_sorted_list:
        if race_id not in horse_newDis_dict.keys():
            horse_newDis_dict[race_id] = {}
        curRaceRows = race_rows[race_id]
        for row in curRaceRows:
            if row['plc'] not in common.words:
                horse_code = row['horse_code']
                curDistance = int(row['distance'])
                curWt = int(row['actual_wt'])
                curWtDec = int(row['declar_horse_wt'])

                # 赛前
                if horse_code not in horse_newDis_dict[race_id].keys():
                    horse_newDis_dict[race_id][horse_code] = {}
                if horse_code in horse_race_dict.keys():
                    # new_dis
                    if len(horse_race_dict[horse_code]) >= 4:
                        new_dis = True
                        for info in horse_race_dict[horse_code][:4]:
                            if info['distance'] >= (curDistance * 0.8):
                                new_dis = False
                                break
                    else:
                        new_dis = False

                    # rest
                    pre_date = str(horse_race_dict[horse_code][0]['race_date'])
                    rest = __getCurRaceRest(pre_date, str(row['race_date']))

                    # act_delta
                    act_delta = curWt - horse_race_dict[horse_code][0]['actual_wt']

                    # dct_delta
                    dct_delta = curWtDec - horse_race_dict[horse_code][0]['declar_horse_wt']

                    horse_newDis_dict[race_id][horse_code]['new_dis'] = new_dis
                    horse_newDis_dict[race_id][horse_code]['rest'] = rest
                    horse_newDis_dict[race_id][horse_code]['act_delta'] = act_delta
                    horse_newDis_dict[race_id][horse_code]['dct_delta'] = dct_delta
                else:
                    horse_newDis_dict[race_id][horse_code]['new_dis'] = False
                    horse_newDis_dict[race_id][horse_code]['rest'] = 0
                    horse_newDis_dict[race_id][horse_code]['act_delta'] = 0
                    horse_newDis_dict[race_id][horse_code]['dct_delta'] = 0

                # 赛后累加
                if horse_code not in horse_race_dict.keys():
                    horse_race_dict[horse_code] = []
                temp_dict = {}
                temp_dict['distance'] = curDistance
                temp_dict['race_date'] = row['race_date']
                temp_dict['actual_wt'] = curWt
                temp_dict['declar_horse_wt'] = curWtDec
                horse_race_dict[horse_code].insert(0, temp_dict)
    return horse_newDis_dict







