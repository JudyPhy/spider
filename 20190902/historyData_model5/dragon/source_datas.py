from common import common
from pedigree_dst import pedigree_dst
from results_table import results_table
from horse_record import horse_record, horse_recent_record, horse_fav_record
from horse_record import horse_site_course_record, horse_site_course_fav_record
from horse_record import horse_go_record, horse_dst_record, horse_cls_record, horse_gear_record
from horse_record import horse_best_recent_time
from trainer_records import trainer_record, trainer_recent_record, trainer_fav_record
from jockey_record import jockey_record, jockey_recent, jockey_fav_record
from horse_trend import horse_dct_trend
from horse_rest import horse_rest
from record import draw_record, track_fav_record, track_record
from cls_standard_time import cls_standard_time
from odds_wave import horse_odds_wave


def getRaceId(race_date_No, horse_code, sort_history_raceResults_rows):
    if (race_date_No in sort_history_raceResults_rows.keys()) and (horse_code in sort_history_raceResults_rows[race_date_No].keys()):
        year = int(race_date_No[len(race_date_No) - 8: len(race_date_No) - 6])
        month = int(race_date_No[len(race_date_No) - 6: len(race_date_No) - 4])
        if month < 8:
            year -= 1
        race_id = sort_history_raceResults_rows[race_date_No][horse_code]['race_id']
        new_race_id = int(str(year) + common.toThreeDigitStr(race_id))
        return new_race_id
    print("RaceId can't find:", race_date_No, horse_code)
    return -1


def getValue(race_date_No, horse_code, dict, defalut_value):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    print("Value can't find:", race_date_No, horse_code)
    return defalut_value


def getRecords(race_date_No, code, dict):
    if (race_date_No in dict.keys()) and (code in dict[race_date_No].keys()):
        records = dict[race_date_No][code]
        return [records[0] + records[1] + records[2] + records[3], records[4]]
    print(race_date_No, code, " can't find records")
    return [0, 0]


def getFavRecords(race_date_No, code, dict):
    if (race_date_No in dict.keys()) and (code in dict[race_date_No].keys()):
        records = dict[race_date_No][code]
        return [records[0] + records[1] + records[2], records[4]]
    print(race_date_No, code, " can't find fav records")
    return [0, 0]


def getHorseOddsWave(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    # print("HorseOddsSectionalTrend can't find:", race_date_No, horse_code)
    return 1


def getHorseOddsDiff(race_date_No, horse_code, dict):
    if (race_date_No in dict.keys()) and (horse_code in dict[race_date_No].keys()):
        return dict[race_date_No][horse_code]
    # print("HorseOddsDiff can't find:", race_date_No, horse_code)
    return 0


def __toRaceDateRows(sort_history_raceCard_rows):
    sort_race_date_rows = {} # race_date & [rows]
    for race_date_No, dict in sort_history_raceCard_rows.items():
        race_date = race_date_No[: len(race_date_No) - 2]
        if race_date not in sort_race_date_rows.keys():
            sort_race_date_rows[race_date] = []
        for horse_code, row in dict.items():
            sort_race_date_rows[race_date].append(row)
    return sort_race_date_rows


def prepareDatas(sort_history_raceCard_rows, sort_history_raceResults_rows, horse_pedigree_rows,
                 course_standard_times_rows, odds_sectional_rows, odds_immd_sectional_rows):
    data_dict = {}
    data_dict['race_info'] = results_table.GetRaceInfoDict(sort_history_raceCard_rows, sort_history_raceResults_rows)

    data_dict['horse_record'] = horse_record.GetHorseRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_recent_record'] = horse_recent_record.GetHorseRecentRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_fav_record'] = horse_fav_record.GetHorseFavRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_site_course_record'] = horse_site_course_record.GetHorseSiteCourseRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_site_course_fav_record'] = horse_site_course_fav_record.GetHorseSiteCourseFavRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_going_record'] = horse_go_record.GetHorseGoingRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_dst_record'] = horse_dst_record.GetHorseDstRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_cls_record'] = horse_cls_record.GetHorseClsRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['horse_gear_record'] = horse_gear_record.GetHorseGearRecord(sort_history_raceCard_rows, sort_history_raceResults_rows)

    sort_race_date_rows = __toRaceDateRows(sort_history_raceCard_rows)
    data_dict['trainer_record'] = trainer_record.GetTrainerRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['trainer_recent'] = trainer_recent_record.GetTrainerRecentRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['trainer_fav_record'] = trainer_fav_record.GetTrainerFavRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['jockey_record'] = jockey_record.GetJockeyRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['jockey_recent'] = jockey_recent.GetJockeyRecent(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['jockey_fav_record'] = jockey_fav_record.GetJockeyFavRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['draw_record'] = draw_record.GetDrawRecord(sort_race_date_rows, sort_history_raceResults_rows)
    data_dict['track_record'] = track_record.GetTrackRecord(sort_race_date_rows)
    data_dict['track_fav_record'] = track_fav_record.GetTrackFavRecord(sort_race_date_rows, sort_history_raceResults_rows)

    data_dict['horse_dct_trend'] = horse_dct_trend.GetHorseDctTrend(sort_history_raceCard_rows, sort_history_raceResults_rows)

    data_dict['horse_rest'] = horse_rest.GetHorseRest(sort_history_raceCard_rows, sort_history_raceResults_rows)
    data_dict['pedigree_dst'] = pedigree_dst.GetPedigreeDistanceDict(sort_history_raceCard_rows, horse_pedigree_rows)

    data_dict['horse_best_recent_speed'] = horse_best_recent_time.GetHorseBestRecentSpeed(sort_history_raceCard_rows, sort_history_raceResults_rows)

    data_dict['cls_standard_speed'] = cls_standard_time.GetClsStandardSpeedDict(sort_history_raceCard_rows, course_standard_times_rows)

    data_dict['horse_odds_wave'] = horse_odds_wave.getOddsWave(sort_history_raceCard_rows, sort_history_raceResults_rows, odds_sectional_rows, odds_immd_sectional_rows)

    data_dict['horse_odds_diff'] = horse_odds_wave.getOddsDiff(sort_history_raceCard_rows, sort_history_raceResults_rows, odds_sectional_rows, odds_immd_sectional_rows)

    # for race_date_No, dict in data_dict['track_record'].items():
    #     print(race_date_No, dict)

    return data_dict

