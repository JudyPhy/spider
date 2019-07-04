from pedigree_dst import pedigree_dst
from horse_record import horse_record, horse_recent_record, horse_fav_record
from horse_record import horse_site_course_record, horse_site_course_fav_record
from horse_record import horse_go_record, horse_dst_record, horse_cls_record, horse_gear_record
from trainer_record import trainer_record, trainer_recent, trainer_fav_record
from jockey_record import jockey_record, jockey_recent, jockey_fav_record
from horse_trend import horse_dct_trend
from horse_time import horse_best_recent_time
from horse_rest import horse_rest
from record import draw_record, track_fav_record, track_record
from race_info import going as race_info_going
from common import common


def getTrainer(race_date_No, horse_No, immd_info_dict, future_race_card_row):
    if (race_date_No in immd_info_dict.keys()) and (horse_No in immd_info_dict[race_date_No].keys()):
        array = immd_info_dict[race_date_No][horse_No]['trainer'].split('(')
        return array[0].strip()
    array = future_race_card_row['trainer'].split('(')
    return array[0].strip()


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


def getPedigreeDst(horse_code, dict, default_value):
    if horse_code in dict.keys():
        return dict[horse_code]
    return default_value


def getHorseRecords(race_date_No, horse_No, dict):
    if (race_date_No in dict.keys()) and (horse_No in dict[race_date_No].keys()):
        array = dict[race_date_No][horse_No]
        return [array[0] + array[1] + array[2] + array[3], array[4]]
    print("HorseRecord can't find:", race_date_No, horse_No)
    return [0, 0]


def getHorseFavRecords(race_date_No, horse_No, dict):
    if (race_date_No in dict.keys()) and (horse_No in dict[race_date_No].keys()):
        array = dict[race_date_No][horse_No]
        return [array[0] + array[1] + array[2], array[4]]
    print("HorseFavRecord can't find:", race_date_No, horse_No)
    return [0, 0]


def getRecords(key, dict):
    if key in dict.keys():
        array = dict[key]
        return [array[0] + array[1] + array[2] + array[3], array[4]]
    return [0, 0]


def getFavRecords(key, dict):
    if key in dict.keys():
        array = dict[key]
        return [array[0] + array[1] + array[2], array[4]]
    return [0, 0]


def getClsStandardSpeed(site, course, dst, cls, course_standard_times_rows):
    cur_course = course
    if '"' in cur_course:
        cur_track = site + 'TurfTrack'
    else:
        cur_track = site + 'AllWeatherTrack'
    for row in course_standard_times_rows:
        cur_dist = int(row['distance'])
        if (cur_track == row['track']) and (cur_dist == dst):
            cur_time = ''
            if 'Class' in cls:
                if '1' in cls:
                    cur_time = row['cls_1']
                elif '2' in cls:
                    cur_time = row['cls_2']
                elif '3' in cls:
                    cur_time = row['cls_3']
                elif '4' in cls:
                    cur_time = row['cls_4']
                elif '5' in cls:
                    cur_time = row['cls_5']
            elif 'Group' in cls:
                cur_time = row['GroupRace']
            elif 'Griffin' in cls:
                cur_time = row['GriffinRace']
            else:
                cur_time = row['GroupRace']
            # to time
            if (cur_time == '') or ('-' in cur_time):
                return 0
            else:
                return cur_dist/common.GetTotalSeconds(cur_time)
    return 0


def prepareDatas(future_raceCard_rows, immd_info_dict, history_raceResults_rows, history_raceCard_rows, horse_pedigree_rows):
    data_dict = {}
    data_dict['going'] = race_info_going.GetAllGoingDict(future_raceCard_rows, immd_info_dict, history_raceResults_rows)

    data_dict['horse_record'] = horse_record.GetHorseRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_recent_record'] = horse_recent_record.GetHorseRecentRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_fav_record'] = horse_fav_record.GetHorseFavRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_site_course_record'] = horse_site_course_record.GetHorseSiteCourseRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_site_course_fav_record'] = horse_site_course_fav_record.GetHorseSiteCourseFavRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_go_record'] = horse_go_record.GetHorseGoingRecord(future_raceCard_rows, history_raceResults_rows, data_dict['going'])
    data_dict['horse_dst_record'] = horse_dst_record.GetHorseDstRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_cls_record'] = horse_cls_record.GetHorseClsRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_gear_record'] = horse_gear_record.GetHorseGearRecord(future_raceCard_rows, history_raceCard_rows, history_raceResults_rows)

    data_dict['trainer_record'] = trainer_record.getTrainerRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['trainer_recent'] = trainer_recent.getTrainerRecentRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['trainer_fav_record'] = trainer_fav_record.getTrainerFavRecord(future_raceCard_rows, history_raceResults_rows)

    data_dict['jockey_record'] = jockey_record.GetJockeyRecord(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    data_dict['jockey_recent'] = jockey_recent.GetJockeyRecent(future_raceCard_rows, immd_info_dict, history_raceResults_rows)
    data_dict['jockey_fav_record'] = jockey_fav_record.GetJockeyFavRecent(future_raceCard_rows, immd_info_dict, history_raceResults_rows)

    data_dict['draw_record'] = draw_record.GetDrawRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['track_fav_record'] = track_fav_record.GetTrackFavRecord(future_raceCard_rows, history_raceResults_rows)
    data_dict['track_record'] = track_record.GetTrackRecord(future_raceCard_rows, history_raceResults_rows)

    data_dict['horse_dct_trend'] = horse_dct_trend.GetDctTrend(future_raceCard_rows, history_raceResults_rows, history_raceCard_rows)

    data_dict['horse_best_recent_speed'] = horse_best_recent_time.GetHorseBestRecentSpeed(future_raceCard_rows, history_raceResults_rows)
    data_dict['horse_rest'] = horse_rest.GetHorseRest(future_raceCard_rows, history_raceResults_rows)
    data_dict['pedigree_dst'] = pedigree_dst.GetPedigreeDistanceDict(future_raceCard_rows, horse_pedigree_rows)
    # for race_date_No, dict in data_dict['jockey_trainer_record'].items():
    #     print(race_date_No, dict)

    return data_dict
