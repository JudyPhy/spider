from db.database import singleton_Scrub_DB
from common import common
from config.myconfig import singleton_cfg
from horse_starts import main as cal_horse_starts
from horse_deltaDays import deltaDays as cal_horse_deltaDays
from horse_age import main as cal_horse_age
from horse_speed import main as cal_horse_speed
from current_rating import main as cal_current_rating
from season_stakes import main as cal_season_stakes
from dis_avesr import main as cal_dis_avesr
from dis_avesr_horse import main as cal_dis_avesr_horse
from horse_score import main as cal_horse_score
from go_aversr import main as cal_go_aversr
from go_aversr_horse import main as cal_go_aversr_horse
from new_dis import main as cal_new_dis
from horse_jockey import horse_jockey as cal_horse_jockey
from horse_trainer import horse_trainer as cal_horse_trainer
from jockey_trainer import jockey_trainer as cal_jockey_trainer

TODAY_HORSE_TABLE = singleton_cfg.getTodayHorseInfoTable()


# 获取当天比赛的马匹数据
def __searchTodayHorse():
    all_info = {}   # horse_code & row
    if singleton_Scrub_DB.table_exists(TODAY_HORSE_TABLE):
        race_date = singleton_cfg.getRaceDate()
        singleton_Scrub_DB.cursor.execute("select code,current_rating,season_stakes,total_stakes from {} where race_date=%s".format(TODAY_HORSE_TABLE), race_date)
        all_list = singleton_Scrub_DB.cursor.fetchall()
        singleton_Scrub_DB.connect.commit()
        for row in all_list:
            key = row['code'].strip()
            if key not in all_info.keys():
                all_info[key] = row
            else:
                common.log('has repeat horse in today_orig_horse_table, code=' + key)
        print('[source_dateas]today horse count=', len(all_info))
    else:
        common.log('sourse_datas: Table[' + TODAY_HORSE_TABLE + '] not exist.')
    return all_info


def getHorseInfo(row, today_horse_dict):
    horse_info = {}
    horse_code = row['horse_code']
    if horse_code in today_horse_dict.keys():
        horse_info['season_stakes'] = int(today_horse_dict[horse_code]['season_stakes'])
        horse_info['total_stakes'] = int(today_horse_dict[horse_code]['total_stakes'])
    else:
        horse_info['season_stakes'] = 0
        horse_info['total_stakes'] = 0
    return horse_info


