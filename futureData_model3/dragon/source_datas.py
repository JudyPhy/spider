from current_rating import current_rating
from pedigree_dst import pedigree_dst
from results_table import results_table
from horse_record import horse_record
from horse_record import horse_recent_record
from horse_record import horse_site_record
from horse_record import horse_go_record
from horse_record import horse_course_record
from horse_record import horse_dst_record
from horse_record import horse_cls_record
from horse_record import horse_draw_record
from horse_record import horse_jockey_record
from horse_speed import horse_speed
from horse_speed import horse_recent_speed
from horse_speed import horse_site_speed
from horse_speed import horse_go_speed
from horse_speed import horse_course_speed
from horse_speed import horse_dst_speed
from horse_speed import horse_cls_speed
from horse_speed import horse_draw_speed
from horse_speed import horse_jockey_speed
from horse_speed import horse_gear_speed
from horse_trend import horse_dct_trend
from horse_trend import horse_act_trend
from horse_trend import horse_odds_trend
from horse_rest import horse_rest
from horse_new_dis import horse_new_dis
from record import draw_record
from record import trainer_record
from record import jockey_record
from record import jockey_recent
from hot import jockey_hot


def __getSeasonId(race_date):   # race_date: 20190202 str
    str_date = str(race_date)
    year = int(str_date[len(str_date) - 6: len(str_date) - 4])
    month = int(str_date[len(str_date) - 4: len(str_date) - 2])
    if month < 8:
        return year - 1
    else:
        return year


def getLastRaceId(race_date, dict):
    race_date_No_list = []
    for date_No, horse_dict in dict.items():
        if date_No not in race_date_No_list:
            race_date_No_list.append(date_No)
    sort_race_date_No_List = sorted(race_date_No_list)
    nearest_date = '0'
    race_date_No = race_date + '01'
    for date_No in sort_race_date_No_List:
        if (date_No < race_date_No) and (date_No > nearest_date):
            nearest_date_No = date_No
    if nearest_date_No in dict.keys():
        for horse_code, row in dict[nearest_date_No].items():
            return row['race_id']
    return 0


