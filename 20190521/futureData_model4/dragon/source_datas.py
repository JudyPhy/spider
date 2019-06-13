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
from horse_speed import horse_last_dst_time
from horse_trend import horse_dct_trend
from horse_trend import horse_act_trend
from horse_trend import horse_odds_trend
from horse_rest import horse_rest
from horse_new_dis import horse_new_dis
from record import draw_record
from record import trainer_record
from record import jockey_record
from record import jockey_recent
from record import jockey_trainer_record
from hot import jockey_hot
from race_info import going as race_info_going


def getTrainer(race_date_No, horse_No, immd_info_dict, future_race_card_row):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        return immd_info_dict[race_date_No][horse_No]['trainer']
    return future_race_card_row['trainer'].strip()


def getJockey(race_date_No, horse_No, immd_info_dict, future_race_card_row):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array = immd_info_dict[race_date_No][horse_No]['jockey'].split('(')
        return array[0].strip()
    array = future_race_card_row['jockey'].split('(')
    return array[0].strip()


def getCourse(course_text):
    if '"' in course_text:
        array = course_text.split('"')
        return array[1].strip()
    return course_text.strip()


def getValue(race_date_No, horse_No, dict, default_value):
    if (race_date_No in dict.keys()) and (horse_No in dict[race_date_No].keys()):
        return dict[race_date_No][horse_No]
    return default_value


def getHorseRecords(race_date_No, horse_No, dict):
    if (race_date_No in dict.keys()) and (horse_No in dict[race_date_No].keys()):
        array = dict[race_date_No][horse_No]
        return [array[0] + array[1] + array[2] + array[3], array[4]]
    print("HorseRecord can't find:", race_date_No, horse_No)
    return [-1, -1]


def getHorseSpeeds(race_date_No, horse_No, dict):
    if (race_date_No in dict.keys()) and (horse_No in dict[race_date_No].keys()):
        return dict[race_date_No][horse_No]
    print("HorseSpeed can't find:", race_date_No, horse_No)
    return [-1, -1, -1]


def getRatingTrend(rtg_as_text):
    if '-' == rtg_as_text:
        return 0
    else:
        return int(rtg_as_text)


def getRecords(key, dict):
    if key in dict.keys():
        array = dict[key]
        return [array[0] + array[1] + array[2] + array[3], array[4]]
    return [-1, -1]


def getHot(key, dict):
    if key in dict.keys():
        return dict[key]
    return [-1, -1]


def prepareDatas(future_raceCard_rows, immd_info_dict, history_raceResults_rows, history_raceCard_rows, horse_pedigree_rows,
                 display_sectional_time_rows):
    data_dict = {}
    data_dict['going'] = race_info_going.GetAllGoingDict(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    data_dict['pedigree_dst'] = pedigree_dst.GetPedigreeDistanceDict(future_raceCard_rows, horse_pedigree_rows)

    data_dict['horse_record'] = horse_record.GetHorseRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_recent_record'] = horse_recent_record.GetHorseRecentRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_site_record'] = horse_site_record.GetHorseSiteRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_go_record'] = horse_go_record.GetHorseGoingRecord(future_raceCard_rows, history_raceResults_rows, data_dict['going'])
    data_dict['horse_course_record'] = horse_course_record.GetHorseCourseRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_dst_record'] = horse_dst_record.GetHorseDstRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_cls_record'] = horse_cls_record.GetHorseClsRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_draw_record'] = horse_draw_record.GetHorseDrawRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_jockey_record'] = horse_jockey_record.GetHorseJockeyRecord(future_raceCard_rows, immd_info_dict, history_raceResults_rows)

    data_dict['horse_speed'] = horse_speed.GetSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_recent_speed'] = horse_recent_speed.GetHorseRecentSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_site_speed'] = horse_site_speed.GetHorseSiteSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_go_speed'] = horse_go_speed.GetHorseGoSpeed(future_raceCard_rows, history_raceResults_rows, data_dict['going'])
    data_dict['horse_course_speed'] = horse_course_speed.GetHorseCourseSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_dst_speed'] = horse_dst_speed.GetHorseDstSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_cls_speed'] = horse_cls_speed.GetHorseClsSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_draw_speed'] = horse_draw_speed.GetHorseDrawSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_gear_speed'] = horse_gear_speed.GetHorseGearSpeed(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows)
    data_dict['horse_jockey_speed'] = horse_jockey_speed.GetHorseJockeySpeed(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    data_dict['horse_last_dst_time'] = horse_last_dst_time.GetHorseLastDstTime(future_raceCard_rows, history_raceResults_rows, display_sectional_time_rows, data_dict['going'])

    data_dict['rtg'] = current_rating.GetRtgDict(future_raceCard_rows)

    data_dict['horse_dct_trend'] = horse_dct_trend.GetDctTrend(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows)
    data_dict['horse_act_trend'] = horse_act_trend.GetActTrend(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows)

    data_dict['horse_rest'] = horse_rest.GetHorseRest(future_raceCard_rows, history_raceResults_rows)

    data_dict['horse_new_dis'] = horse_new_dis.GetHorseNewDis(future_raceCard_rows, history_raceResults_rows)

    data_dict['draw_record'] = draw_record.GetDrawRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['trainer_record'] = trainer_record.getTrainerRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['jockey_record'] = jockey_record.GetJockeyRecord(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    data_dict['jockey_recent'] = jockey_recent.GetJockeyRecent(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    data_dict['jockey_trainer_record'] = jockey_trainer_record.GetJockeyTrainerRecord(future_raceCard_rows, immd_info_dict, history_raceResults_rows)

    data_dict['jockey_hot'] = jockey_hot.GetJockeyHot(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    # for race_date_No, dict in data_dict['jockey_trainer_record'].items():
    #     print(race_date_No, dict)

    return data_dict