def getRaceCount(row, today_count_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_No']))
    if race_id in today_count_dict.keys():
        return today_count_dict[race_id]
    return 0


# speed_dict: horse_code & [pre_speed, last_4_speed]
def getHorseSpeed(row, speed_dict):
    horse_code = row['horse_code']
    if horse_code in speed_dict.keys():
        return speed_dict[horse_code]
    return [0, 0]


# today_horse_dict: horse_code & current_rating
def getCurrentRating(row, today_horse_dict):
    horse_code = row['horse_code']
    if horse_code in today_horse_dict.keys():
        return today_horse_dict[horse_code]
    else:
        common.log('horse[' + horse_code + '] has no today and historay currenting data, ERROR!!!')
        return 0


def getHorseStartsInfo(row, horse_raceStarts_dict):
    dict = {}
    dict['No1_curRace'] = 0
    dict['No2_curRace'] = 0
    dict['No3_curRace'] = 0
    dict['No4_curRace'] = 0
    dict['Total_curRace'] = 0
    dict['No1_allRace'] = 0
    dict['No2_allRace'] = 0
    dict['No3_allRace'] = 0
    dict['No4_allRace'] = 0
    dict['Total_allRace'] = 0
    horse_code = row['horse_code']
    if horse_code in horse_raceStarts_dict.keys():
        row_starts = horse_raceStarts_dict[horse_code]
        dict['No1_curRace'] = row_starts['No1']
        dict['No2_curRace'] = row_starts['No2']
        dict['No3_curRace'] = row_starts['No3']
        dict['No4_curRace'] = row_starts['No4']
        dict['Total_curRace'] = row_starts['All']
        dict['No1_allRace'] = row_starts['No1']
        dict['No2_allRace'] = row_starts['No2']
        dict['No3_allRace'] = row_starts['No3']
        dict['No4_allRace'] = row_starts['No4']
        dict['Total_allRace'] = row_starts['All']
    return dict


def getHorseDate(key, dict, defualt_value):
    if key in dict.keys():
        return dict[key]
    return defualt_value


def getNewDisData(key, horse_newDis_dict, words_name, defualt_value):
    if key in horse_newDis_dict.keys():
        return horse_newDis_dict[key][words_name]
    return defualt_value


# 计算当天比赛的count字段，因未开始比赛，plc字段还未有值，因此所有马匹都算作有效马匹
def __calculateTodayCount(today_rows):
    dict = {}   # new_race_id & count
    for row in today_rows:
        key = int(str(row['race_date']) + common.toThreeDigitStr(row['race_No']))
        if key not in dict.keys():
            dict[key] = 0
        dict[key] += 1
    return dict


# horse_detail: horse_code & row
# race_count: new_race_id & count
# horse_raceStarts: horse_code & {No1:count, No2:count, No3:count, No4:count, All:count}
# horse_deltaDays: horse_code & deltaDays
# horse_score: horse_code & score
# horse_age: horse_code & age
# horse_speed: horse_code & [pre_speed, last_4_speed]
# current_rating: horse_code & current_rating
# season_stakes: horse_code & season_stakes
# dis_avesr: distance & ave_speed
# dis_avesr_horse: horse_code & dis_ave_speed
# go_aversr: going & ave_speed
# go_aversr_horse: horse_code & go_ave_speed
# horse_newDis: horse_code & {keys=>new_dis, rest, act_delta, dct_delta}
# hj_raceCount: hj & [all_count, all_count_before3]
# ht_raceCount: ht & [all_count, all_count_before3]
# jt_raceCount: jt & [all_count, all_count_before3]
def prepareDatas(today_rows):
    data_dict = {}
    data_dict['horse_detail'] = __searchTodayHorse()
    data_dict['race_count'] = __calculateTodayCount(today_rows)
    data_dict['horse_raceStarts'] = cal_horse_starts.getTodayHorseStartsDict(today_rows)
    data_dict['horse_deltaDays'] = cal_horse_deltaDays.getTodayDeltaDaysDict(today_rows)
    data_dict['horse_score'] = cal_horse_score.getAllHorseScoreDict(int(singleton_cfg.getRaceDate()))
    # data_dict['horse_age'] = cal_horse_age.getTodayHorseAgeDict()
    data_dict['horse_speed'] = cal_horse_speed.getTodayRaceHorseSpeedDict(today_rows)
    data_dict['current_rating'] = cal_current_rating.getTodayCurrentRatingBeforeRace()
    data_dict['season_stakes'] = cal_season_stakes.getTodaySeasonStakesBeforeRace()
    data_dict['dis_avesr'] = cal_dis_avesr.getTodayDistanceAveSpeed(today_rows)
    data_dict['dis_avesr_horse'] = cal_dis_avesr_horse.getTodayDistanceAveSpeed(today_rows)
    data_dict['go_aversr'] = cal_go_aversr.getTodayGoingAveSpeed(today_rows)
    data_dict['go_aversr_horse'] = cal_go_aversr_horse.getTodayGoingAveSpeed(today_rows)
    data_dict['horse_newDis'] = cal_new_dis.getTodayHorseNewDisDict(today_rows)
    data_dict['hj_raceCount'] = cal_horse_jockey.getTodayHorseJockeyDict(today_rows)
    data_dict['ht_raceCount'] = cal_horse_trainer.getTodayHorseTrainerDict(today_rows)
    data_dict['jt_raceCount'] = cal_jockey_trainer.getTodayJockeyTrainerDict(today_rows)
    return data_dict
