from common import common
from horse_starts import main as cal_horse_starts
from horse_deltaDays import deltaDays as cal_horse_deltaDays
from horse_age import main as cal_horse_age
from horse_speed import main as cal_horse_speed
from current_rating import main as cal_current_rating
from dis_avesr import main as cal_dis_avesr
from dis_avesr_horse import main as cal_dis_avesr_horse
from horse_score import main as cal_horse_score
from go_aversr import main as cal_go_aversr
from go_aversr_horse import main as cal_go_aversr_horse
from new_dis import main as cal_new_dis
from season_stakes import main as cal_season_stakes
from total_stakes import main as cal_total_stakes
from jockey_trainer import jockey_trainer as cal_jt_raceCount
from horse_jockey import horse_jockey as cal_hj_raceCount
from horse_trainer import horse_trainer as cal_ht_raceCount


def getHorseInfo(row, all_horse_dict):
    horse_info = {}
    horse_code = row['horse_code']
    if horse_code in all_horse_dict.keys():
        horse_info['season_stakes'] = int(all_horse_dict[horse_code]['season_stakes'])
        horse_info['total_stakes'] = int(all_horse_dict[horse_code]['total_stakes'])
    else:
        horse_info['season_stakes'] = 0
        horse_info['total_stakes'] = 0
    return horse_info


# all_count_dict: new_race_id & count
def getRaceCount(row, all_count_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    if race_id in all_count_dict.keys():
        return all_count_dict[race_id]
    return 0


# horse_raceStarts_dict: new_race_id & {horse_code & [No1, No2, No3, No4, ALL]}
# horse_allRaceStarts_dict: horse_code & [No1, No2, No3, No4, ALL]
def getHorseStartsInfo(row, horse_raceStarts_dict, horse_allRaceStarts_dict):
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
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in horse_raceStarts_dict.keys()) and (horse_code in horse_raceStarts_dict[race_id].keys()):
        curHorseRaceStarts = horse_raceStarts_dict[race_id][horse_code]
        dict['No1_curRace'] = curHorseRaceStarts[0]
        dict['No2_curRace'] = curHorseRaceStarts[1]
        dict['No3_curRace'] = curHorseRaceStarts[2]
        dict['No4_curRace'] = curHorseRaceStarts[3]
        dict['Total_curRace'] = curHorseRaceStarts[4]
    if horse_code in horse_allRaceStarts_dict:
        curHorseAllStarts = horse_allRaceStarts_dict[horse_code]
        dict['No1_allRace'] = curHorseAllStarts[0]
        dict['No2_allRace'] = curHorseAllStarts[1]
        dict['No3_allRace'] = curHorseAllStarts[2]
        dict['No4_allRace'] = curHorseAllStarts[3]
        dict['Total_allRace'] = curHorseAllStarts[4]
    return dict


# horse_deltaDays_dict: new_race_id & {horse_code & deltaDays}
def getHorseDeltaDays(row, horse_deltaDays_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in horse_deltaDays_dict.keys()) and (horse_code in horse_deltaDays_dict[race_id].keys()):
        return horse_deltaDays_dict[race_id][horse_code]
    return 0


# score_dict: new_race_id & {horse_code & score}
def getHorseScore(row, score_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in score_dict.keys()) and (horse_code in score_dict[race_id].keys()):
        return score_dict[race_id][horse_code]
    return common.HORSE_DEFAULT_SCORE


# age_dict: new_race_id & {horse_code & age}
def getHorseAge(row, age_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in age_dict.keys()) and (horse_code in age_dict[race_id].keys()):
        return age_dict[race_id][horse_code]
    return 0


# speed_dict: new_race_id & {horse_code & [pre_speed, last_4_speed]}
def getHorseSpeed(row, speed_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in speed_dict.keys()) and (horse_code in speed_dict[race_id].keys()):
        return speed_dict[race_id][horse_code]
    return [0, 0]


# has_before_data_dict: race_date & {horse_code & current_rating}
def getCurrentRating(row, has_before_data_dict):
    race_date = row['race_date']
    horse_code = row['horse_code'].strip()
    if (race_date in has_before_data_dict.keys()) and (horse_code in has_before_data_dict[race_date].keys()):
        return has_before_data_dict[race_date][horse_code]
    return -1


# rtg_dict: race_date(int) & {horse_code & rtg}
def getRtg(row, rtg_dict):
    race_date = row['race_date']
    horse_code = row['horse_code']
    if (race_date in rtg_dict.keys()) and (horse_code in rtg_dict[race_date].keys()):
        return rtg_dict[race_date][horse_code]
    return -1


