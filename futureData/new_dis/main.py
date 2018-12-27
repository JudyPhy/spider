###    判断该马过去4场比赛是否距离全部小于当前距离的80%    ###
###    当前马匹距离上一场比赛的时间间隔    ###
###    当前马匹负重距离上一场比赛的变化   ###
###    当前马匹排位体重距离上一场比赛的变化   ###
from config.myconfig import singleton_cfg
from common import common
from db.database import singleton_Results_DB
from db.database import singleton_Scrub_DB
import datetime

HISTORY_RESULTS_FROM_TABLE = singleton_cfg.getHistoryRaceTable()
TODAY_RESULTS_FROM_TABLE = singleton_cfg.getTodayResultsTable()


def __getHistoryHorseRaceData(horse_code_list, today_date):
    horse_race_dict = {}  # horse_code & {new_race_id & {key=>distance, actual_wt, declar_horse_wt}
    if singleton_Results_DB.table_exists(HISTORY_RESULTS_FROM_TABLE):
        singleton_Results_DB.cursor.execute(
            '''select race_date,race_id,horse_code,distance,plc,actual_wt,declar_horse_wt from {} where race_date<%s'''.format(HISTORY_RESULTS_FROM_TABLE), today_date)
        rows_orig = singleton_Results_DB.cursor.fetchall()
        singleton_Results_DB.connect.commit()
        for row in rows_orig:
            horse_code = row['horse_code']
            if horse_code in horse_code_list:
                new_race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
                if horse_code not in horse_race_dict.keys():
                    horse_race_dict[horse_code] = {}
                if row['plc'] not in common.words:
                    dict = {}
                    dict['distance'] = int(row['distance'])
                    dict['actual_wt'] = int(row['actual_wt'])
                    dict['declar_horse_wt'] = int(row['declar_horse_wt'])
                    horse_race_dict[horse_code][new_race_id] = dict
    else:
        common.log('new_dis: table[' + HISTORY_RESULTS_FROM_TABLE + '] not exist')
    return horse_race_dict


def __getTodayHorseRaceData():
    horse_race_dict = {}  # horse_code & {key=>distance, actual_wt, declar_horse_wt}
    if singleton_Scrub_DB.table_exists(TODAY_RESULTS_FROM_TABLE):
        singleton_Scrub_DB.cursor.execute(
            'select race_date,race_id,horse_code,distance,wt,horse_wt_dec from {}'.format(TODAY_RESULTS_FROM_TABLE))
        rows_orig = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in rows_orig:
            horse_code = row['horse_code']
            if horse_code not in horse_race_dict.keys():
                horse_race_dict[horse_code] = {}
                horse_race_dict[horse_code]['race_date'] = row['race_date']
                horse_race_dict[horse_code]['distance'] = int(row['distance'])
                horse_race_dict[horse_code]['actual_wt'] = int(row['wt'])
                horse_race_dict[horse_code]['declar_horse_wt'] = int(row['horse_wt_dec'])
    else:
        common.log('new_dis: table[' + TODAY_RESULTS_FROM_TABLE + '] not exist')
    return horse_race_dict


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


def getTodayHorseNewDisDict(today_rows):
    horse_code_list = []
    for row in today_rows:
        horse_code = row['horse_code']
        if horse_code not in horse_code_list:
            horse_code_list.append(horse_code)
    today_date = today_rows[0]['race_date']
    history_race_dict = __getHistoryHorseRaceData(horse_code_list, today_date)  # horse_code & {new_race_id & {key=>distance, actual_wt, declar_horse_wt}
    today_race_dict = __getTodayHorseRaceData() # horse_code & {key=>distance, actual_wt, declar_horse_wt}

    horse_results_dict = {}  # horse_code & {keys=>new_dis, rest, act_delta, dct_delta}
    for horse_code, race_dict in history_race_dict.items():
        if horse_code not in horse_results_dict.keys():
            horse_results_dict[horse_code] = {}
            horse_results_dict[horse_code]['new_dis'] = False
            horse_results_dict[horse_code]['rest'] = 0
            horse_results_dict[horse_code]['act_delta'] = 0
            horse_results_dict[horse_code]['dct_delta'] = 0

        curRaceDate = today_race_dict[horse_code]['race_date']
        curDistance = today_race_dict[horse_code]['distance']
        curActualWt = today_race_dict[horse_code]['actual_wt']
        curDeclarWt = today_race_dict[horse_code]['declar_horse_wt']

        race_id_sorted_list = sorted(race_dict.keys())
        race_id_sorted_list.reverse()
        # new dis
        if len(race_id_sorted_list) > 3:
            temp_new_dis = True
            for race_id in race_id_sorted_list[:4]:
                prev_distance = race_dict[race_id]['distance']
                if prev_distance >= (curDistance * 0.8):
                    temp_new_dis = False
                    break
            horse_results_dict[horse_code]['new_dis'] = temp_new_dis

            # rest, act_delta, dct_delta
        if len(race_id_sorted_list) > 0:
            pre_race_id_text = str(race_id_sorted_list[0])
            horse_results_dict[horse_code]['rest'] = __getCurRaceRest(pre_race_id_text[: len(pre_race_id_text) - 3], str(curRaceDate))

            pre_wt = race_dict[race_id_sorted_list[0]]['actual_wt']
            horse_results_dict[horse_code]['act_delta'] = curActualWt - pre_wt

            pre_wt_dec = race_dict[race_id_sorted_list[0]]['declar_horse_wt']
            horse_results_dict[horse_code]['dct_delta'] = curDeclarWt - pre_wt_dec
        else:
            horse_results_dict[horse_code]['rest'] = 0
            horse_results_dict[horse_code]['act_delta'] = 0
            horse_results_dict[horse_code]['dct_delta'] = 0

    return horse_results_dict