lost_pedigreeDst_horse = []
def getPedigreeDst(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    if horse_code not in lost_pedigreeDst_horse:
        lost_pedigreeDst_horse.append(horse_code)
    # print("PedigreeDst can't find:", horse_code, race_id)
    return False

def showLostPedigreeDst():
    print('\nlost pedigreeDst horse(', len(lost_pedigreeDst_horse), '):', lost_pedigreeDst_horse)


def getHorseRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseRecentRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseRecentRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseSiteRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseSiteRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseGoingRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseGoingRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseCourseRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseCourseRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseDstRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseDstRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseClsRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseClsRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseDrawRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseDrawRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseJockeyRecord(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseJockeyRecord can't find:", race_date_No, horse_code)
    return [-1, -1, -1, -1, -1]


def getHorseSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseRecentSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseRecentSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseSiteSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseSiteSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseGoSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseGoSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseCourseSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseCourseSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseDstSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseDstSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseClsSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseClsSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseDrawSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseDrawSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseGearSpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseGearSpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getHorseJockeySpeed(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseJockeySpeed can't find:", race_date_No, horse_code)
    return [-1, -1, -1]


def getRtg(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("Rtg can't find:", race_date_No, horse_code)
    return -1


def getHorseDctTrend(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseDctTrend can't find:", race_date_No, horse_code)
    return -1


def getHorseActTrend(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseActTrend can't find:", race_date_No, horse_code)
    return -1


def getHorseRest(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseRest can't find:", race_date_No, horse_code)
    return -1


def getHorseNewDis(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("HorseNewDis can't find:", race_date_No, horse_code)
    return False


def getDrawRecord(race_date, draw, dict):
    if (race_date in dict.keys()) and (draw in dict[race_date].keys()):
        return dict[race_date][draw]
    # print("DrawRecord can't find:", race_date, draw)
    return [0, 0, 0, 0, 0]


def getTrainerRecord(race_date, trainer, dict):
    if (race_date in dict.keys()) and (trainer in dict[race_date].keys()):
        return dict[race_date][trainer]
    # print("TrainerRecord can't find:", race_date, trainer)
    return [0, 0, 0, 0, 0]


def getJockeyRecord(race_date, jockey, dict):
    if (race_date in dict.keys()) and (jockey in dict[race_date].keys()):
        return dict[race_date][jockey]
    # print("JockeyRecord can't find:", race_date, jockey)
    return [0, 0, 0, 0, 0]


def getJockeyRecent(race_date, jockey, dict):
    if (race_date in dict.keys()) and (jockey in dict[race_date].keys()):
        return dict[race_date][jockey]
    # print("JockeyRecent can't find:", race_date, jockey)
    return [0, 0, 0, 0, 0]


def getJockeyHot(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("JockeyHot can't find:", race_date_No, horse_code)
    return -1


def getJockeyHotBefore4(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("JockeyHotBefore4 can't find:", race_date_No, horse_code)
    return -1


# plc_dict: race_date_No & {horse_code & plc}

# pedigree_dst: race_date_No & {horse_code & pedigree_dst(bool)}

# horse_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_recent_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_site_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_go_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_course_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_dst_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_cls_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_draw_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}
# horse_jockey_record: race_date_No & {horse_code & [No1, No2, No3, No4, Fail]}

# horse_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_recent_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_site_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_go_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_course_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_dst_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_cls_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_draw_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_jockey_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}
# horse_gear_speed: race_date_No & {horse_code & [highest_speed, lowest_speed, avr_speed]}

# rtg: race_date_No & {horse_code & rtg}

# horse_dct_trend: race_date_No & {horse_code & dct_trend}
# horse_act_trend: race_date_No & {horse_code & act_trend}

# horse_rest: race_date_No & {horse_code & rest}

# horse_new_dis: race_date_No & {horse_code & new_dis}

# draw_record: race_date & {draw & [No1, No2, No3, No4, Fail]}
# trainer_record: race_date & {trainer & [No1, No2, No3, No4, Fail]}
# jockey_record: race_date & {jockey & [No1, No2, No3, No4, Fail]}
# jockey_recent: race_date & {jockey & [No1, No2, No3, No4, Fail]}

# jockey_hot: race_date_No & {horse_code & jockey_hot}
# jockey_hot_before4: race_date_No & {horse_code & jockey_hot_before4}
def prepareDatas(raceCard_rows, results_rows):
    data_dict = {}
    plc_dict = results_table.getPlcDict(raceCard_rows, results_rows)
    going_dict = results_table.getGoingDict(raceCard_rows, results_rows)
    data_dict['pedigree_dst'] = pedigree_dst.getPedigreeDistanceDict(raceCard_rows)

    data_dict['horse_record'] = horse_record.getHorseRecord(raceCard_rows, plc_dict)
    data_dict['horse_recent_record'] = horse_recent_record.getHorseRecentRecord(raceCard_rows, plc_dict)
    data_dict['horse_site_record'] = horse_site_record.getHorseSiteRecord(raceCard_rows, plc_dict)
    data_dict['horse_go_record'] = horse_go_record.getHorseGoingRecord(raceCard_rows, plc_dict, going_dict)
    data_dict['horse_course_record'] = horse_course_record.getHorseCourseRecord(raceCard_rows, plc_dict)
    data_dict['horse_dst_record'] = horse_dst_record.getHorseDstRecord(raceCard_rows, plc_dict)
    data_dict['horse_cls_record'] = horse_cls_record.getHorseClsRecord(raceCard_rows, results_rows, plc_dict)
    data_dict['horse_draw_record'] = horse_draw_record.getHorseDrawRecord(raceCard_rows, plc_dict)
    data_dict['horse_jockey_record'] = horse_jockey_record.getHorseJockeyRecord(raceCard_rows, plc_dict)

    data_dict['horse_speed'] = horse_speed.getSpeed(raceCard_rows, results_rows)
    data_dict['horse_recent_speed'] = horse_recent_speed.getHorseRecentSpeed(raceCard_rows, results_rows)
    data_dict['horse_site_speed'] = horse_site_speed.getHorseSiteSpeed(raceCard_rows, results_rows)
    data_dict['horse_go_speed'] = horse_go_speed.getHorseGoSpeed(raceCard_rows, results_rows, going_dict)
    data_dict['horse_course_speed'] = horse_course_speed.getHorseCourseSpeed(raceCard_rows, results_rows)
    data_dict['horse_dst_speed'] = horse_dst_speed.getHorseDstSpeed(raceCard_rows, results_rows)
    data_dict['horse_cls_speed'] = horse_cls_speed.getHorseClsSpeed(raceCard_rows, results_rows)
    data_dict['horse_draw_speed'] = horse_draw_speed.getHorseDrawSpeed(raceCard_rows, results_rows)
    data_dict['horse_gear_speed'] = horse_gear_speed.getHorseGearSpeed(raceCard_rows, results_rows)
    data_dict['horse_jockey_speed'] = horse_jockey_speed.getHorseJockeySpeed(raceCard_rows, results_rows)

    data_dict['rtg'] = current_rating.getRtgDict(raceCard_rows)

    data_dict['horse_dct_trend'] = horse_dct_trend.getDctTrend(raceCard_rows)
    data_dict['horse_act_trend'] = horse_act_trend.getActTrend(raceCard_rows)

    data_dict['horse_rest'] = horse_rest.getHorseRest(raceCard_rows)

    data_dict['horse_new_dis'] = horse_new_dis.getHorseNewDis(raceCard_rows)

    data_dict['draw_record'] = draw_record.getDrawRecord(raceCard_rows, plc_dict)
    data_dict['trainer_record'] = trainer_record.getTrainerRecord(raceCard_rows, plc_dict)
    data_dict['jockey_record'] = jockey_record.getJockeyRecord(raceCard_rows, plc_dict)
    data_dict['jockey_recent'] = jockey_recent.getJockeyRecent(raceCard_rows, plc_dict)

    data_dict['jockey_hot'], data_dict['jockey_hot_before4'] = jockey_hot.getJockeyHot(raceCard_rows, results_rows)
    return data_dict