# dis_avesr_dict: new_race_id & ave_speed
def getDistanceAveSpeed(row, dis_avesr_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    if race_id in dis_avesr_dict.keys():
        return dis_avesr_dict[race_id]
    return 0


# dis_avesr_horse_dict: new_race_id & {horse_code & ave_speed}
def getDistanceAveHorseSpeed(row, dis_avesr_horse_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in dis_avesr_horse_dict.keys()) and (horse_code in dis_avesr_horse_dict[race_id].keys()):
        return dis_avesr_horse_dict[race_id][horse_code]
    return 0


# go_aversr: new_race_id & go_speed
def getGoingAveSpeed(row, go_avesr_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    if race_id in go_avesr_dict.keys():
        return go_avesr_dict[race_id]
    return 0


# go_avesr_horse_dict: new_race_id & {horse_code & go_speed}
def getGoingAveHorseSpeed(row, go_avesr_horse_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in go_avesr_horse_dict.keys()) and (horse_code in go_avesr_horse_dict[race_id].keys()):
        return go_avesr_horse_dict[race_id][horse_code]
    return 0


# horse_newDis: new_race_id & {horse_code & {keys=>new_dis, rest, act_delta, dct_delta}}
def getNewDis(row, horse_newDis_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in horse_newDis_dict.keys()) and (horse_code in horse_newDis_dict[race_id].keys()):
        new_dis = horse_newDis_dict[race_id][horse_code]['new_dis']
        rest = horse_newDis_dict[race_id][horse_code]['rest']
        act_delta = horse_newDis_dict[race_id][horse_code]['act_delta']
        dct_delta = horse_newDis_dict[race_id][horse_code]['dct_delta']
        return [new_dis, rest, act_delta, dct_delta]
    return [False, 0, 0, 0]


# horse_seasonStakes_dict: race_date & {horse_code & season_stakes}
def getSeasonStakes(row, horse_seasonStakes_dict):
    race_date = row['race_date']
    horse_code = row['horse_code']
    if (race_date in horse_seasonStakes_dict.keys()) and (horse_code in horse_seasonStakes_dict[race_date].keys()):
        return horse_seasonStakes_dict[race_date][horse_code]
    return -1


# horse_totalStakes_dict: race_date & {horse_code & total_stakes}
def getTotalStakes(row, horse_totalStakes_dict):
    race_date = row['race_date']
    horse_code = row['horse_code']
    if (race_date in horse_totalStakes_dict.keys()) and (horse_code in horse_totalStakes_dict[race_date].keys()):
        return horse_totalStakes_dict[race_date][horse_code]
    return -1


# hjt_raceCount_dict: new_race_id & {horse_code & [all_count, all_count_before3]}
def getHorseJockeyTrainerRaceCount(row, hjt_raceCount_dict):
    race_id = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
    horse_code = row['horse_code']
    if (race_id in hjt_raceCount_dict.keys()) and (horse_code in hjt_raceCount_dict[race_id].keys()):
        return hjt_raceCount_dict[race_id][horse_code]
    return [0, 0]


def __getRaceCount(history_rows):
    dict = {}   # new_race_id & count
    for row in history_rows:
        key = int(str(row['race_date']) + common.toThreeDigitStr(row['race_id']))
        if key not in dict.keys():
            dict[key] = 0
        if row['plc'] not in common.words:
            dict[key] += 1
    return dict


# horse_detail: horse_code & row
# race_count: new_race_id & count
# horse_raceStarts: new_race_id & {horse_code & [No1, No2, No3, No4, ALL]}
# horse_allRaceStarts: horse_code & [No1, No2, No3, No4, ALL]
# horse_deltaDays: new_race_id & {horse_code & deltaDays}
# horse_score: new_race_id & {horse_code & score}
# horse_age: new_race_id & {horse_code & age}
# horse_speed: new_race_id & {horse_code & [pre_speed, last_4_speed]}
# current_rating: race_date & {horse_code & current_rating}
# rtg: race_date(int) & {horse_code & rtg}
# dis_avesr: new_race_id & ave_speed
# dis_avesr_horse: new_race_id & {horse_code & ave_speed}
# go_aversr: new_race_id & go_speed
# go_aversr_horse: new_race_id & {horse_code & go_speed}
# horse_newDis: new_race_id & {horse_code & {keys=>new_dis, rest, act_delta, dct_delta}}
# season_stakes: race_date & {horse_code & season_stakes}
# total_stakes: race_date & {horse_code & total_stakes}
# jt_raceCount: new_race_id & {horse_code & [all_raceCount, all_raceCount_before3]}
# hj_raceCount: new_race_id & {horse_code & [all_raceCount, all_raceCount_before3]}
# ht_raceCount: new_race_id & {horse_code & [all_raceCount, all_raceCount_before3]}
def prepareDatas(history_rows):
    data_dict = {}
    data_dict['race_count'] = __getRaceCount(history_rows)
    data_dict['horse_raceStarts'], data_dict['horse_allRaceStarts'] = cal_horse_starts.getHorseStartsDict(history_rows)
    data_dict['horse_deltaDays'] = cal_horse_deltaDays.getDeltaDaysDict(history_rows)
    data_dict['horse_score'] = cal_horse_score.getHorseScoreDict(history_rows)
    data_dict['horse_age'] = cal_horse_age.getHorseAgeDict(history_rows)
    data_dict['horse_speed'] = cal_horse_speed.getRaceHorseSpeedDict(history_rows)
    data_dict['current_rating'] = cal_current_rating.getCurrentRatingBeforeRace()
    data_dict['rtg'] = cal_current_rating.getRtg()
    data_dict['dis_avesr'] = cal_dis_avesr.getDistanceAveSpeed(history_rows)
    data_dict['dis_avesr_horse'] = cal_dis_avesr_horse.getDistanceAveSpeed(history_rows)
    data_dict['go_aversr'] = cal_go_aversr.getGoingAveSpeed(history_rows)
    data_dict['go_aversr_horse'] = cal_go_aversr_horse.getGoingAveSpeed(history_rows)
    data_dict['horse_newDis'] = cal_new_dis.getHorseNewDisDict(history_rows)
    data_dict['season_stakes'] = cal_season_stakes.getSeasonStakesBeforeRace()
    data_dict['total_stakes'] = cal_total_stakes.getTotalStakesBeforeRace()
    data_dict['jt_raceCount'] = cal_jt_raceCount.getJockeyTrainerRaceCount(history_rows)
    data_dict['hj_raceCount'] = cal_hj_raceCount.getHorseJockeyRaceCount(history_rows)
    data_dict['ht_raceCount'] = cal_ht_raceCount.getHorseTrainerRaceCount(history_rows)
    return data_dict
